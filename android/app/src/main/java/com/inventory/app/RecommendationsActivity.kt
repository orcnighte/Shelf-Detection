package com.inventory.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.inventory.app.databinding.ActivityRecommendationsBinding

class RecommendationsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityRecommendationsBinding
    private lateinit var viewModel: RecommendationsViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRecommendationsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        viewModel = ViewModelProvider(this)[RecommendationsViewModel::class.java]

        // Set up RecyclerView
        val adapter = RecommendationsAdapter()
        binding.recommendationsRecyclerView.layoutManager = LinearLayoutManager(this)
        binding.recommendationsRecyclerView.adapter = adapter

        // Observe recommendations
        viewModel.recommendations.observe(this) { recommendations ->
            adapter.submitList(recommendations.recommendations)
        }

        // Load recommendations
        viewModel.loadRecommendations()
    }
}




