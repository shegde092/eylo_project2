
import UIKit
import UserNotifications
import FirebaseMessaging

class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate, MessagingDelegate {
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Configure Firebase
        // FirebaseApp.configure() // Uncomment when GoogleService-Info.plist is added
        
        // Setup Push Notifications
        UNUserNotificationCenter.current().delegate = self
        
        let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
        UNUserNotificationCenter.current().requestAuthorization(options: authOptions) { granted, _ in
            print("Push permission granted: \(granted)")
        }
        
        application.registerForRemoteNotifications()
        
        // Setup Firebase Messaging
        Messaging.messaging().delegate = self
        
        return true
    }
    
    // MARK: - MessagingDelegate
    
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        print("FCM Token: \(fcmToken ?? "")")
        
        // Save to UserDefaults for Share Extension to use
        if let token = fcmToken {
            let userDefaults = UserDefaults(suiteName: "group.com.eylo.app")
            userDefaults?.set(token, forKey: "fcmToken")
        }
    }
    
    // MARK: - UNUserNotificationCenterDelegate
    
    func userNotificationCenter(_ center: UNUserNotificationCenter, didReceive response: UNNotificationResponse, withCompletionHandler completionHandler: @escaping () -> Void) {
        
        let userInfo = response.notification.request.content.userInfo
        print("Received notification: \(userInfo)")
        
        // Handle recipe_imported notification
        if let type = userInfo["type"] as? String, type == "recipe_imported",
           let recipeId = userInfo["recipe_id"] as? String {
            
            print("Recipe imported: \(recipeId)")
            // Post notification to update UI
            NotificationCenter.default.post(name: NSNotification.Name("OpenRecipe"), object: nil, userInfo: ["recipeId": recipeId])
        }
        
        completionHandler()
    }
    
    // Handle foreground notifications
    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .sound])
    }
}
