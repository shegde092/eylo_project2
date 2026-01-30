
import SwiftUI

struct RecipeDetailView: View {
    let recipe: Recipe
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Header Image
                if let urlStr = recipe.videoUrl ?? recipe.thumbnailUrl, let url = URL(string: urlStr) {
                    // Ideally check video player, but use thumbnail for now if simpler
                    AsyncImage(url: url) { image in
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                    } placeholder: {
                        Color.gray.opacity(0.2)
                            .frame(height: 200)
                    }
                    .frame(maxWidth: .infinity)
                    .background(Color.black.opacity(0.1))
                }
                
                // Title & Info
                VStack(alignment: .leading, spacing: 8) {
                    Text(recipe.data.title)
                        .font(.title)
                        .fontWeight(.bold)
                    
                    HStack {
                        Label("Prep: \(recipe.data.prepTimeMinutes ?? 0)m", systemImage: "clock")
                        Label("Cook: \(recipe.data.cookTimeMinutes ?? 0)m", systemImage: "flame")
                    }
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    
                    if !recipe.data.tags.isEmpty {
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack {
                                ForEach(recipe.data.tags, id: \.self) { tag in
                                    Text("#\(tag)")
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 4)
                                        .background(Capsule().fill(Color.blue.opacity(0.1)))
                                        .foregroundColor(.blue)
                                        .font(.caption)
                                }
                            }
                        }
                    }
                }
                .padding(.horizontal)
                
                Divider()
                
                // Ingredients
                VStack(alignment: .leading, spacing: 8) {
                    Text("Ingredients")
                        .font(.headline)
                        .padding(.bottom, 4)
                    
                    ForEach(recipe.data.ingredients, id: \.item) { ingredient in
                        HStack(alignment: .top) {
                            Text("•")
                            Text(ingredient.quantity + " " + ingredient.unit)
                                .fontWeight(.medium)
                            Text(ingredient.item)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .padding(.horizontal)
                
                Divider()
                
                // Instructions
                VStack(alignment: .leading, spacing: 12) {
                    Text("Instructions")
                        .font(.headline)
                        .padding(.bottom, 4)
                    
                    ForEach(Array(recipe.data.steps.enumerated()), id: \.offset) { index, step in
                        HStack(alignment: .top) {
                            Text("\(index + 1).")
                                .font(.headline)
                                .foregroundColor(.orange)
                                .frame(width: 25, alignment: .leading)
                            
                            Text(step)
                                .font(.body)
                        }
                    }
                }
                .padding(.horizontal)
                
            }
            .padding(.bottom, 20)
        }
        .navigationBarTitleDisplayMode(.inline)
    }
}
