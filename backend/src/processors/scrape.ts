export interface ScrapedData {
    url: string;
    videoUrl?: string;
    caption: string;
}

export async function scrapeRecipe(url: string): Promise<ScrapedData> {
    console.log(`[Mock Scraper] Scraping ${url}...`);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    return {
        url,
        videoUrl: 'https://example.com/video.mp4',
        caption: 'Delicious pasta recipe! Ingredients: 200g flour, 2 eggs. Instructions: Mix and boil.'
    };
}
