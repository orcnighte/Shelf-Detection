[app]

# (str) Title of your application
title = Inventory Manager

# (str) Package name
package.name = inventoryapp

# (str) Package domain (needed for android/ios packaging)
package.domain = com.inventory

# (str) Source code where the main.py live
source.dir = mobile

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.2.0,plyer,requests,Pillow,pyjnius

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (str) The Android permission to write to external storage
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True
