"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.config = void 0;
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
exports.config = {
    redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT || '6379'),
    },
    postgres: {
        user: process.env.POSTGRES_USER || 'admin',
        host: process.env.POSTGRES_HOST || 'localhost',
        database: process.env.POSTGRES_DB || 'eylo_db',
        password: process.env.POSTGRES_PASSWORD || 'password',
        port: parseInt(process.env.POSTGRES_PORT || '5432'),
    },
    apify: {
        token: process.env.APIFY_TOKEN || 'mock_token',
    },
    gemini: {
        apiKey: process.env.GEMINI_API_KEY || 'mock_key',
    }
};
