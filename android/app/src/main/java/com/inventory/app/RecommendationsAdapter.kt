package com.inventory.app

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView

class RecommendationsAdapter : ListAdapter<RecommendationItem, RecommendationsAdapter.ViewHolder>(DiffCallback()) {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val productName: TextView = view.findViewById(R.id.productName)
        val score: TextView = view.findViewById(R.id.score)
        val explanation: TextView = view.findViewById(R.id.explanation)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_recommendation, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = getItem(position)
        holder.productName.text = item.product_name
        holder.score.text = "Score: ${String.format("%.2f", item.score)}"
        holder.explanation.text = item.explanation
    }

    class DiffCallback : DiffUtil.ItemCallback<RecommendationItem>() {
        override fun areItemsTheSame(oldItem: RecommendationItem, newItem: RecommendationItem): Boolean {
            return oldItem.product_id == newItem.product_id
        }

        override fun areContentsTheSame(oldItem: RecommendationItem, newItem: RecommendationItem): Boolean {
            return oldItem == newItem
        }
    }
}




