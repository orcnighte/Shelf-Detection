package com.inventory.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class AnalyticsViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = InventoryRepository()

    private val _weeklyAnalytics = MutableLiveData<WeeklyAnalyticsResponse>()
    val weeklyAnalytics: LiveData<WeeklyAnalyticsResponse> = _weeklyAnalytics

    fun loadWeeklyAnalytics(days: Int = 7) {
        viewModelScope.launch {
            try {
                val analytics = repository.getWeeklyAnalytics(days)
                _weeklyAnalytics.value = analytics
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}




