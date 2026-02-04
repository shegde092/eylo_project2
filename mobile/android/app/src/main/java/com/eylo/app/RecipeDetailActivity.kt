package com.eylo.app

import android.os.Bundle
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.eylo.app.models.Recipe

class RecipeDetailActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_recipe_detail)

        val recipe = intent.getSerializableExtra("RECIPE") as? Recipe
        if (recipe == null) {
            finish()
            return
        }

        bindViews(recipe)
    }

    private fun bindViews(recipe: Recipe) {
        findViewById<TextView>(R.id.tvDetailTitle).text = recipe.title
        
        // Prep/Cook Times
        findViewById<TextView>(R.id.tvDetailPrep).text = 
            recipe.data.prepTimeMinutes?.let { "$it m prep" } ?: "-"
        findViewById<TextView>(R.id.tvDetailCook).text = 
            recipe.data.cookTimeMinutes?.let { "$it m cook" } ?: "-"

        // Thumbnail or Video
        val ivThumbnail = findViewById<ImageView>(R.id.ivDetailThumbnail)
        // Prefer video if available (as thumbnail), else thumbnail
        val mediaUrl = recipe.videoUrl ?: recipe.thumbnailUrl
        
        if (!mediaUrl.isNullOrEmpty()) {
            Glide.with(this)
                .load(mediaUrl)
                .centerCrop()
                .placeholder(R.drawable.ic_launcher_background)
                .into(ivThumbnail)
        }

        // Ingredients
        val llIngredients = findViewById<LinearLayout>(R.id.llIngredients)
        recipe.data.ingredients.forEach { ingredient ->
            val tv = TextView(this).apply {
                text = "• ${ingredient.quantity} ${ingredient.unit} ${ingredient.item}"
                textSize = 16f
                setPadding(0, 8, 0, 8)
            }
            llIngredients.addView(tv)
        }

        // Instructions
        val llInstructions = findViewById<LinearLayout>(R.id.llInstructions)
        recipe.data.steps.forEachIndexed { index, step ->
            val tv = TextView(this).apply {
                text = "${index + 1}. $step"
                textSize = 16f
                setPadding(0, 8, 0, 8)
            }
            llInstructions.addView(tv)
        }
    }
}
