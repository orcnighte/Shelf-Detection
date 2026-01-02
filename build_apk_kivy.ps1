# اسکریپت ساخت APK با Buildozer
# نیاز به: Python, Buildozer, Android SDK, NDK

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ساخت APK با Buildozer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# بررسی Buildozer
$buildozerInstalled = pip show buildozer 2>$null
if (-not $buildozerInstalled) {
    Write-Host "⚠️  Buildozer نصب نیست!" -ForegroundColor Yellow
    Write-Host "در حال نصب Buildozer..." -ForegroundColor Green
    pip install buildozer
}

# بررسی فایل buildozer.spec
if (-not (Test-Path "buildozer.spec")) {
    Write-Host "❌ فایل buildozer.spec پیدا نشد!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Buildozer آماده است" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  توجه: ساخت APK روی Windows نیاز به WSL یا Docker دارد" -ForegroundColor Yellow
Write-Host ""
Write-Host "گزینه 1: استفاده از WSL (Windows Subsystem for Linux)" -ForegroundColor Cyan
Write-Host "  wsl buildozer android debug" -ForegroundColor White
Write-Host ""
Write-Host "گزینه 2: استفاده از Docker" -ForegroundColor Cyan
Write-Host "  docker run -it -v %cd%:/app kivy/buildozer buildozer android debug" -ForegroundColor White
Write-Host ""
Write-Host "گزینه 3: استفاده از Linux VM یا Cloud" -ForegroundColor Cyan
Write-Host ""

# تلاش برای ساخت (اگر در WSL هستیم)
if ($env:WSL_DISTRO_NAME) {
    Write-Host "🔨 در حال ساخت APK در WSL..." -ForegroundColor Green
    wsl buildozer android debug
} else {
    Write-Host "💡 برای ساخت APK:" -ForegroundColor Yellow
    Write-Host "   1. WSL را نصب کنید (Windows Subsystem for Linux)" -ForegroundColor White
    Write-Host "   2. در WSL: sudo apt-get update && sudo apt-get install -y buildozer" -ForegroundColor White
    Write-Host "   3. در WSL: buildozer android debug" -ForegroundColor White
}



