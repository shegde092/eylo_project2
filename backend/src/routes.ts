import { Router } from 'express';
import { ImportRequest, JobPayload } from './types';
import { Queue } from 'bullmq';
import { v4 as uuidv4 } from 'uuid';

export const router = Router();

// Setup BullMQ Queue
const connection = {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379')
};

const ingestionQueue = new Queue('ingestion-queue', { connection });

router.post('/recipes/import', async (req, res) => {
    try {
        const { user_id, source_url } = req.body as ImportRequest;

        if (!source_url) {
            return res.status(400).json({ error: 'Source URL is required' });
        }

        // Basic URL validation
        try {
            new URL(source_url);
        } catch (e) {
            return res.status(400).json({ error: 'Invalid URL format' });
        }

        const job_id = uuidv4();
        const payload: JobPayload = {
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

    } catch (error) {
        console.error('Import Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});
