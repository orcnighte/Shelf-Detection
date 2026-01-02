# راهنمای ساخت APK - MVP

## روش 1: ساخت APK با Android Studio (ساده‌ترین روش)

### مرحله 1: باز کردن پروژه
1. Android Studio را باز کنید
2. **File → Open**
3. پوشه `android` را انتخاب کنید (نه `android/app`)
4. صبر کنید تا Gradle sync شود

### مرحله 2: تنظیم API Endpoint
1. فایل `app/src/main/java/com/inventory/app/InventoryRepository.kt` را باز کنید
2. خط 23 را پیدا کنید
3. IP کامپیوتر خود را بگذارید:
   ```kotlin
   private val baseUrl = "http://192.168.1.XXX:8000/" // IP خود را بگذارید
   ```
4. برای پیدا کردن IP: در CMD بنویسید `ipconfig` و IPv4 Address را پیدا کنید

### مرحله 3: ساخت APK
1. در Android Studio: **Build → Build Bundle(s) / APK(s) → Build APK(s)**
2. صبر کنید تا build تمام شود
3. وقتی تمام شد، روی **locate** کلیک کنید
4. APK در مسیر زیر است:
   ```
   android/app/build/outputs/apk/debug/app-debug.apk
   ```

### مرحله 4: نصب روی دستگاه
1. APK را به گوشی خود منتقل کنید (با USB یا Bluetooth)
2. روی گوشی: **Settings → Security → Unknown Sources** را فعال کنید
3. روی فایل APK کلیک کنید و نصب کنید

---

## روش 2: ساخت APK با Command Line

### پیش‌نیاز:
- Android Studio نصب باشد (برای Android SDK)
- JAVA_HOME تنظیم شده باشد

### دستورات:

```powershell
# 1. رفتن به پوشه android
cd C:\Users\Farasoo\Desktop\inventory\android

# 2. ساخت APK Debug
.\gradlew.bat assembleDebug

# یا برای Release (نیاز به keystore دارد):
# .\gradlew.bat assembleRelease
```

APK در مسیر زیر ساخته می‌شود:
```
android/app/build/outputs/apk/debug/app-debug.apk
```

---

## روش 3: استفاده از Android Studio Terminal

1. Android Studio را باز کنید
2. پروژه را باز کنید
3. **View → Tool Windows → Terminal** را باز کنید
4. دستورات زیر را اجرا کنید:

```bash
./gradlew assembleDebug
```

---

## ⚠️ نکات مهم

### 1. تنظیم IP برای تست روی دستگاه واقعی:
- کامپیوتر و گوشی باید در یک شبکه WiFi باشند
- IP کامپیوتر را در `InventoryRepository.kt` بگذارید
- Firewall Windows را موقتاً غیرفعال کنید یا port 8000 را باز کنید

### 2. Backend باید در حال اجرا باشد:
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. اگر خطا گرفتید:
- **Gradle Sync**: File → Sync Project with Gradle Files
- **Invalidate Caches**: File → Invalidate Caches → Restart
- **Clean Project**: Build → Clean Project

---

## 📱 تست APK

### روی Emulator:
1. Emulator را در Android Studio اجرا کنید
2. APK را drag & drop کنید روی Emulator
3. یا از ADB استفاده کنید:
   ```bash
   adb install app-debug.apk
   ```

### روی دستگاه واقعی:
1. USB Debugging را فعال کنید (Settings → Developer Options)
2. گوشی را به کامپیوتر وصل کنید
3. از ADB استفاده کنید:
   ```bash
   adb install app-debug.apk
   ```
4. یا APK را به گوشی منتقل کنید و دستی نصب کنید

---

## 🎯 چک‌لیست قبل از Build

- [ ] Android Studio نصب است
- [ ] پروژه در Android Studio باز است
- [ ] Gradle sync موفق بوده
- [ ] API endpoint در `InventoryRepository.kt` تنظیم شده
- [ ] Backend در حال اجرا است
- [ ] IP کامپیوتر درست است

---

## 🚀 دستور سریع (اگر Gradle wrapper کار کند)

```powershell
cd C:\Users\Farasoo\Desktop\inventory\android
.\gradlew.bat assembleDebug
```

APK در: `app\build\outputs\apk\debug\app-debug.apk`

**موفق باشید! 🎉**



