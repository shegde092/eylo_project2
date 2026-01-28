# iOS Share Extension Implementation

## Overview

iOS Share Extension that allows users to share Instagram URLs directly to Eylo from the Instagram app.

## Setup Instructions

### 1. Add Share Extension Target in Xcode

1. Open `Eylo.xcodeproj` in Xcode
2. Go to **File → New → Target**
3. Select **Share Extension** template
4. Name it `EyloShare`
5. Choose **Swift** as language
6. Click **Finish**

### 2. Configure App Groups

Both the main app and extension need to share data via App Groups:

1. Select the **Eylo** target
2. Go to **Signing & Capabilities**
3. Click **+ Capability** → **App Groups**
4. Add: `group.com.eylo.app`

5. Select the **EyloShare** target
6. Repeat steps 2-4

### 3. Configure Keychain Sharing

To share the auth token between app and extension:

1. Select the **Eylo** target
2. **Signing & Capabilities** → **+ Capability** → **Keychain Sharing**
3. Add: `com.eylo.app`

4. Select the **EyloShare** target
5. Repeat steps 2-3

### 4. Add Dependencies

Add to `Podfile` (or use Swift Package Manager):

```ruby
target 'Eylo' do
  pod 'KeychainAccess'
  pod 'FirebaseMessaging'
end

target 'EyloShare' do
  pod 'KeychainAccess'
end
```

Run: `pod install`

### 5. Replace Generated Files

Replace the auto-generated `ShareViewController.swift` and `Info.plist` with the files in this directory.

## How It Works

### Flow

1. User is in Instagram app viewing a Reel
2. Taps **Share** button
3. Selects **Eylo** from share sheet
4. `ShareViewController` extracts the Instagram URL
5. Reads auth token from shared Keychain
6. Makes `POST /import/recipe` API call
7. Shows success message
8. Extension closes → user back in Instagram

### Authentication

Auth token is stored in **Keychain** with:
- Service: `com.eylo.app`
- Key: `authToken`
- Accessibility: `.afterFirstUnlock`

The main app saves the token after login, and the extension reads it.

### FCM Token Sharing

FCM token is saved in **UserDefaults** with App Group:
```swift
let userDefaults = UserDefaults(suiteName: "group.com.eylo.app")
userDefaults?.set(fcmToken, forKey: "fcmToken")
```

## Main App Integration

### 1. Save Auth Token (After Login)

```swift
import KeychainAccess

let keychain = Keychain(service: "com.eylo.app")
    .accessibility(.afterFirstUnlock)

try? keychain.set(authToken, key: "authToken")
```

### 2. Save FCM Token

```swift
let userDefaults = UserDefaults(suiteName: "group.com.eylo.app")
userDefaults?.set(fcmToken, forKey: "fcmToken")
```

### 3. Handle Push Notifications

In `AppDelegate.swift`:

```swift
import UserNotifications
import FirebaseMessaging

class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate, MessagingDelegate {
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Firebase
        FirebaseApp.configure()
        
        // Push notifications
        UNUserNotificationCenter.current().delegate = self
        let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
        UNUserNotificationCenter.current().requestAuthorization(options: authOptions) { granted, _ in
            print("Push permission: \(granted)")
        }
        application.registerForRemoteNotifications()
        
        Messaging.messaging().delegate = self
        
        return true
    }
    
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        print("FCM Token: \(fcmToken ?? "")")
        
        // Save to UserDefaults for Share Extension
        if let token = fcmToken {
            let userDefaults = UserDefaults(suiteName: "group.com.eylo.app")
            userDefaults?.set(token, forKey: "fcmToken")
        }
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter, didReceive response: UNNotificationResponse, withCompletionHandler completionHandler: @escaping () -> Void) {
        
        let userInfo = response.notification.request.content.userInfo
        
        // Handle recipe_imported notification
        if let type = userInfo["type"] as? String, type == "recipe_imported",
           let recipeId = userInfo["recipe_id"] as? String {
            
            // Navigate to recipe detail
            navigateToRecipe(id: recipeId)
        }
        
        completionHandler()
    }
    
    func navigateToRecipe(id: String) {
        // TODO: Navigate to RecipeDetailViewController
        print("Navigate to recipe: \(id)")
    }
}
```

### 4. Handle Deep Links

In `AppDelegate.swift`:

```swift
func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
    
    // Handle eylo://recipe/{id}
    if url.scheme == "eylo" && url.host == "recipe" {
        let recipeId = url.pathComponents[1]
        navigateToRecipe(id: recipeId)
        return true
    }
    
    return false
}
```

Add to `Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>eylo</string>
        </array>
        <key>CFBundleURLName</key>
        <string>com.eylo.app</string>
    </dict>
</array>
```

## Testing

### 1. Run on Simulator

```bash
# Build and run main app
Cmd + R

# To test share extension:
1. Open Safari in Simulator
2. Navigate to: https://www.instagram.com/reel/ABC123/
3. Tap share button
4. Select "Eylo"
```

**Note**: Push notifications don't work in Simulator - need physical device.

### 2. Test on Physical Device

1. Connect iPhone via USB
2. Select device in Xcode
3. Build and run
4. Open Instagram app
5. Share a Reel
6. Select "Eylo"
7. Wait ~30 seconds for push notification

## Troubleshooting

### Share extension doesn't appear

- Check `Info.plist` activation rules
- Ensure extension is included in build
- Restart device

### "Please log in to Eylo first" error

- Main app hasn't saved auth token to Keychain
- Check Keychain Sharing is configured for both targets

### Network error

- Check API base URL (use ngrok for testing with localhost)
- Verify auth token is valid

## Production Checklist

- [ ] Update `apiBaseURL` to production URL
- [ ] Add error logging (Sentry, etc.)
- [ ] Test with various Instagram URL formats
- [ ] Add retry logic for failed requests
- [ ] Optimize UI/UX feedback
