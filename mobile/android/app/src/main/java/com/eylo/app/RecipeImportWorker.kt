package com.eylo.app

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException

class RecipeImportWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    
    companion object {
        const val API_BASE_URL = "http://10.0.2.2:8000" // Match ShareActivity
    }
    
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val url = inputData.getString("url") ?: return@withContext Result.failure()
        val authToken = inputData.getString("authToken") ?: return@withContext Result.failure()
        val fcmToken = inputData.getString("fcmToken")
        
        try {
            sendImportRequest(url, authToken, fcmToken)
            Result.success()
        } catch (e: Exception) {
            // Retry on failure
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure()
            }
        }
    }
    
    private fun sendImportRequest(url: String, authToken: String, fcmToken: String?) {
        val client = OkHttpClient()
        
        val json = JSONObject().apply {
            put("url", url)
            put("fcm_token", fcmToken ?: "")
        }
        
        val body = json.toString().toRequestBody("application/json".toMediaType())
        
        val request = Request.Builder()
            .url("$API_BASE_URL/import/recipe")
            .post(body)
            .addHeader("Content-Type", "application/json")
            .addHeader("Authorization", "Bearer $authToken")
            .build()
        
        val response = client.newCall(request).execute()
        
        if (!response.isSuccessful) {
            throw IOException("API request failed: ${response.code}")
        }
    }
}
