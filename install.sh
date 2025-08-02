#!/data/data/com.termux/files/usr/bin/bash
# Telegram botlar boshqaruvi uchun o‘rnatish skripti
# Muallif: @originalprofil

echo "📦 Termux muhiti tayyorlanmoqda..."

# Python va pip o‘rnatish (Termux uchun)
pkg update -y && pkg upgrade -y
pkg install -y python git
pkg install -y python git
pip install --upgrade pip

# pipni yangilash
pip install --upgrade pip

# Telethon kutubxonasini o‘rnatish
pip install -r requirements.txt

echo "✅ O‘rnatish tugadi. Endi quyidagilarni bajaring:"
echo "👉 python admin_bot_manager.py"
