package com.eylo.app.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class Recipe(
    val id: String,
    @SerializedName("user_id") val userId: String,
    val title: String,
    @SerializedName("source_url") val sourceUrl: String,
    @SerializedName("source_type") val sourceType: String,
    val data: RecipeData,
    @SerializedName("thumbnail_url") val thumbnailUrl: String?,
    @SerializedName("video_url") val videoUrl: String?,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("imported_at") val importedAt: String
) : Serializable

data class RecipeData(
    val title: String,
    @SerializedName("prep_time_minutes") val prepTimeMinutes: Int?,
    @SerializedName("cook_time_minutes") val cookTimeMinutes: Int?,
    val ingredients: List[Ingredient],
    val steps: List[String],
    val tags: List[String]
) : Serializable

data class Ingredient(
    val item: String,
    val quantity: String,
    val unit: String
) : Serializable
