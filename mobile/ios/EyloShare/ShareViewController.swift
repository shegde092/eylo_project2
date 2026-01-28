import UIKit
import Social
import MobileCoreServices
import KeychainAccess

class ShareViewController: SLComposeServiceViewController {
    
    // Shared configuration
    let apiBaseURL = "http://localhost:8000"  // Change in production
    let appGroupIdentifier = "group.com.eylo.app"
    let keychainService = "com.eylo.app"
    
    var sharedURL: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Extract URL from share context
        extractSharedURL()
    }
    
    override func isContentValid() -> Bool {
        // Validate that we have an Instagram URL
        guard let url = sharedURL else {
            return false
        }
        
        return isInstagramURL(url)
    }
    
    override func didSelectPost() {
        // User tapped "Post" button - send to API
        guard let url = sharedURL else {
            showError("No URL found")
            return
        }
        
        // Get auth token from Keychain
        guard let authToken = getAuthToken() else {
            showError("Please log in to Eylo first")
            return
        }
        
        // Send to API
        sendImportRequest(url: url, authToken: authToken)
    }
    
    override func configurationItems() -> [Any]! {
        // Show info about what will happen
        let statusItem = SLComposeSheetConfigurationItem()!
        statusItem.title = "Status"
        statusItem.value = sharedURL != nil ? "Ready to import" : "No URL detected"
        
        return [statusItem]
    }
    
    // MARK: - Private Methods
    
    private func extractSharedURL() {
        guard let extensionItem = extensionContext?.inputItems.first as? NSExtensionItem,
              let itemProvider = extensionItem.attachments?.first else {
            return
        }
        
        // Check for URL
        if itemProvider.hasItemConformingToTypeIdentifier(kUTTypeURL as String) {
            itemProvider.loadItem(forTypeIdentifier: kUTTypeURL as String, options: nil) { [weak self] (url, error) in
                if let shareURL = url as? URL {
                    DispatchQueue.main.async {
                        self?.sharedURL = shareURL.absoluteString
                        self?.validateContent()
                    }
                }
            }
        }
        // Check for text (might contain URL)
        else if itemProvider.hasItemConformingToTypeIdentifier(kUTTypePlainText as String) {
            itemProvider.loadItem(forTypeIdentifier: kUTTypePlainText as String, options: nil) { [weak self] (text, error) in
                if let shareText = text as? String {
                    // Extract URL from text
                    if let extractedURL = self?.extractURLFromText(shareText) {
                        DispatchQueue.main.async {
                            self?.sharedURL = extractedURL
                            self?.validateContent()
                        }
                    }
                }
            }
        }
    }
    
    private func extractURLFromText(_ text: String) -> String? {
        // Simple regex to find Instagram URL
        let pattern = "https?://(?:www\\.)?instagram\\.com/(?:reel|p|tv)/[\\w-]+/?"
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return nil
        }
        
        let range = NSRange(text.startIndex..., in: text)
        if let match = regex.firstMatch(in: text, options: [], range: range) {
            if let urlRange = Range(match.range, in: text) {
                return String(text[urlRange])
            }
        }
        
        return nil
    }
    
    private func isInstagramURL(_ url: String) -> Bool {
        let pattern = "https?://(?:www\\.)?instagram\\.com/(?:reel|p|tv)/[\\w-]+/?"
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return false
        }
        
        let range = NSRange(url.startIndex..., in: url)
        return regex.firstMatch(in: url, options: [], range: range) != nil
    }
    
    private func getAuthToken() -> String? {
        // Read from Keychain (shared with main app via App Group)
        let keychain = Keychain(service: keychainService)
            .accessibility(.afterFirstUnlock)
            .synchronizable(false)
        
        return try? keychain.get("authToken")
    }
    
    private func getFCMToken() -> String? {
        // Read FCM token from UserDefaults (shared via App Group)
        if let userDefaults = UserDefaults(suiteName: appGroupIdentifier) {
            return userDefaults.string(forKey: "fcmToken")
        }
        return nil
    }
    
    private func sendImportRequest(url: String, authToken: String) {
        let endpoint = "\(apiBaseURL)/import/recipe"
        
        guard let apiURL = URL(string: endpoint) else {
            showError("Invalid API URL")
            return
        }
        
        var request = URLRequest(url: apiURL)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        
        let body: [String: Any] = [
            "url": url,
            "fcm_token": getFCMToken() ?? ""
        ]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        // Show loading
        let loadingAlert = showLoading()
        
        // Send request
        let task = URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                loadingAlert.dismiss(animated: false)
                
                if let error = error {
                    self?.showError("Network error: \(error.localizedDescription)")
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    self?.showError("Invalid response")
                    return
                }
                
                if httpResponse.statusCode == 200 || httpResponse.statusCode == 202 {
                    // Success!
                    self?.showSuccess()
                } else {
                    self?.showError("Server error: \(httpResponse.statusCode)")
                }
            }
        }
        
        task.resume()
    }
    
    private func showLoading() -> UIAlertController {
        let alert = UIAlertController(title: "Importing Recipe...", message: "Please wait", preferredStyle: .alert)
        present(alert, animated: true)
        return alert
    }
    
    private func showSuccess() {
        let alert = UIAlertController(
            title: "Recipe Import Started! 🍝",
            message: "You'll receive a notification when it's ready.",
            preferredStyle: .alert
        )
        
        alert.addAction(UIAlertAction(title: "OK", style: .default) { [weak self] _ in
            self?.extensionContext?.completeRequest(returningItems: nil, completionHandler: nil)
        })
        
        present(alert, animated: true)
    }
    
    private func showError(_ message: String) {
        let alert = UIAlertController(
            title: "Error",
            message: message,
            preferredStyle: .alert
        )
        
        alert.addAction(UIAlertAction(title: "OK", style: .default) { [weak self] _ in
            self?.extensionContext?.cancelRequest(withError: NSError(domain: "EyloShare", code: -1))
        })
        
        present(alert, animated: true)
    }
}
