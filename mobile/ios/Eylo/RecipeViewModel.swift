
import Foundation
import Combine

class RecipeViewModel: ObservableObject {
    @Published var recipes: [Recipe] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String? = nil
    
    // NOTE: Change this if testing on a real device. Simulator can use localhost.
    private let apiURL = "http://localhost:8000/recipes"
    
    private var cancellables = Set<AnyCancellable>()
    
    init() {
        fetchRecipes()
    }
    
    func fetchRecipes() {
        guard let url = URL(string: apiURL) else {
            self.errorMessage = "Invalid URL"
            return
        }
        
        self.isLoading = true
        self.errorMessage = nil
        
        URLSession.shared.dataTaskPublisher(for: url)
            .map { $0.data }
            .decode(type: [Recipe].self, decoder: createJSONDecoder())
            .receive(on: DispatchQueue.main)
            .sink(receiveCompletion: { [weak self] completion in
                self?.isLoading = false
                switch completion {
                case .finished:
                    break
                case .failure(let error):
                    self?.errorMessage = error.localizedDescription
                    print("Error fetching recipes: \(error)")
                }
            }, receiveValue: { [weak self] recipes in
                self?.recipes = recipes
            })
            .store(in: &cancellables)
    }
    
    private func createJSONDecoder() -> JSONDecoder {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601 // Python datetime format
        return decoder
    }
}
