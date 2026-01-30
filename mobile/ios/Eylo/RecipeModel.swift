import Foundation

// MARK: - Recipe Models

struct Recipe: Identifiable, Codable {
    let id: UUID
    let userId: UUID
    let title: String
    let sourceUrl: String
    let sourceType: String
    let data: RecipeData
    let thumbnailUrl: String?
    let videoUrl: String?
    let createdAt: Date
    let importedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case title
        case sourceUrl = "source_url"
        case sourceType = "source_type"
        case data
        case thumbnailUrl = "thumbnail_url"
        case videoUrl = "video_url"
        case createdAt = "created_at"
        case importedAt = "imported_at"
    }
}

struct RecipeData: Codable {
    let title: String
    let prepTimeMinutes: Int?
    let cookTimeMinutes: Int?
    let ingredients: [Ingredient]
    let steps: [String]
    let tags: [String]
    
    enum CodingKeys: String, CodingKey {
        case title
        case prepTimeMinutes = "prep_time_minutes"
        case cookTimeMinutes = "cook_time_minutes"
        case ingredients
        case steps
        case tags
    }
}

struct Ingredient: Codable, Identifiable {
    var id: String { item } // Using item name as ID for simplicity in SwiftUI
    let item: String
    let quantity: String
    let unit: String
}
