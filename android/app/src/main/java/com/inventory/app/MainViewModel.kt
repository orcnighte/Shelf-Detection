package com.inventory.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import java.io.File

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = InventoryRepository()

    private val _dailyCounts = MutableLiveData<List<DailyCount>>()
    val dailyCounts: LiveData<List<DailyCount>> = _dailyCounts

    private val _uploadStatus = MutableLiveData<String>()
    val uploadStatus: LiveData<String> = _uploadStatus

    init {
        loadDailyCounts()
    }

    fun uploadImage(imageFile: File) {
        viewModelScope.launch {
            try {
                val response = repository.uploadImage(imageFile)
                _uploadStatus.value = "Upload successful: ${response.totalProducts} products detected"
                loadDailyCounts()
            } catch (e: Exception) {
                _uploadStatus.value = "Upload failed: ${e.message}"
            }
        }
    }

    fun loadDailyCounts() {
        viewModelScope.launch {
            try {
                val today = java.time.LocalDate.now()
                val counts = repository.getDailySummary(today)
                _dailyCounts.value = counts.products.map {
                    DailyCount(it.productName, it.count)
                }
            } catch (e: Exception) {
                _uploadStatus.value = "Failed to load counts: ${e.message}"
            }
        }
    }
}

data class DailyCount(val productName: String, val count: Int)




