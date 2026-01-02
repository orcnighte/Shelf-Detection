package com.inventory.app

import android.content.Context
import androidx.work.*
import java.util.concurrent.TimeUnit

object WorkManagerInitializer {
    fun scheduleDailyCapture(context: Context) {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()

        val dailyWorkRequest = PeriodicWorkRequestBuilder<DailyCaptureWorker>(
            1, TimeUnit.DAYS
        )
            .setConstraints(constraints)
            .setInitialDelay(1, TimeUnit.HOURS) // Start after 1 hour
            .addTag("daily_capture")
            .build()

        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            "daily_capture_work",
            ExistingPeriodicWorkPolicy.KEEP,
            dailyWorkRequest
        )
    }
}




