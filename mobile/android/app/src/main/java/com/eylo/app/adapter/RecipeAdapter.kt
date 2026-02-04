package com.eylo.app.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.eylo.app.R
import com.eylo.app.models.Recipe

class RecipeAdapter(
    private var recipes: List<Recipe>,
    private val onClick: (Recipe) -> Unit
) : RecyclerView.Adapter<RecipeAdapter.RecipeViewHolder>() {

    class RecipeViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvTitle: TextView = view.findViewById(R.id.tvTitle)
        val tvPrepTime: TextView = view.findViewById(R.id.tvPrepTime)
        val tvCookTime: TextView = view.findViewById(R.id.tvCookTime)
        val ivThumbnail: ImageView = view.findViewById(R.id.ivThumbnail)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecipeViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_recipe, parent, false)
        return RecipeViewHolder(view)
    }

    override fun onBindViewHolder(holder: RecipeViewHolder, position: Int) {
        val recipe = recipes[position]
        holder.tvTitle.text = recipe.data.title
        
        // Handle times
        holder.tvPrepTime.text = if (recipe.data.prepTimeMinutes != null) {
            "${recipe.data.prepTimeMinutes} m prep"
        } else {
            ""
        }
        
        holder.tvCookTime.text = if (recipe.data.cookTimeMinutes != null) {
            "${recipe.data.cookTimeMinutes} m cook"
        } else {
            ""
        }
        
        // Load Image
        if (!recipe.thumbnailUrl.isNullOrEmpty()) {
            Glide.with(holder.itemView.context)
                .load(recipe.thumbnailUrl)
                .centerCrop()
                .placeholder(R.drawable.ic_launcher_background) // fallback
                .into(holder.ivThumbnail)
        } else {
            holder.ivThumbnail.setImageResource(R.drawable.ic_launcher_background)
        }
        
        holder.itemView.setOnClickListener { onClick(recipe) }
    }

    override fun getItemCount() = recipes.size
    
    fun updateRecipes(newRecipes: List<Recipe>) {
        recipes = newRecipes
        notifyDataSetChanged()
    }
}
