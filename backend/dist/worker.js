"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const bullmq_1 = require("bullmq");
const config_1 = require("./config");
const scrape_1 = require("./processors/scrape");
const analyze_1 = require("./processors/analyze");
console.log('Starting Eylo Worker Service...');
const worker = new bullmq_1.Worker('ingestion-queue', async (job) => {
    console.log(`Processing Job ${job.id}: ${job.data.source_url}`);
    try {
        // Step 1: Scrape
        await job.updateProgress(10);
        const rawData = await (0, scrape_1.scrapeRecipe)(job.data.source_url);
        await job.updateProgress(50);
        // Step 2: Analyze
        const recipe = await (0, analyze_1.analyzeRecipe)(rawData);
        await job.updateProgress(90);
        // Step 3: Save (Stubbed)
        console.log('Saving recipe:', recipe.name);
        await job.updateProgress(100);
        return recipe;
    }
    catch (error) {
        console.error(`Job ${job.id} failed:`, error);
        throw error;
    }
}, {
    connection: config_1.config.redis
});
worker.on('completed', (job) => {
    console.log(`Job ${job.id} has completed!`);
});
worker.on('failed', (job, err) => {
    console.log(`Job ${job?.id} has failed with ${err.message}`);
});
