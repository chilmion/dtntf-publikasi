#!/usr/bin/env bash
# Runner untuk cron di mini PC / server lokal.
#   crontab -e
#   0 2 * * 1  /path/ke/dtntf-profil/jalankan.sh >> /path/ke/dtntf-profil/log.txt 2>&1
# (Senin 02:00 WIB — di luar jam sibuk SINTA.)

set -euo pipefail
cd "$(dirname "$0")"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') mulai ==="

# Ambil data. Kalau scraping gagal total, JSON lama tetap utuh.
python3 scripts/build.py

# Push ke GitHub hanya kalau ada perubahan.
if [[ -n "$(git status --porcelain data/)" ]]; then
  git add data/
  git commit -m "Perbarui data publikasi $(date '+%Y-%m-%d')"
  git push
  echo "→ perubahan dikirim ke GitHub"
else
  echo "→ tidak ada perubahan"
fi

echo "=== selesai ==="
