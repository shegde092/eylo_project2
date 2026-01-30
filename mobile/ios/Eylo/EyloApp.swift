
import SwiftUI
import KeychainAccess

@main
struct EyloApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    init() {
        // For development: Set a mock auth token so Share Extension works
        seedAuthToken()
    }
    
    var body: some Scene {
        WindowGroup {
            RecipeListView()
                .onOpenURL { url in
                    print("Opened with URL: \(url)")
                    // Handle deep link here
                }
                .onReceive(NotificationCenter.default.publisher(for: NSNotification.Name("OpenRecipe"))) { notification in
                    if let recipeId = notification.userInfo?["recipeId"] as? String {
                        print("Opening recipe via notification: \(recipeId)")
                        // Trigger navigation in RecipeListView
                    }
                }
        }
    }
    
    private func seedAuthToken() {
        // In a real app, this happens after successful login
        let keychainService = "com.eylo.app"
        let keychain = Keychain(service: keychainService)
            .accessibility(.afterFirstUnlock)
            .synchronizable(false)
        
        // Mock token
        let mockToken = "eylo_dev_token_12345"
        
        do {
            try keychain.set(mockToken, key: "authToken")
            print("Set mock auth token for Share Extension")
        } catch {
            print("Failed to set mock token: \(error)")
        }
    }
}
