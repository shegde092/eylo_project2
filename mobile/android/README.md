# Android Share Intent Implementation

## Overview

Android Share Intent implementation that allows users to share Instagram URLs from the Instagram app directly to Eylo.

## Setup Instructions

### 1. Add Dependencies

Ensure `build.gradle` (app level) has these dependencies:
- WorkManager: For reliable background API requests
- Firebase Messaging: For push notifications
- OkHttp: For HTTP requests

Already included in the provided `build.gradle`.

### 2. Add Firebase Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create/select your project
3. Add Android app with package name: `com.eylo.app`
4. Download `google-services.json`
5. Place it in `mobile/android/app/`

### 3. Update Manifest

Replace `AndroidManifest.xml` with the provided file. It includes:
- `ShareActivity` with SEND intent filter
- `FCMService` for push notifications
- Deep link configuration for `eylo://recipe/{id}`

### 4. Add String Resources

Create/update `res/values/strings.xml`:

```xml
<resources>
    <string name="app_name">Eylo</string>
    <string name="share_to_eylo">Save to Eylo</string>
</resources>
```

### 5. Add Notification Icon

Add a recipe icon at:
- `res/drawable/ic_recipe.xml`

Or use a default icon during development.

## How It Works

### Flow

1. User opens Instagram Reel
2. Taps **Share** button
3. Selects **Eylo** from share sheet
4. `ShareActivity` extracts Instagram URL from Intent
5. Reads auth token from SharedPreferences
6. Enqueues `RecipeImportWorker` (WorkManager)
7. Shows success Toast
8. Activity finishes → user back in Instagram
9. Worker makes API request in background
10. ~30 seconds later, FCM push notification arrives
11. User taps → MainActivity opens with deep link

### Authentication

Auth token stored in **SharedPreferences**:
```kotlin
val prefs = getSharedPreferences("EyloPrefs", MODE_PRIVATE)
prefs.edit().putString("authToken", token).apply()
```

### WorkManager

Used instead of direct API call because:
- Survives process death (user can close Instagram immediately)
- Automatic retry on failure
- Respects network constraints

## Main App Integration

### 1. Save Auth Token (After Login)

```kotlin
val prefs = getSharedPreferences("EyloPrefs", Context.MODE_PRIVATE)
prefs.edit().putString("authToken", authToken).apply()
```

### 2. Initialize Firebase

In `MainActivity.kt`:

```kotlin
import com.google.firebase.messaging.FirebaseMessaging

class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Request notification permission (Android 13+)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            requestPermissions(arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 1)
        }
        
        // Get and save FCM token
        FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
            if (task.isSuccessful) {
                val token = task.result
                saveFCMToken(token)
                // TODO: Send to backend
            }
        }
        
        // Handle deep link
        handleDeepLink(intent)
    }
    
    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        handleDeepLink(intent)
    }
    
    private fun handleDeepLink(intent: Intent?) {
        val uri = intent?.data
        
        if (uri?.scheme == "eylo" && uri.host == "recipe") {
            val recipeId = uri.pathSegments.getOrNull(0)
            if (recipeId != null) {
                navigateToRecipe(recipeId)
            }
        }
    }
    
    private fun navigateToRecipe(recipeId: String) {
        // TODO: Navigate to RecipeDetailFragment
        Log.d("MainActivity", "Navigate to recipe: $recipeId")
    }
    
    private fun saveFCMToken(token: String) {
        val prefs = getSharedPreferences("EyloPrefs", Context.MODE_PRIVATE)
        prefs.edit().putString("fcmToken", token).apply()
    }
}
```

## Testing

### 1. Run on Emulator

```bash
# Start Android Studio
# Open project: mobile/android
# Click Run (Shift + F10)
```

### 2. Test Share Intent

Since Instagram app doesn't work well in emulator:

```kotlin
// Create test activity
class TestShareActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val shareIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, "https://www.instagram.com/reel/ABC123/")
        }
        
        val chooser = Intent.createChooser(shareIntent, "Share to")
        startActivity(chooser)
        
        finish()
    }
}
```

Add button in MainActivity to trigger this.

### 3. Test on Physical Device

1. Connect Android phone via USB
2. Enable USB Debugging
3. Build and run from Android Studio
4. Open Instagram app
5. Share a Reel
6. Select "Save to Eylo"
7. Should see Toast message
8. Wait ~30 seconds for push notification

### API Localhost Testing

For emulator:
- Use `10.0.2.2` (maps to host machine's localhost)

For physical device:
- Use `ngrok` to expose localhost:
  ```bash
  ngrok http 8000
  ```
- Update `API_BASE_URL` in `ShareActivity.kt` and `RecipeImportWorker.kt`

## Debugging

### Check WorkManager Status

```kotlin
// In MainActivity
val workManager = WorkManager.getInstance(this)
val workInfos = workManager.getWorkInfosByTag("recipe_import").get()
workInfos.forEach { info ->
    Log.d("WorkManager", "State: ${info.state}")
}
```

### View Logs

```bash
adb logcat | grep Eylo
```

### Check SharedPreferences

```bash
adb shell
run-as com.eylo.app
cd shared_prefs
cat EyloPrefs.xml
```

## Production Checklist

- [ ] Update `API_BASE_URL` to production
- [ ] Remove `android:usesCleartextTraffic="true"` from manifest
- [ ] Add ProGuard rules for OkHttp and Gson
- [ ] Add error analytics (Crashlytics)
- [ ] Test with various Instagram URL formats
- [ ] Optimize WorkManager constraints
- [ ] Add icon for notification

## Common Issues

### "Please log in to Eylo first"

- Auth token not saved yet
- Check SharedPreferences in debugger

### Worker not running

- Device in battery saver mode
- Check WorkManager constraints
- View logs with `adb logcat`

### No push notification

- FCM token not sent to backend
- Check Firebase Console for delivery status
- Ensure notification permission granted

## Resources

- [WorkManager Guide](https://developer.android.com/topic/libraries/architecture/workmanager)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging/android/client)
- [App Links & Deep Links](https://developer.android.com/training/app-links)
