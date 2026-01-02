# Django Backend - راهنمای راه‌اندازی

## نصب و راه‌اندازی

### 1. نصب Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### 2. تنظیم دیتابیس MySQL:
فایل `.env` در پوشه `backend` ایجاد کنید:
```env
DB_NAME=inventory_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

یا در `settings.py` مستقیماً تنظیم کنید.

### 3. ایجاد Migration ها:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. ایجاد Superuser (اختیاری):
```bash
python manage.py createsuperuser
```

### 5. اجرای سرور:
```bash
python manage.py runserver 0.0.0.0:8000
```

## API Endpoints

همه endpoints در `/api/v1/` هستند:

- `POST /api/v1/images/upload` - آپلود تصویر
- `GET /api/v1/images` - لیست تصاویر
- `GET /api/v1/products` - لیست محصولات
- `POST /api/v1/products` - ایجاد محصول
- `GET /api/v1/products/{id}/counts` - تعداد روزانه محصول
- `GET /api/v1/analytics/weekly` - آنالیتیکس هفتگی
- `GET /api/v1/analytics/daily` - خلاصه روزانه
- `GET /api/v1/recommendations/weekly` - توصیه‌های هفتگی

## Admin Panel

بعد از ایجاد superuser:
```
http://localhost:8000/admin
```

## تست API

```bash
# Health check
curl http://localhost:8000/api/v1/products

# Upload image
curl -X POST -F "file=@image.jpg" http://localhost:8000/api/v1/images/upload
```



