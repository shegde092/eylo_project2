package com.eylo.app.api

import com.eylo.app.models.Recipe
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path

interface EyloService {
    @GET("/recipes")
    fun listRecipes(): Call<List<Recipe>>
    
    @GET("/recipes/{id}")
    fun getRecipe(@Path("id") id: String): Call<Recipe>
}
