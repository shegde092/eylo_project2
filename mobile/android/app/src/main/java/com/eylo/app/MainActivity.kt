package com.eylo.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.eylo.app.adapter.RecipeAdapter
import com.eylo.app.api.RetrofitClient
import com.eylo.app.models.Recipe
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {

    private lateinit var rvRecipes: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var tvEmpty: TextView
    private lateinit var adapter: RecipeAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        rvRecipes = findViewById(R.id.rvRecipes)
        progressBar = findViewById(R.id.progressBar)
        tvEmpty = findViewById(R.id.tvEmpty)

        setupRecyclerView()
        fetchRecipes()
        
        // Handle deep link if app is launched from notification
        handleDeepLink(intent)
    }
    
    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        handleDeepLink(intent)
    }
    
    private fun handleDeepLink(intent: Intent?) {
        val uri: Uri? = intent?.data
        if (uri != null && uri.scheme == "eylo" && uri.host == "recipe") {
            val recipeId = uri.lastPathSegment
            if (recipeId != null) {
                Log.d("MainActivity", "Opening recipe from deep link: $recipeId")
                fetchAndOpenRecipe(recipeId)
            }
        }
    }
    
    private fun setupRecyclerView() {
        adapter = RecipeAdapter(emptyList()) { recipe ->
            // Open Detail Activity
            val intent = Intent(this, RecipeDetailActivity::class.java)
            intent.putExtra("RECIPE", recipe)
            startActivity(intent)
        }
        rvRecipes.layoutManager = LinearLayoutManager(this)
        rvRecipes.adapter = adapter
    }
    
    private fun fetchRecipes() {
        progressBar.visibility = View.VISIBLE
        tvEmpty.visibility = View.GONE
        
        RetrofitClient.instance.listRecipes().enqueue(object : Callback<List<Recipe>> {
            override fun onResponse(call: Call<List<Recipe>>, response: Response<List<Recipe>>) {
                progressBar.visibility = View.GONE
                if (response.isSuccessful) {
                    val recipes = response.body() ?: emptyList()
                    if (recipes.isEmpty()) {
                        tvEmpty.visibility = View.VISIBLE
                    } else {
                        adapter.updateRecipes(recipes)
                    }
                } else {
                    showError("Failed to load recipes: ${response.code()}")
                }
            }
            
            override fun onFailure(call: Call<List<Recipe>>, t: Throwable) {
                progressBar.visibility = View.GONE
                showError("Network error: ${t.message}")
            }
        })
    }
    
    private fun fetchAndOpenRecipe(recipeId: String) {
        // Fetch single recipe and open detail
        RetrofitClient.instance.getRecipe(recipeId).enqueue(object : Callback<Recipe> {
            override fun onResponse(call: Call<Recipe>, response: Response<Recipe>) {
                if (response.isSuccessful && response.body() != null) {
                    val recipe = response.body()!!
                    val intent = Intent(this@MainActivity, RecipeDetailActivity::class.java)
                    intent.putExtra("RECIPE", recipe)
                    startActivity(intent)
                }
            }
            
            override fun onFailure(call: Call<Recipe>, t: Throwable) {
                Log.e("MainActivity", "Failed to fetch recipe for deep link", t)
            }
        })
    }
    
    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
