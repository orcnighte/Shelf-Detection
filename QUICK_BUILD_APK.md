# ساخت APK - راهنمای سریع

## روش ساده (با Android Studio):

1. **Android Studio را باز کنید**
2. **File → Open** → پوشه `android` را انتخاب کنید
3. صبر کنید تا Gradle sync شود
4. **Build → Build Bundle(s) / APK(s) → Build APK(s)**
5. APK در مسیر زیر ساخته می‌شود:
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

## قبل از Build:

### 1. تنظیم IP در InventoryRepository.kt:
```kotlin
// خط 23 را پیدا کنید و IP کامپیوتر خود را بگذارید
private val baseUrl = "http://192.168.1.XXX:8000/"
```

### 2. پیدا کردن IP کامپیوتر:
```cmd
ipconfig
```
IPv4 Address را پیدا کنید

### 3. Backend باید در حال اجرا باشد:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## نصب APK روی گوشی:

1. APK را به گوشی منتقل کنید
2. Settings → Security → Unknown Sources را فعال کنید
3. روی APK کلیک کنید و نصب کنید

---

**فایل راهنمای کامل: BUILD_APK_GUIDE_FA.md**



