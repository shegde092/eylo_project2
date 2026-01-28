export interface ImportRequest {
    user_id: string; // In real app, extracted from JWT
    source_url: string;
}

export interface JobPayload {
    job_id: string;
    user_id: string;
    source_url: string;
    token?: string; // Encrypted auth token if needed
}

export enum ImportStatus {
    PENDING = 'PENDING',
    SCRAPING = 'SCRAPING',
    ANALYZING = 'ANALYZING',
    COMPLETED = 'COMPLETED',
    FAILED = 'FAILED'
}

export interface Ingredient { // Schema.org compliant
    name: string;
    amount?: string;
}
