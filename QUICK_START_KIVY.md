# راهنمای سریع - Kivy + MySQL

## 1. راه‌اندازی Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# ایجاد فایل .env با محتوا:
# DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/inventory_db

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 2. ساخت APK (در WSL):

```bash
# در WSL Terminal
sudo apt-get update
sudo apt-get install -y python3-pip git unzip openjdk-17-jdk
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin

cd /mnt/c/Users/Farasoo/Desktop/inventory

# تنظیم IP در mobile/main.py (خط 15)
# API_BASE_URL = "http://192.168.1.XXX:8000"

buildozer android debug
```

## 3. APK در:
```
bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

## 4. نصب:
```bash
adb install bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

---

**فایل راهنمای کامل: SETUP_KIVY_MYSQL_FA.md**



