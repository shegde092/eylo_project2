import { ApifyClient } from 'apify-client';
import { config } from '../config';

export interface ScrapedData {
    url: string;
    videoUrl?: string; // Direct link to CDN or S3
    caption: string;
    ownerUsername?: string; // Made optional
}

const client = new ApifyClient({
    token: config.apify.token,
});

export async function scrapeRecipe(url: string): Promise<ScrapedData> {
    console.log(`[Scraper] Starting scrape for ${url}...`);

    // Using the 'apify/instagram-reel-scraper' actor
    const run = await client.actor('apify/instagram-reel-scraper').call({
        reelUrls: [url],
    });

    console.log(`[Scraper] Run finished: ${run.id}`);

    const { items } = await client.dataset(run.defaultDatasetId).listItems();

    if (items.length === 0) {
        throw new Error('No data returned from scraper');
    }

    const result = items[0] as any; // Cast to specific Apify output type if available

    return {
        url,
        videoUrl: result.videoUrl, // Adjust based on actual Apify output schema
        caption: result.caption,
        ownerUsername: result.ownerUsername
    };
}
