# راهنمای کامل - Django + Kivy + MySQL

## ✅ تغییرات انجام شده:

1. ✅ **Backend به Django تبدیل شد** (به جای FastAPI)
2. ✅ **دیتابیس MySQL** (به جای PostgreSQL)
3. ✅ **اپلیکیشن Kivy** برای موبایل
4. ✅ **همه API endpoints حفظ شدند**

---

## 🚀 راه‌اندازی Backend (Django)

### 1. نصب MySQL:
- دانلود از: https://dev.mysql.com/downloads/mysql/
- یا از XAMPP استفاده کنید

### 2. ایجاد دیتابیس:
```sql
CREATE DATABASE inventory_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. نصب Dependencies:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**نکته:** اگر `mysqlclient` نصب نشد، از `pymysql` استفاده کنید:
```bash
pip install pymysql
```
و در `settings.py` اضافه کنید:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 4. تنظیم Settings:
در `backend/inventory_project/settings.py` یا فایل `.env`:
```env
DB_NAME=inventory_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Migration ها:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. ایجاد Superuser (اختیاری):
```bash
python manage.py createsuperuser
```

### 7. اجرای سرور:
```bash
python manage.py runserver 0.0.0.0:8000
```

**✅ اگر موفق بود:**
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin

---

## 📱 ساخت APK با Kivy

### تنظیم IP Backend:
فایل `mobile/main.py` را باز کنید (خط 15):
```python
API_BASE_URL = "http://192.168.1.XXX:8000"  # IP کامپیوتر خود
```

### ساخت APK (در WSL):
```bash
# در WSL Terminal
cd /mnt/c/Users/Farasoo/Desktop/inventory

# نصب Buildozer (اگر نصب نیست)
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin

# ساخت APK
buildozer android debug
```

APK در مسیر زیر ساخته می‌شود:
```
bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

---

## 🔌 API Endpoints

همه endpoints در `/api/v1/` هستند:

### Images:
- `POST /api/v1/images/upload` - آپلود تصویر
- `GET /api/v1/images` - لیست تصاویر

### Products:
- `GET /api/v1/products` - لیست محصولات
- `POST /api/v1/products` - ایجاد محصول
- `GET /api/v1/products/{id}/counts` - تعداد روزانه

### Analytics:
- `GET /api/v1/analytics/weekly?days=7` - آنالیتیکس هفتگی
- `GET /api/v1/analytics/daily?target_date=2024-01-01` - خلاصه روزانه

### Recommendations:
- `GET /api/v1/recommendations/weekly?days=7` - توصیه‌های هفتگی

---

## 🧪 تست API

### با curl:
```bash
# لیست محصولات
curl http://localhost:8000/api/v1/products

# آپلود تصویر
curl -X POST -F "file=@image.jpg" http://localhost:8000/api/v1/images/upload

# آنالیتیکس
curl http://localhost:8000/api/v1/analytics/weekly?days=7
```

### با Postman یا Browser:
- http://localhost:8000/api/v1/products
- http://localhost:8000/api/v1/analytics/weekly

---

## 📁 ساختار پروژه

```
inventory/
├── backend/                    # Django Backend
│   ├── inventory_project/     # Django settings
│   ├── inventory_app/         # Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   ├── serializers.py     # DRF serializers
│   │   └── services.py        # Business logic
│   ├── manage.py
│   └── requirements.txt
├── mobile/                     # Kivy App
│   ├── main.py
│   └── requirements.txt
└── buildozer.spec              # Buildozer config
```

---

## ⚠️ مشکلات رایج

### مشکل 1: mysqlclient نصب نمی‌شود
**راه حل:**
```bash
# Windows: از pymysql استفاده کنید
pip install pymysql

# در settings.py یا __init__.py اضافه کنید:
import pymysql
pymysql.install_as_MySQLdb()
```

### مشکل 2: Migration خطا می‌دهد
```bash
# دیتابیس را بررسی کنید
# مطمئن شوید که دیتابیس ایجاد شده است
python manage.py showmigrations
```

### مشکل 3: CORS Error
در `settings.py` بررسی کنید:
```python
CORS_ALLOW_ALL_ORIGINS = True  # برای development
```

### مشکل 4: Connection Error در App
- IP Backend را بررسی کنید
- Backend در حال اجرا است؟
- Firewall را بررسی کنید

---

## 🎯 دستورات سریع

### Backend:
```bash
cd backend
venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

### Migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

### ساخت APK:
```bash
# در WSL
cd /mnt/c/Users/Farasoo/Desktop/inventory
buildozer android debug
```

---

## ✅ چک‌لیست نهایی

- [ ] MySQL نصب و دیتابیس ایجاد شده
- [ ] Dependencies نصب شده
- [ ] Migration ها اجرا شده
- [ ] Backend در حال اجرا است (http://localhost:8000)
- [ ] IP Backend در mobile/main.py تنظیم شده
- [ ] Buildozer نصب شده
- [ ] APK ساخته شده
- [ ] APK روی گوشی نصب شده

---

**موفق باشید! 🚀**



