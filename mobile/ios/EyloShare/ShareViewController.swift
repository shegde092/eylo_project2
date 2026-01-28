import UIKit
import Social
import MobileCoreServices

class ShareViewController: SLComposeServiceViewController {

    override func isContentValid() -> Bool {
        // Do validation of contentText and/or NSExtensionContext attachments here
        return true
    }

    override func didSelectPost() {
        // This is called after the user selects Post. Do the upload of contentText and/or NSExtensionContext attachments.
        
        // 1. Extract URL logic
        guard let extensionItems = extensionContext?.inputItems as? [NSExtensionItem] else { return }
        
        for item in extensionItems {
            if let attachments = item.attachments {
                for provider in attachments {
                    if provider.hasItemConformingToTypeIdentifier("public.url") {
                        provider.loadItem(forTypeIdentifier: "public.url", options: nil) { (url, error) in
                            if let shareURL = url as? URL {
                                self.sendToBackend(url: shareURL.absoluteString)
                            }
                        }
                        return
                    } else if provider.hasItemConformingToTypeIdentifier("public.plain-text") {
                         provider.loadItem(forTypeIdentifier: "public.plain-text", options: nil) { (text, error) in
                            if let textString = text as? String {
                                // Simple regex to find URL
                                if let url = self.extractURL(from: textString) {
                                    self.sendToBackend(url: url)
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // Inform the host that we're done, so it un-blocks its UI. Note: Alternatively you could call super's -didSelectPost, which will similarly complete the extension context.
        self.extensionContext!.completeRequest(returningItems: [], completionHandler: nil)
    }

    override func configurationItems() -> [Any]! {
        // To add configuration options via table cells at the bottom of the sheet, return an array of SLComposeSheetConfigurationItem here.
        return []
    }
    
    func extractURL(from text: String) -> String? {
         // Basic regex for URL
         let detector = try! NSDataDetector(types: NSTextCheckingResult.CheckingType.link.rawValue)
         let matches = detector.matches(in: text, options: [], range: NSRange(location: 0, length: text.utf16.count))
         
         for match in matches {
             guard let range = Range(match.range, in: text) else { continue }
             return String(text[range])
         }
         return nil
    }
    
    func sendToBackend(url: String) {
        // Define your backend URL
        guard let apiURL = URL(string: "http://localhost:3000/api/v1/recipes/import") else { return }
        
        var request = URLRequest(url: apiURL)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "user_id": "test_user_ios",
            "source_url": url
        ]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: [])
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending to backend: \(error)")
                return
            }
            print("Successfully sent to backend")
        }
        task.resume()
    }
}
