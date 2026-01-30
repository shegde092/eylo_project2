
import SwiftUI

struct RecipeListView: View {
    @ObservedObject var viewModel = RecipeViewModel()
    
    var body: some View {
        NavigationView {
            Group {
                if viewModel.isLoading {
                    ProgressView("Loading recipes...")
                } else if let error = viewModel.errorMessage {
                    VStack {
                        Text("Error: \(error)")
                            .foregroundColor(.red)
                            .padding()
                        Button("Retry") {
                            viewModel.fetchRecipes()
                        }
                    }
                } else if viewModel.recipes.isEmpty {
                    VStack {
                        Image(systemName: "fork.knife.circle")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("No recipes yet")
                            .font(.title3)
                            .foregroundColor(.secondary)
                        Text("Share a reel from Instagram to get started!")
                            .font(.caption)
                            .padding(.top, 4)
                    }
                } else {
                    List {
                        ForEach(viewModel.recipes) { recipe in
                            NavigationLink(destination: RecipeDetailView(recipe: recipe)) {
                                RecipeRow(recipe: recipe)
                            }
                        }
                    }
                    .refreshable {
                        viewModel.fetchRecipes()
                    }
                }
            }
            .navigationTitle("Eylo Recipes")
            .onAppear {
                viewModel.fetchRecipes()
            }
        }
    }
}

struct RecipeRow: View {
    let recipe: Recipe
    
    var body: some View {
        HStack {
            if let urlStr = recipe.thumbnailUrl, let url = URL(string: urlStr) {
                // In a real app, use AsyncImage or Kingfisher
                AsyncImage(url: url) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Color.gray.opacity(0.3)
                }
                .frame(width: 60, height: 60)
                .cornerRadius(8)
            } else {
                Color.gray.opacity(0.3)
                    .frame(width: 60, height: 60)
                    .cornerRadius(8)
                    .overlay(Image(systemName: "photo").foregroundColor(.gray))
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text(recipe.data.title)
                    .font(.headline)
                    .lineLimit(2)
                
                HStack {
                    if let prep = recipe.data.prepTimeMinutes {
                        Label("\(prep)m prep", systemImage: "clock")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    if let cook = recipe.data.cookTimeMinutes {
                        Label("\(cook)m cook", systemImage: "flame")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
        }
        .padding(.vertical, 4)
    }
}
