import { Worker, Job } from 'bullmq';
import { config } from './config';
import { JobPayload } from './types';
import { scrapeRecipe } from './processors/scrape';
import { analyzeRecipe } from './processors/analyze';

console.log('Starting Eylo Worker Service...');

const worker = new Worker('ingestion-queue', async (job: Job<JobPayload>) => {
    console.log(`Processing Job ${job.id}: ${job.data.source_url}`);

    try {
        // Step 1: Scrape
        await job.updateProgress(10);
        const rawData = await scrapeRecipe(job.data.source_url);
        await job.updateProgress(50);

        // Step 2: Analyze
        const recipe = await analyzeRecipe(rawData);
        await job.updateProgress(90);

        // Step 3: Save (Stubbed)
        console.log('Saving recipe:', recipe.name);

        await job.updateProgress(100);
        return recipe;

    } catch (error) {
        console.error(`Job ${job.id} failed:`, error);
        throw error;
    }
}, {
    connection: config.redis
});

worker.on('completed', (job) => {
    console.log(`Job ${job.id} has completed!`);
});

worker.on('failed', (job, err) => {
    console.log(`Job ${job?.id} has failed with ${err.message}`);
});
