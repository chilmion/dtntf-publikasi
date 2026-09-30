#!/usr/bin/env python3
"""
Ambil data SINTA dari KOMPUTERMU (IP Indonesia), lalu kirim hasilnya ke GitHub.

    python3 scripts/perbarui_lokal.py            # tanya: uji 2 dosen atau semua
    python3 scripts/perbarui_lokal.py semua      # 38 dosen, tanpa tanya
    python3 scripts/perbarui_lokal.py faridah,widya-rosita

Langkah: (1) sambung ke GitHub dengan token (sama seperti unggah_manual.py),
(2) samakan folder lokal dengan versi terbaru di GitHub, (3) scrape SINTA,
(4) pasang data manual, (5) kirim yang berubah sebagai SATU commit ke main,
(6) picu penerbitan ulang GitHub Pages. Data lama tidak ditimpa bila scrape
gagal. Stdlib saja; tidak perlu git.
"""

import base64
import getpass
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import unggah_manual as um  # noqa: E402  (gh, token, REPO, CABANG)

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO, CABANG = um.REPO, um.CABANG
DISINKRON = ("data/", "manual/luaran.xlsx", "manual/luaran.csv", "dosen.csv")


def sha_blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def pastikan_token():
    t = um.baca_token()
    if t:
        return t
    print("\nBelum ada token GitHub. Buat sekali (langkah lengkap di README, bagian")
    print("'Mini app unggah'): izin Contents = Read and write dan Actions = Read and write.")
    t = getpass.getpass("Tempel token di sini (tidak tampil di layar), lalu Enter: ").strip()
    kode, r = um.gh("GET", f"/repos/{REPO}", t)
    if kode == 0:
        sys.exit(f"Tidak bisa terhubung ke GitHub: {r.get('message')}. Ini bukan salah token; "
                 "cek internet, lalu jalankan lagi.")
    if kode != 200:
        sys.exit(f"Token ditolak GitHub ({r.get('message', kode)}). Periksa akses repo.")
    um.TOKEN_FILE.write_text(t)
    os.chmod(um.TOKEN_FILE, 0o600)
    print("Tersambung. Token tersimpan di komputer ini.")
    return t


def pohon_remote(t):
    kode, ref = um.gh("GET", f"/repos/{REPO}/git/ref/heads/{CABANG}", t)
    if kode != 200:
        sys.exit(f"Tidak bisa membaca cabang {CABANG} ({ref.get('message', kode)}).")
    head = ref["object"]["sha"]
    kode, komit = um.gh("GET", f"/repos/{REPO}/git/commits/{head}", t)
    kode, pohon = um.gh("GET", f"/repos/{REPO}/git/trees/{komit['tree']['sha']}?recursive=1", t)
    if kode != 200 or pohon.get("truncated"):
        sys.exit("Daftar berkas GitHub tidak terbaca lengkap.")
    return head, komit["tree"]["sha"], {e["path"]: e["sha"] for e in pohon["tree"] if e["type"] == "blob"}


def relevan(p):
    return any(p == d or (d.endswith("/") and p.startswith(d)) for d in DISINKRON)


def sinkron_dari_remote(t, remote):
    n = 0
    for p, sha in remote.items():
        if not relevan(p):
            continue
        f = ROOT / p
        if f.exists() and sha_blob(f.read_bytes()) == sha:
            continue
        kode, b = um.gh("GET", f"/repos/{REPO}/git/blobs/{sha}", t)
        if kode != 200:
            sys.exit(f"Gagal mengunduh {p} ({b.get('message', kode)}).")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(base64.b64decode(b["content"]))
        n += 1
    print(f"Folder lokal disamakan dengan GitHub ({n} berkas diperbarui).")


COOKIE_FILE = pathlib.Path.home() / ".dtntf-sinta-cookie"


def atur_cookie(args):
    """Cookie login SINTA (bukan kata sandi). Disimpan lokal, tidak dikirim ke GitHub."""
    if "--tanpa-cookie" in args:
        os.environ["SINTA_COOKIE"] = ""       # abaikan file cookie
        print("Mode tanpa login SINTA (10 entri terbaru per tab).")
        return
    if COOKIE_FILE.exists() and "--cookie-baru" not in args:
        print("Memakai cookie login SINTA yang tersimpan.")
        return
    print("\nOpsional: login SINTA supaya daftar luaran LENGKAP (bukan hanya 10 terbaru).")
    print("Login dulu di browser, lalu salin cookie (langkah di BACA-DULU.txt).")
    c = getpass.getpass("Tempel cookie (tidak tampil di layar), atau tekan Enter untuk lewati: ").strip()
    if c:
        COOKIE_FILE.write_text(c)
        os.chmod(COOKIE_FILE, 0o600)
        print("Cookie tersimpan di komputer ini.")
    else:
        print("Dilewati: mode tanpa login.")


def scrape(pilihan):
    # -u: tanpa penampung, supaya progres ([n/38]) langsung tampil di jendela.
    cmd = [sys.executable, "-u", str(ROOT / "scripts" / "build.py")] + ([pilihan] if pilihan else [])
    print("\nMengambil data dari SINTA. Jeda antar permintaan disengaja (sopan ke SINTA); mohon tunggu.\n")
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, bufsize=1, env=dict(os.environ, PYTHONUNBUFFERED="1"))
    isi = []
    for baris in p.stdout:
        print(baris, end="", flush=True)
        isi.append(baris)
    p.wait()
    teks = "".join(isi)
    ok = len(re.findall(r"✓ \d+ publikasi", teks))
    blok = teks.count("diblokir sementara")
    return p.returncode, ok, blok, teks


def kirim(t, head, base_tree, remote):
    lokal = {}
    for f in (ROOT / "data").rglob("*.json"):
        lokal[f.relative_to(ROOT).as_posix()] = f.read_bytes()
    entri, ubah, hapus = [], 0, 0
    for p, data in sorted(lokal.items()):
        if remote.get(p) == sha_blob(data):
            continue
        kode, b = um.gh("POST", f"/repos/{REPO}/git/blobs", t,
                        {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        if kode != 201:
            sys.exit(f"Gagal mengirim {p} ({b.get('message', kode)}).")
        entri.append({"path": p, "mode": "100644", "type": "blob", "sha": b["sha"]})
        ubah += 1
    for p in remote:  # berkas data yang sudah tidak ada lagi secara lokal
        if p.startswith("data/") and p not in lokal:
            entri.append({"path": p, "mode": "100644", "type": "blob", "sha": None})
            hapus += 1
    if not entri:
        print("\nTidak ada perubahan data untuk dikirim.")
        return False
    kode, pohon = um.gh("POST", f"/repos/{REPO}/git/trees", t, {"base_tree": base_tree, "tree": entri})
    if kode != 201:
        sys.exit(f"Gagal membuat commit ({pohon.get('message', kode)}).")
    kode, k = um.gh("POST", f"/repos/{REPO}/git/commits", t, {
        "message": "Perbarui data publikasi dari komputer lokal", "tree": pohon["sha"], "parents": [head]})
    if kode != 201:
        sys.exit(f"Gagal membuat commit ({k.get('message', kode)}).")
    kode, r = um.gh("PATCH", f"/repos/{REPO}/git/refs/heads/{CABANG}", t, {"sha": k["sha"]})
    if kode != 200:
        sys.exit(f"Gagal memperbarui {CABANG} ({r.get('message', kode)}). Coba jalankan lagi.")
    print(f"\nTerkirim ke GitHub: {ubah} berkas diubah/ditambah, {hapus} dihapus.")
    return True


def main():
    um.siapkan_ssl()
    args = [x for x in sys.argv[1:] if x.startswith("--")]
    pos = [x for x in sys.argv[1:] if not x.startswith("--")]
    arg = pos[0].strip() if pos else ""
    if not arg:
        print("Uji dulu 2 dosen (faridah, widya-rosita; ±6 menit) atau ambil SEMUA dosen (±30–60 menit)?")
        j = input("Tekan Enter untuk uji 2 dosen, atau ketik 'semua': ").strip().lower()
        arg = "semua" if j == "semua" else "faridah,widya-rosita"
    pilihan = "" if arg == "semua" else arg

    t = pastikan_token()
    head, base_tree, remote = pohon_remote(t)
    sinkron_dari_remote(t, remote)

    atur_cookie(args)
    kode, ok, blok, teks = scrape(pilihan)
    if "LOGIN_TIDAK_AKTIF" in teks and COOKIE_FILE.exists():
        COOKIE_FILE.unlink()
        print("\nCookie login tampak kedaluwarsa, jadi dihapus. Jalankan lagi untuk memasukkan cookie baru.")
    if kode != 0 or ok == 0:
        print("\nTidak ada dosen yang berhasil diambil, jadi tidak ada yang dikirim ke GitHub.")
        if blok:
            print("SINTA memblokir sementara (403). Tunggu ±1 jam lalu coba lagi, dan pastikan")
            print("komputer ini memakai internet Indonesia (matikan VPN).")
        return 1
    print(f"\n{ok} dosen berhasil diambil.")

    subprocess.run([sys.executable, str(ROOT / "scripts" / "manual.py")], cwd=ROOT, check=False)

    if kirim(t, head, base_tree, remote):
        kode, r = um.gh("POST", f"/repos/{REPO}/actions/workflows/manual.yml/dispatches", t, {"ref": CABANG})
        if kode == 204:
            print("Penerbitan ulang situs dijalankan; hasilnya tampil dalam ±1–2 menit.")
        else:
            print("Data sudah di GitHub, tapi penerbitan ulang belum bisa dipicu otomatis "
                  f"({r.get('message', kode)}).\nBuka GitHub → Actions → 'Perbarui data manual' → Run workflow.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
