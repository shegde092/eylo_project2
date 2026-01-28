package com.eylo.app

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.work.*
import com.google.firebase.messaging.FirebaseMessaging

class ShareActivity : AppCompatActivity() {
    
    companion object {
        const val API_BASE_URL = "http://10.0.2.2:8000" // Android emulator localhost
        // For physical device, use: "https://your-production-api.com"
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Handle share intent
        handleShareIntent()
    }
    
    private fun handleShareIntent() {
        when {
            intent?.action == Intent.ACTION_SEND -> {
                if (intent.type == "text/plain") {
                    handleSharedText(intent)
                } else {
                    showError("Unsupported content type")
                    finish()
                }
            }
            else -> {
                showError("Invalid share action")
                finish()
            }
        }
    }
    
    private fun handleSharedText(intent: Intent) {
        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
        
        if (sharedText.isNullOrEmpty()) {
            showError("No URL found")
            finish()
            return
        }
        
        // Extract Instagram URL
        val url = extractInstagramURL(sharedText)
        
        if (url == null) {
            showError("Not an Instagram URL")
            finish()
            return
        }
        
        // Get auth token
        val authToken = getAuthToken()
        if (authToken.isNullOrEmpty()) {
            showError("Please log in to Eylo first")
            finish()
            return
        }
        
        // Get FCM token
        getFCMToken { fcmToken ->
            // Enqueue background work
            enqueueImportWork(url, authToken, fcmToken)
            
            // Show success message
            Toast.makeText(
                this,
                "Recipe import started! 🍝\nYou'll get a notification when it's ready.",
                Toast.LENGTH_LONG
            ).show()
            
            // Close activity
            finish()
        }
    }
    
    private fun extractInstagramURL(text: String): String? {
        val pattern = Regex("https?://(?:www\\.)?instagram\\.com/(?:reel|p|tv)/[\\w-]+/?")
        return pattern.find(text)?.value
    }
    
    private fun getAuthToken(): String? {
        val prefs = getSharedPreferences("EyloPrefs", MODE_PRIVATE)
        return prefs.getString("authToken", null)
    }
    
    private fun getFCMToken(callback: (String?) -> Unit) {
        FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                callback(task.result)
            } else {
                callback(null)
            }
        }
    }
    
    private fun enqueueImportWork(url: String, authToken: String, fcmToken: String?) {
        val workData = workDataOf(
            "url" to url,
            "authToken" to authToken,
            "fcmToken" to fcmToken
        )
        
        val importRequest = OneTimeWorkRequestBuilder<RecipeImportWorker>()
            .setInputData(workData)
            .setConstraints(
                Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build()
            )
            .build()
        
        WorkManager.getInstance(this).enqueue(importRequest)
    }
    
    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
