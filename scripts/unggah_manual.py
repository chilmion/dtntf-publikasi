#!/usr/bin/env python3
"""
Mini app lokal: unggah Excel luaran manual ke GitHub tanpa login GitHub.

    python3 scripts/unggah_manual.py

Membuka halaman di http://127.0.0.1:8787 (hanya bisa diakses dari komputermu
sendiri). Pilih berkas .xlsx → "Periksa" (cek isi, tanpa mengirim apa pun) →
"Unggah & perbarui" (menaruh berkas di manual/luaran.xlsx di GitHub; workflow
"Perbarui data manual" lalu jalan otomatis, ±1 menit).

Token GitHub (Personal Access Token) diminta SEKALI dan disimpan di
~/.dtntf-publikasi-token (izin 600). Token tidak pernah dikirim ke browser
dan tidak masuk repo. Stdlib saja.
"""

import base64
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import manual  # noqa: E402

REPO = os.environ.get("DTNTF_REPO", "chilmion/dtntf-publikasi")
CABANG = os.environ.get("DTNTF_CABANG", "main")
BERKAS = "manual/luaran.xlsx"
PORT = int(os.environ.get("DTNTF_PORT", "8787"))
TOKEN_FILE = pathlib.Path.home() / ".dtntf-publikasi-token"
MAKS_BYTE = 5 * 1024 * 1024


def baca_token():
    t = os.environ.get("GITHUB_TOKEN", "").strip()
    if t:
        return t
    try:
        return TOKEN_FILE.read_text().strip()
    except OSError:
        return ""


def siapkan_ssl():
    """Python buatan python.org di macOS sering belum punya sertifikat akar
    ("CERTIFICATE_VERIFY_FAILED"). Kalau begitu, pakai sertifikat bawaan macOS
    (keychain). SSL_CERT_FILE juga diwarisi proses anak (mis. build.py)."""
    if os.environ.get("SSL_CERT_FILE"):
        return
    try:
        urllib.request.urlopen(urllib.request.Request(
            "https://api.github.com", headers={"User-Agent": "dtntf-unggah"}), timeout=20)
        return
    except urllib.error.HTTPError:
        return                       # TLS beres; GitHub hanya membalas kode HTTP
    except Exception as e:
        if "CERTIFICATE_VERIFY_FAILED" not in str(e) or sys.platform != "darwin":
            return
    try:
        pem = subprocess.run(
            ["security", "find-certificate", "-a", "-p",
             "/System/Library/Keychains/SystemRootCertificates.keychain",
             "/Library/Keychains/System.keychain"],
            capture_output=True, text=True, timeout=60).stdout
        if "BEGIN CERTIFICATE" in pem:
            f = pathlib.Path.home() / ".dtntf-ca.pem"
            f.write_text(pem)
            os.environ["SSL_CERT_FILE"] = str(f)
            print("Sertifikat SSL disiapkan dari keychain macOS.")
    except Exception:
        pass


def gh(metode, jalur, token, badan=None):
    req = urllib.request.Request(
        "https://api.github.com" + jalur, method=metode,
        data=json.dumps(badan).encode() if badan is not None else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "dtntf-unggah",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            teks = r.read().decode()
            return r.status, (json.loads(teks) if teks else {})
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}
    except urllib.error.URLError as e:
        return 0, {"message": f"tidak bisa terhubung ke GitHub ({e.reason})"}


def periksa_isi(data):
    """→ dict ringkasan; melempar ValueError kalau berkas tak terbaca."""
    if len(data) > MAKS_BYTE:
        raise ValueError("Berkas terlalu besar (maks 5 MB).")
    if data[:2] != b"PK":
        raise ValueError("Ini bukan berkas .xlsx. Simpan dari Excel sebagai 'Excel Workbook (.xlsx)'.")
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        f.write(data)
        path = f.name
    try:
        try:
            baris = manual.baca_berkas(path)
        except Exception as e:
            raise ValueError(f"Berkas tidak terbaca ({type(e).__name__}). Pastikan ada sheet bernama 'Luaran'.")
    finally:
        os.unlink(path)
    if baris and not {"dosen", "jenis", "judul", "tahun"} <= set(baris[0]):
        raise ValueError("Kolom wajib tidak lengkap. Baris 1 harus berisi: dosen, jenis, judul, tahun. "
                         "Jangan ubah nama kolom di templat.")
    per_dosen, masalah, valid = manual.validasi(baris)
    per_jenis, dosen = {}, {}
    for s, es in per_dosen.items():
        dosen[s] = len(es)
        for e in es:
            per_jenis[e["kategori"]] = per_jenis.get(e["kategori"], 0) + 1
    return {"baris": len(baris), "valid": valid, "masalah": masalah,
            "per_dosen": dosen, "contoh": [
                {"no": r["_baris"], "dosen": r.get("dosen"), "jenis": r.get("jenis"),
                 "judul": r.get("judul"), "tahun": r.get("tahun")} for r in baris[:8]]}


HALAMAN = r"""<!doctype html><html lang=id><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Unggah luaran manual DTNTF</title>
<style>
:root{--navy:#073C64;--dark:#1A2C43;--lilac:#F7F7FB;--line:#e3e4ec;--lime:#C8E86D}
*{box-sizing:border-box}body{margin:0;font:15px/1.55 'Plus Jakarta Sans',system-ui,sans-serif;color:#0B0B16;background:var(--lilac)}
main{max-width:760px;margin:0 auto;padding:32px 20px 60px}
h1{font-size:1.4rem;color:var(--dark);margin:0 0 4px}.sub{color:#4a5264;margin:0 0 24px}
.kartu{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px;margin-bottom:16px}
h2{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;color:var(--dark);margin:0 0 12px}
button{font:inherit;font-weight:600;padding:10px 18px;border-radius:8px;border:1px solid var(--navy);
 background:var(--navy);color:#fff;cursor:pointer}button.abu{background:#fff;color:var(--navy)}
button[disabled]{opacity:.5;cursor:default}
input[type=text],input[type=password]{width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit}
.ok{color:#2e6b1f}.err{color:#9b2c2c}.kecil{font-size:.82rem;color:#4a5264}
table{border-collapse:collapse;width:100%;font-size:.84rem}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
ul{margin:8px 0;padding-left:20px}.aksi{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
#kotak{border:2px dashed #b9c4d0;border-radius:10px;padding:26px;text-align:center;background:var(--lilac)}
</style>
<main>
<h1>Unggah luaran manual</h1>
<p class=sub>Satu berkas Excel untuk seluruh jurusan → <b id=repo></b></p>

<div class=kartu id=k-token style="display:none">
 <h2>1. Sambungkan ke GitHub (sekali saja)</h2>
 <p class=kecil>Buat token di GitHub: Settings → Developer settings → Personal access tokens → Fine-grained tokens →
 Generate. Repository access: hanya repo ini. Permissions: <b>Contents = Read and write</b> dan
 <b>Actions = Read and write</b>. Tempel di bawah. Token disimpan di komputer ini saja.</p>
 <input type=password id=token placeholder="github_pat_…" autocomplete=off>
 <div class=aksi><button id=simpan>Simpan token</button></div><p id=pesan-token></p>
</div>

<div class=kartu id=k-berkas>
 <h2>Pilih berkas Excel</h2>
 <div id=kotak><input type=file id=berkas accept=".xlsx"><p class=kecil>Templat: manual/templat-luaran.xlsx</p></div>
 <div class=aksi><button id=periksa disabled>Periksa</button></div>
 <div id=hasil></div>
</div>

<div class=kartu id=k-unggah style="display:none">
 <h2>Kirim ke GitHub</h2>
 <p class=kecil>Berkas akan menggantikan manual/luaran.xlsx yang lama. Riwayat versi tetap tersimpan di GitHub.</p>
 <div class=aksi><button id=unggah>Unggah &amp; perbarui</button>
 <button id=jalan class=abu>Jalankan ulang saja (tanpa unggah)</button></div><p id=pesan-unggah></p>
</div>
</main>
<script>
var $=function(i){return document.getElementById(i)}, isi=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function api(jalur,opsi){opsi=opsi||{};opsi.headers=Object.assign({'X-Aplikasi':'1'},opsi.headers||{});
 return fetch(jalur,opsi).then(function(r){return r.json()})}
function status(){api('/status').then(function(s){$('repo').textContent=s.repo;
 $('k-token').style.display=s.token?'none':'block';})}
status();
$('simpan').onclick=function(){api('/token',{method:'POST',body:JSON.stringify({token:$('token').value})}).then(function(r){
 $('pesan-token').className=r.ok?'ok':'err';$('pesan-token').textContent=r.pesan;if(r.ok)status();})};
$('berkas').onchange=function(){var f=this.files[0];$('periksa').disabled=!f;$('hasil').innerHTML='';$('k-unggah').style.display='none';
 if(!f)return;var rd=new FileReader();rd.onload=function(){isi=rd.result;};rd.readAsArrayBuffer(f);};
$('periksa').onclick=function(){if(!isi)return;$('hasil').innerHTML='<p class=kecil>Memeriksa…</p>';
 api('/periksa',{method:'POST',body:isi}).then(function(r){
  if(!r.ok){$('hasil').innerHTML='<p class=err>'+esc(r.pesan)+'</p>';return}
  var h='<p><b>'+r.valid+'</b> dari '+r.baris+' baris valid.</p>';
  var pd=Object.keys(r.per_dosen);if(pd.length)h+='<p class=kecil>Dosen: '+pd.map(function(k){return esc(k)+' ('+r.per_dosen[k]+')'}).join(', ')+'</p>';
  if(r.masalah.length)h+='<p class=err>Perlu diperbaiki (baris ini dilewati):</p><ul>'+r.masalah.map(function(m){return '<li>'+esc(m)+'</li>'}).join('')+'</ul>';
  if(r.contoh.length)h+='<table><tr><th>#</th><th>Dosen</th><th>Jenis</th><th>Judul</th><th>Tahun</th></tr>'+r.contoh.map(function(c){
   return '<tr><td>'+c.no+'</td><td>'+esc(c.dosen)+'</td><td>'+esc(c.jenis)+'</td><td>'+esc(c.judul)+'</td><td>'+esc(c.tahun)+'</td></tr>'}).join('')+'</table>';
  $('hasil').innerHTML=h;$('k-unggah').style.display=r.valid?'block':'none';
  if(!r.valid)$('hasil').innerHTML+='<p class=err>Tidak ada baris valid, jadi tidak bisa diunggah.</p>';});};
$('unggah').onclick=function(){$('unggah').disabled=true;$('pesan-unggah').className='kecil';$('pesan-unggah').textContent='Mengunggah…';
 api('/unggah',{method:'POST',body:isi}).then(function(r){$('unggah').disabled=false;$('pesan-unggah').className=r.ok?'ok':'err';
  $('pesan-unggah').innerHTML=esc(r.pesan)+(r.tautan?' <a href="'+esc(r.tautan)+'" target=_blank>Lihat prosesnya di GitHub ↗</a>':'');})};
$('jalan').onclick=function(){api('/jalankan',{method:'POST'}).then(function(r){$('pesan-unggah').className=r.ok?'ok':'err';
 $('pesan-unggah').innerHTML=esc(r.pesan)+(r.tautan?' <a href="'+esc(r.tautan)+'" target=_blank>Lihat ↗</a>':'');})};
</script></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "dtntf-unggah"

    def log_message(self, *a):
        pass

    def kirim(self, kode, obj, tipe="application/json; charset=utf-8"):
        b = obj.encode() if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(kode)
        self.send_header("Content-Type", tipe)
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def lokal(self):
        # tolak permintaan dari situs lain (DNS rebinding / CSRF)
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("127.0.0.1", "localhost")

    def do_GET(self):
        if not self.lokal():
            return self.kirim(403, {"ok": False})
        if self.path == "/":
            return self.kirim(200, HALAMAN, "text/html; charset=utf-8")
        if self.path == "/status":
            return self.kirim(200, {"repo": REPO, "token": bool(baca_token())})
        self.kirim(404, {"ok": False})

    def do_POST(self):
        if not self.lokal() or self.headers.get("X-Aplikasi") != "1":
            return self.kirim(403, {"ok": False, "pesan": "Ditolak."})
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAKS_BYTE + 1024:
            return self.kirim(413, {"ok": False, "pesan": "Berkas terlalu besar."})
        body = self.rfile.read(n)
        fungsi = getattr(self, "p_" + self.path.strip("/"), None)
        if fungsi is None:
            return self.kirim(404, {"ok": False, "pesan": "Tidak dikenal."})
        fungsi(body)

    def p_token(self, body):
        t = (json.loads(body or b"{}").get("token") or "").strip()
        kode, r = gh("GET", f"/repos/{REPO}", t)
        if kode != 200:
            return self.kirim(200, {"ok": False, "pesan": f"Token ditolak GitHub ({r.get('message', kode)}). "
                                    "Periksa akses repo dan izin Contents."})
        TOKEN_FILE.write_text(t)
        os.chmod(TOKEN_FILE, 0o600)
        self.kirim(200, {"ok": True, "pesan": "Tersambung. Token tersimpan."})

    def p_periksa(self, body):
        try:
            self.kirim(200, dict(ok=True, **periksa_isi(body)))
        except ValueError as e:
            self.kirim(200, {"ok": False, "pesan": str(e)})

    def p_unggah(self, body):
        try:
            hasil = periksa_isi(body)
        except ValueError as e:
            return self.kirim(200, {"ok": False, "pesan": str(e)})
        if not hasil["valid"]:
            return self.kirim(200, {"ok": False, "pesan": "Tidak ada baris valid."})
        t = baca_token()
        if not t:
            return self.kirim(200, {"ok": False, "pesan": "Token belum disimpan."})
        kode, r = gh("GET", f"/repos/{REPO}/contents/{BERKAS}?ref={CABANG}", t)
        badan = {"message": f"Perbarui luaran manual ({hasil['valid']} baris)",
                 "content": base64.b64encode(body).decode(), "branch": CABANG}
        if kode == 200:
            badan["sha"] = r["sha"]
        elif kode != 404:
            return self.kirim(200, {"ok": False, "pesan": f"GitHub menolak ({r.get('message', kode)})."})
        kode, r = gh("PUT", f"/repos/{REPO}/contents/{BERKAS}", t, badan)
        if kode not in (200, 201):
            return self.kirim(200, {"ok": False, "pesan": f"Gagal mengunggah ({r.get('message', kode)})."})
        self.kirim(200, {"ok": True, "tautan": f"https://github.com/{REPO}/actions",
                         "pesan": "Terunggah. Data diperbarui otomatis dalam ±1–2 menit."})

    def p_jalankan(self, body):
        t = baca_token()
        if not t:
            return self.kirim(200, {"ok": False, "pesan": "Token belum disimpan."})
        kode, r = gh("POST", f"/repos/{REPO}/actions/workflows/manual.yml/dispatches", t, {"ref": CABANG})
        ok = kode == 204
        self.kirim(200, {"ok": ok, "tautan": f"https://github.com/{REPO}/actions",
                         "pesan": "Pembaruan dijalankan." if ok else
                         f"Gagal ({r.get('message', kode)}). Pastikan token punya izin Actions."})


def main():
    siapkan_ssl()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"Mini app berjalan di {url}\nTekan Ctrl+C untuk berhenti.")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nBerhenti.")


if __name__ == "__main__":
    main()
