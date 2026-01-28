"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzeRecipe = analyzeRecipe;
async function analyzeRecipe(data) {
    console.log(`[Mock AI] Analyzing data...`);
    // Simulate AI processing delay
    await new Promise(resolve => setTimeout(resolve, 3000));
    // Simple deterministic mock based on caption
    if (data.caption.includes('pasta')) {
        return {
            name: 'Homemade Pasta',
            ingredients: [
                { name: 'Flour', amount: '200g' },
                { name: 'Eggs', amount: '2' }
            ],
            instructions: ['Mix ingredients', 'Knead dough', 'Boil water']
        };
    }
    return {
        name: 'Unknown Recipe',
        ingredients: [],
        instructions: []
    };
}
