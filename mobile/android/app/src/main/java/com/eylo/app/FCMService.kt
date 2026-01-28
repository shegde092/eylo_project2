package com.eylo.app

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class FCMService : FirebaseMessagingService() {
    
    override fun onNewToken(token: String) {
        super.onNewToken(token)
        
        // Save FCM token to SharedPreferences
        val prefs = getSharedPreferences("EyloPrefs", Context.MODE_PRIVATE)
        prefs.edit().putString("fcmToken", token).apply()
        
        // TODO: Send token to backend
    }
    
    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        
        // Handle recipe_imported notification
        if (message.data["type"] == "recipe_imported") {
            val recipeId = message.data["recipe_id"] ?: return
            val title = message.notification?.title ?: "Recipe Ready!"
            val body = message.notification?.body ?: "Your recipe has been imported"
            
            showNotification(recipeId, title, body)
        }
    }
    
    private fun showNotification(recipeId: String, title: String, body: String) {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        // Create notification channel (Android 8.0+)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "recipe_imports",
                "Recipe Imports",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Notifications for recipe imports"
            }
            notificationManager.createNotificationChannel(channel)
        }
        
        // Create deep link intent
        val deepLinkIntent = Intent(Intent.ACTION_VIEW, Uri.parse("eylo://recipe/$recipeId"))
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            deepLinkIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        
        // Build notification
        val notification = NotificationCompat.Builder(this, "recipe_imports")
            .setSmallIcon(R.drawable.ic_recipe) // TODO: Add icon
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .build()
        
        notificationManager.notify(recipeId.hashCode(), notification)
    }
}
