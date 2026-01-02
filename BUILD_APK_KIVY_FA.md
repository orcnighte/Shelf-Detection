# راهنمای ساخت APK با Kivy و Buildozer

## ⚠️ نکته مهم
Buildozer روی Windows به صورت مستقیم کار نمی‌کند. نیاز به یکی از روش‌های زیر دارید:

## روش 1: استفاده از WSL (توصیه می‌شود)

### نصب WSL:
```powershell
# در PowerShell با دسترسی Administrator
wsl --install
```

### نصب Buildozer در WSL:
```bash
# در WSL Terminal
sudo apt-get update
sudo apt-get install -y python3-pip git unzip openjdk-17-jdk
pip3 install buildozer
```

### ساخت APK:
```bash
# در WSL Terminal
cd /mnt/c/Users/Farasoo/Desktop/inventory
buildozer android debug
```

APK در مسیر زیر ساخته می‌شود:
```
bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

---

## روش 2: استفاده از Docker

### نصب Docker Desktop:
از https://www.docker.com/products/docker-desktop دانلود کنید

### ساخت APK با Docker:
```powershell
# در PowerShell
cd C:\Users\Farasoo\Desktop\inventory
docker run -it --rm -v ${PWD}:/app kivy/buildozer buildozer android debug
```

---

## روش 3: استفاده از Linux VM یا Cloud

1. یک Linux VM (Ubuntu) ایجاد کنید
2. Buildozer را نصب کنید
3. پروژه را کپی کنید
4. APK را بسازید

---

## تنظیمات قبل از Build

### 1. تنظیم IP Backend:
فایل `mobile/main.py` را باز کنید و خط 15 را تغییر دهید:
```python
API_BASE_URL = "http://192.168.1.XXX:8000"  # IP کامپیوتر خود
```

### 2. بررسی buildozer.spec:
فایل `buildozer.spec` را بررسی کنید و در صورت نیاز تغییر دهید.

---

## دستورات Build

### Debug APK:
```bash
buildozer android debug
```

### Release APK (نیاز به keystore):
```bash
buildozer android release
```

### Clean و Build دوباره:
```bash
buildozer android clean
buildozer android debug
```

---

## مشکلات رایج

### مشکل 1: Buildozer پیدا نمی‌شود
```bash
# در WSL
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin
```

### مشکل 2: Android SDK پیدا نمی‌شود
Buildozer به صورت خودکار Android SDK و NDK را دانلود می‌کند.
اگر مشکل داشتید، دستی نصب کنید.

### مشکل 3: خطای Permission
```bash
chmod +x buildozer.spec
```

---

## نصب APK روی دستگاه

### با ADB:
```bash
adb install bin/inventoryapp-1.0.0-arm64-v8a-debug.apk
```

### دستی:
1. APK را به گوشی منتقل کنید
2. Settings → Security → Unknown Sources را فعال کنید
3. روی APK کلیک کنید و نصب کنید

---

## 🎯 خلاصه سریع (WSL)

```bash
# 1. نصب WSL (در PowerShell با Admin)
wsl --install

# 2. در WSL Terminal
sudo apt-get update
sudo apt-get install -y python3-pip git unzip openjdk-17-jdk
pip3 install buildozer

# 3. ساخت APK
cd /mnt/c/Users/Farasoo/Desktop/inventory
buildozer android debug

# 4. APK در bin/ ساخته می‌شود
```

---

**موفق باشید! 🚀**



