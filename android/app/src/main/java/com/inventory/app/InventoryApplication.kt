package com.inventory.app

import android.app.Application

class InventoryApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        // Initialize WorkManager for daily capture
        WorkManagerInitializer.scheduleDailyCapture(this)
    }
}




