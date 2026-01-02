# اسکریپت PowerShell برای ساخت APK
# استفاده: .\build_apk.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ساخت APK برای Inventory App" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# بررسی وجود Android Studio
$androidStudioPath = "$env:LOCALAPPDATA\Android\Sdk"
if (-not (Test-Path $androidStudioPath)) {
    Write-Host "⚠️  Android SDK پیدا نشد!" -ForegroundColor Yellow
    Write-Host "لطفاً Android Studio را نصب کنید" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "یا از Android Studio استفاده کنید:" -ForegroundColor Green
    Write-Host "Build → Build Bundle(s) / APK(s) → Build APK(s)" -ForegroundColor Green
    exit 1
}

# رفتن به پوشه android
$androidPath = Join-Path $PSScriptRoot "android"
if (-not (Test-Path $androidPath)) {
    Write-Host "❌ پوشه android پیدا نشد!" -ForegroundColor Red
    exit 1
}

Set-Location $androidPath
Write-Host "📁 پوشه: $androidPath" -ForegroundColor Green

# بررسی Gradle wrapper
if (Test-Path "gradlew.bat") {
    Write-Host "✅ Gradle wrapper پیدا شد" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔨 در حال ساخت APK..." -ForegroundColor Cyan
    
    try {
        .\gradlew.bat assembleDebug
        if ($LASTEXITCODE -eq 0) {
            $apkPath = "app\build\outputs\apk\debug\app-debug.apk"
            if (Test-Path $apkPath) {
                Write-Host ""
                Write-Host "✅ APK با موفقیت ساخته شد!" -ForegroundColor Green
                Write-Host "📍 مسیر: $((Get-Item $apkPath).FullName)" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "برای نصب روی دستگاه:" -ForegroundColor Yellow
                Write-Host "  adb install $apkPath" -ForegroundColor White
            } else {
                Write-Host "⚠️  APK ساخته نشد!" -ForegroundColor Yellow
            }
        } else {
            Write-Host "❌ خطا در ساخت APK!" -ForegroundColor Red
            Write-Host "لطفاً از Android Studio استفاده کنید" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ خطا: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 راه حل: از Android Studio استفاده کنید:" -ForegroundColor Green
        Write-Host "   Build → Build Bundle(s) / APK(s) → Build APK(s)" -ForegroundColor White
    }
} else {
    Write-Host "⚠️  Gradle wrapper پیدا نشد!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 لطفاً از Android Studio استفاده کنید:" -ForegroundColor Green
    Write-Host "   1. Android Studio را باز کنید" -ForegroundColor White
    Write-Host "   2. پروژه android را باز کنید" -ForegroundColor White
    Write-Host "   3. Build → Build Bundle(s) / APK(s) → Build APK(s)" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan



