#!/bin/bash
# Klik dua kali (Mac). Mengambil data SINTA dari komputer ini lalu mengirimnya ke GitHub.
cd "$(dirname "$0")"
python3 scripts/perbarui_lokal.py
echo
read -n 1 -s -r -p "Selesai. Tekan tombol apa saja untuk menutup jendela ini."
