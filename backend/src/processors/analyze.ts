import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from '../config';
import { ScrapedData } from './scrape';
import { Ingredient } from '../types';

export interface Recipe {
    name: string;
    ingredients: Ingredient[];
    instructions: string[];
}

const genAI = new GoogleGenerativeAI(config.gemini.apiKey);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });

export async function analyzeRecipe(data: ScrapedData): Promise<Recipe> {
    console.log(`[AI] Analying content for ${data.url}...`);

    const prompt = `
    You are a professional culinary data analyst. Extract a structured recipe from the following social media post data.
    
    CAPTION:
    ${data.caption}
    
    VIDEO URL:
    ${data.videoUrl || 'N/A'} (Note: In this implementation phase, we rely on caption/transcript text primarily, or video URI if the SDK supports passing it directly)
    
    OUTPUT SCHEMA (JSON):
    {
      "name": "Recipe Name",
      "ingredients": [
        { "name": "Ingredient Name", "amount": "Quantity" }
      ],
      "instructions": [ "Step 1", "Step 2" ]
    }
    
    Handle emojis and casual language. Convert to standard culinary terms.
  `;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    // Basic JSON cleanup logic (in production use structuredOutputMode or more robust parsing)
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
        throw new Error('Failed to parse JSON from AI response');
    }

    try {
        const recipe: Recipe = JSON.parse(jsonMatch[0]);
        return recipe;
    } catch (e) {
        console.error('JSON Parse Error:', text);
        throw new Error('Invalid JSON format from AI');
    }
}
