package com.inventory.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class RecommendationsViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = InventoryRepository()

    private val _recommendations = MutableLiveData<RecommendationsResponse>()
    val recommendations: LiveData<RecommendationsResponse> = _recommendations

    fun loadRecommendations(days: Int = 7) {
        viewModelScope.launch {
            try {
                val recs = repository.getWeeklyRecommendations(days)
                _recommendations.value = recs
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}




