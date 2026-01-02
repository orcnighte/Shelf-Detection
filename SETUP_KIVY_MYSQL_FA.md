# راهنمای کامل - Kivy + MySQL

## ✅ تغییرات انجام شده:

1. ✅ **دیتابیس به MySQL تغییر کرد**
2. ✅ **اپلیکیشن Kivy ساخته شد** (به جای Android Kotlin)
3. ✅ **فایل buildozer.spec آماده است**

---

## 🚀 راه‌اندازی Backend (MySQL)

### 1. نصب MySQL:
- دانلود از: https://dev.mysql.com/downloads/mysql/
- یا از XAMPP استفاده کنید (شامل MySQL است)

### 2. ایجاد دیتابیس:
```sql
CREATE DATABASE inventory_db;
```

### 3. تنظیم Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. تنظیم .env:
فایل `.env` در پوشه `backend` ایجاد کنید:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/inventory_db
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=storage/images
MODEL_PATH=models/yolov8_inventory.onnx
```

### 5. اجرای Backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📱 ساخت APK با Buildozer

### روش 1: استفاده از WSL (توصیه می‌شود)

#### مرحله 1: باز کردن WSL Terminal
- Windows Terminal را باز کنید
- یا در PowerShell: `wsl`

#### مرحله 2: نصب Buildozer
```bash
sudo apt-get update
sudo apt-get install -y python3-pip git unzip openjdk-17-jdk
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin
```

#### مرحله 3: رفتن به پوشه پروژه
```bash
cd /mnt/c/Users/Farasoo/Desktop/inventory
```

#### مرحله 4: تنظیم IP Backend
فایل `mobile/main.py` را ویرایش کنید (خط 15):
```python
API_BASE_URL = "http://192.168.1.XXX:8000"  # IP کامپیوتر خود
```

#### مرحله 5: ساخت APK
```bash
buildozer android debug
```

این کار ممکن است 10-30 دقیقه طول بکشد (اولین بار).

#### مرحله 6: پیدا کردن APK
APK در مسیر زیر ساخته می‌شود:
```
bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

---

### روش 2: استفاده از Docker

```powershell
cd C:\Users\Farasoo\Desktop\inventory
docker run -it --rm -v ${PWD}:/app kivy/buildozer buildozer android debug
```

---

## 📲 نصب APK روی گوشی

### روش 1: با ADB
```bash
adb install bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

### روش 2: دستی
1. APK را به گوشی منتقل کنید (USB یا Bluetooth)
2. Settings → Security → Unknown Sources را فعال کنید
3. روی APK کلیک کنید و نصب کنید

---

## ⚙️ تنظیمات مهم

### 1. IP Backend:
- کامپیوتر و گوشی باید در یک شبکه WiFi باشند
- IP کامپیوتر را در `mobile/main.py` بگذارید
- برای پیدا کردن IP: `ipconfig` در CMD

### 2. Firewall:
- Firewall Windows را موقتاً غیرفعال کنید
- یا port 8000 را در Firewall باز کنید

### 3. Backend باید در حال اجرا باشد:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎯 دستورات سریع

### Backend:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ساخت APK (در WSL):
```bash
cd /mnt/c/Users/Farasoo/Desktop/inventory
buildozer android debug
```

### Clean و Build دوباره:
```bash
buildozer android clean
buildozer android debug
```

---

## ⚠️ مشکلات رایج

### مشکل 1: Buildozer پیدا نمی‌شود
```bash
export PATH=$PATH:~/.local/bin
# یا
~/.local/bin/buildozer android debug
```

### مشکل 2: Android SDK پیدا نمی‌شود
Buildozer به صورت خودکار دانلود می‌کند. صبر کنید.

### مشکل 3: خطای Connection در App
- IP Backend را بررسی کنید
- Backend در حال اجرا است؟
- Firewall را بررسی کنید

---

## 📁 ساختار پروژه

```
inventory/
├── backend/          # FastAPI + MySQL
│   ├── app/
│   └── requirements.txt
├── mobile/           # Kivy App
│   ├── main.py
│   └── requirements.txt
├── model/            # YOLO Training
├── buildozer.spec    # Buildozer config
└── README.md
```

---

## ✅ چک‌لیست نهایی

- [ ] MySQL نصب و دیتابیس ایجاد شده
- [ ] Backend در حال اجرا است
- [ ] IP Backend در mobile/main.py تنظیم شده
- [ ] Buildozer در WSL نصب شده
- [ ] APK ساخته شده
- [ ] APK روی گوشی نصب شده

---

**موفق باشید! 🚀**



