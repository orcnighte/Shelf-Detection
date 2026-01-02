# راهنمای سریع - 5 دقیقه تا اجرا

## ⚡ دستورات سریع (Windows)

### 1️⃣ راه‌اندازی دیتابیس
```bash
# PostgreSQL باید نصب و در حال اجرا باشد
# دیتابیس را ایجاد کنید:
psql -U postgres
CREATE DATABASE inventory_db;
\q
```

### 2️⃣ راه‌اندازی Backend
```bash
# در PowerShell یا CMD
cd C:\Users\Farasoo\Desktop\inventory

# ایجاد محیط مجازی
python -m venv venv
venv\Scripts\activate

# نصب dependencies
cd backend
pip install -r requirements.txt

# ایجاد پوشه‌ها
mkdir storage\images
mkdir models

# ایجاد فایل .env (با Notepad یا VS Code)
# محتویات:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventory_db
# STORAGE_TYPE=local
# LOCAL_STORAGE_PATH=storage/images
# MODEL_PATH=models/yolov8_inventory.onnx

# اجرا
uvicorn app.main:app --reload
```

### 3️⃣ باز کردن Android Studio
1. Android Studio را باز کنید
2. **Open** → پوشه `android` را انتخاب کنید
3. صبر کنید تا Gradle sync شود
4. فایل `InventoryRepository.kt` را باز کنید
5. خط 23 را به `http://10.0.2.2:8000/` تغییر دهید (برای Emulator)
6. **Run** (▶) را بزنید

---

## ✅ چک کردن که همه چیز کار می‌کند

### Backend:
- مرورگر: http://localhost:8000/docs
- باید صفحه Swagger UI را ببینید

### Android:
- App باید باز شود
- دوربین باید کار کند
- دکمه Capture را بزنید

---

## 🎯 ترتیب اجرا (یک خطی)

```
PostgreSQL → Backend (uvicorn) → Android Studio → Run App
```

**همه چیز آماده است! 🎉**




