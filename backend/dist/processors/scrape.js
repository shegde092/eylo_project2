"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.scrapeRecipe = scrapeRecipe;
async function scrapeRecipe(url) {
    console.log(`[Mock Scraper] Scraping ${url}...`);
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    return {
        url,
        videoUrl: 'https://example.com/video.mp4',
        caption: 'Delicious pasta recipe! Ingredients: 200g flour, 2 eggs. Instructions: Mix and boil.'
    };
}
