package com.eylo.app

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.util.regex.Pattern
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.MediaType.Companion.toMediaType
import java.io.IOException

class ShareActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // No UI, just logic then finish
        handleIntent(intent)
    }

    private fun handleIntent(intent: Intent) {
        val action = intent.action
        val type = intent.type

        if (Intent.ACTION_SEND == action && type != null) {
            val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
            if (sharedText != null) {
                val url = extractUrl(sharedText)
                if (url != null) {
                    sendToBackend(url)
                } else {
                    finish()
                }
            } else {
                 finish()
            }
        } else {
            finish()
        }
    }

    private fun extractUrl(text: String): String? {
        val urlPattern = Pattern.compile(
            "(?:^|[\\W])((ht|f)tp(s?):\\/\\/|www\\.)" +
                    "(([\\w\\-]+\\.){1,}?([\\w\\-.~]+\\/?)*" +
                    "[\\p{Alnum}.,%_=?&#\\-+()\\[\\]\\*$~@!:/{};']*)",
            Pattern.CASE_INSENSITIVE or Pattern.MULTILINE or Pattern.DOTALL
        )
        val matcher = urlPattern.matcher(text)
        if (matcher.find()) {
            return text.substring(matcher.start(1), matcher.end())
        }
        return null
    }

    private fun sendToBackend(url: String) {
        // Run network on thread or coroutine (simplified here)
        Thread {
            try {
                val client = OkHttpClient()
                val json = "{\"user_id\": \"test_user_android\", \"source_url\": \"$url\"}"
                val body = json.toRequestBody("application/json; charset=utf-8".toMediaType())
                
                // Assume 10.0.2.2 for localhost emulator access
                val request = Request.Builder()
                    .url("http://10.0.2.2:3000/api/v1/recipes/import")
                    .post(body)
                    .build()

                client.newCall(request).execute().use { response ->
                    if (!response.isSuccessful) throw IOException("Unexpected code $response")
                    
                    runOnUiThread {
                        Toast.makeText(this, "Recipe Import Started!", Toast.LENGTH_LONG).show()
                        finish()
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    Toast.makeText(this, "Import Failed", Toast.LENGTH_SHORT).show()
                    finish()
                }
            }
        }.start()
    }
}
