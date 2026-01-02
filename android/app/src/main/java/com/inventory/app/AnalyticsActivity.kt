package com.inventory.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.inventory.app.databinding.ActivityAnalyticsBinding

class AnalyticsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityAnalyticsBinding
    private lateinit var viewModel: AnalyticsViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAnalyticsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        viewModel = ViewModelProvider(this)[AnalyticsViewModel::class.java]

        // Observe analytics data
        viewModel.weeklyAnalytics.observe(this) { analytics ->
            displayAnalytics(analytics)
            updateCharts(analytics)
        }

        // Load analytics
        viewModel.loadWeeklyAnalytics()
    }

    private fun displayAnalytics(analytics: WeeklyAnalyticsResponse) {
        val text = analytics.products.joinToString("\n\n") { product ->
            """
            ${product.product_name}:
            - Average Daily Demand: ${String.format("%.2f", product.average_daily_demand)}
            - Growth Rate: ${String.format("%.2f", product.growth_rate)}%
            - Consistency: ${String.format("%.2f", product.demand_consistency)}%
            - Total Count: ${product.total_count}
            """.trimIndent()
        }
        binding.analyticsText.text = text
    }

    private fun updateCharts(analytics: WeeklyAnalyticsResponse) {
        // Create line chart for growth rates
        val growthEntries = analytics.products.mapIndexed { index, product ->
            Entry(index.toFloat(), product.growth_rate.toFloat())
        }
        
        val growthDataSet = LineDataSet(growthEntries, "Growth Rate (%)")
        growthDataSet.color = android.graphics.Color.BLUE
        growthDataSet.valueTextColor = android.graphics.Color.BLACK
        
        val lineData = LineData(growthDataSet)
        binding.growthChart.data = lineData
        binding.growthChart.description.text = "Product Growth Rates"
        binding.growthChart.invalidate()
    }
}




