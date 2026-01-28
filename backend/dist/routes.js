"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.router = void 0;
const express_1 = require("express");
const bullmq_1 = require("bullmq");
const uuid_1 = require("uuid");
exports.router = (0, express_1.Router)();
// Setup BullMQ Queue
const connection = {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379')
};
const ingestionQueue = new bullmq_1.Queue('ingestion-queue', { connection });
exports.router.post('/recipes/import', async (req, res) => {
    try {
        const { user_id, source_url } = req.body;
        if (!source_url) {
            return res.status(400).json({ error: 'Source URL is required' });
        }
        // Basic URL validation
        try {
            new URL(source_url);
        }
        catch (e) {
            return res.status(400).json({ error: 'Invalid URL format' });
        }
        const job_id = (0, uuid_1.v4)();
        const payload = {
            job_id,
            user_id: user_id || 'anonymous', // Fallback for testing
            source_url
        };
        await ingestionQueue.add('process-recipe', payload, {
            jobId: job_id,
            removeOnComplete: true
        });
        res.status(202).json({
            status: 'ACCEPTED',
            job_id,
            message: 'Recipe import started'
        });
    }
    catch (error) {
        console.error('Import Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});
