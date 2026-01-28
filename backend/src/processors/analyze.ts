import { ScrapedData } from './scrape';
import { Ingredient } from '../types';

export interface Recipe {
    name: string;
    ingredients: Ingredient[];
    instructions: string[];
}

export async function analyzeRecipe(data: ScrapedData): Promise<Recipe> {
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
