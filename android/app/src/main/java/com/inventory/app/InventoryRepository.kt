package com.inventory.app

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.io.File
import java.time.LocalDate

interface InventoryApiService {
    @Multipart
    @POST("api/v1/images/upload")
    suspend fun uploadImage(
        @Part file: MultipartBody.Part
    ): ImageUploadResponse

    @GET("api/v1/analytics/daily")
    suspend fun getDailySummary(
        @Query("target_date") date: LocalDate? = null
    ): DailySummaryResponse

    @GET("api/v1/analytics/weekly")
    suspend fun getWeeklyAnalytics(
        @Query("days") days: Int = 7
    ): WeeklyAnalyticsResponse

    @GET("api/v1/recommendations/weekly")
    suspend fun getWeeklyRecommendations(
        @Query("days") days: Int = 7
    ): RecommendationsResponse
}

class InventoryRepository {
    // برای تست روی دستگاه واقعی، IP کامپیوتر خود را اینجا بگذارید
    // برای پیدا کردن IP: در CMD بنویسید: ipconfig
    // برای Emulator: http://10.0.2.2:8000/
    private val baseUrl = "http://192.168.1.100:8000/" // TODO: IP خود را تغییر دهید

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val client = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(baseUrl)
        .client(client)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val apiService = retrofit.create(InventoryApiService::class.java)

    suspend fun uploadImage(imageFile: File): ImageUploadResponse {
        val requestFile = imageFile.asRequestBody("image/jpeg".toMediaType())
        val body = MultipartBody.Part.createFormData("file", imageFile.name, requestFile)
        return apiService.uploadImage(body)
    }

    suspend fun getDailySummary(date: LocalDate?): DailySummaryResponse {
        return apiService.getDailySummary(date)
    }

    suspend fun getWeeklyAnalytics(days: Int = 7): WeeklyAnalyticsResponse {
        return apiService.getWeeklyAnalytics(days)
    }

    suspend fun getWeeklyRecommendations(days: Int = 7): RecommendationsResponse {
        return apiService.getWeeklyRecommendations(days)
    }
}

// Data classes matching backend schemas
data class ImageUploadResponse(
    val image_id: Int,
    val detections: List<DetectionResult>,
    val total_products: Int,
    val processing_time: Double
)

data class DetectionResult(
    val product_name: String,
    val count: Int,
    val confidence: Double
)

data class DailySummaryResponse(
    val date: String,
    val total_products: Int,
    val total_items: Int,
    val products: List<ProductCount>
)

data class ProductCount(
    val product_id: Int,
    val product_name: String,
    val count: Int
)

data class WeeklyAnalyticsResponse(
    val start_date: String,
    val end_date: String,
    val products: List<AnalyticsSummary>
)

data class AnalyticsSummary(
    val product_id: Int,
    val product_name: String,
    val average_daily_demand: Double,
    val growth_rate: Double,
    val demand_consistency: Double,
    val total_count: Int,
    val days_analyzed: Int
)

data class RecommendationsResponse(
    val week_start: String,
    val week_end: String,
    val recommendations: List<RecommendationItem>,
    val generated_at: String
)

data class RecommendationItem(
    val product_id: Int,
    val product_name: String,
    val category: String?,
    val score: Double,
    val explanation: String,
    val metrics: Map<String, Double>
)


