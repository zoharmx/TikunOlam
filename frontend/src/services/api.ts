import axios, { AxiosInstance } from 'axios';
import type {
  AnalysisRequest,
  AnalysisResponse,
  JobResponse,
  JobStatusResponse,
  JobListResponse,
} from '../types';

class TikunAPI {
  private client: AxiosInstance;

  constructor(baseURL: string = '') {
    this.client = axios.create({
      baseURL,
      timeout: 900000, // 15 minutes for long analysis (Tikun pipeline 8-12 min with overhead)
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async analyzeSync(request: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await this.client.post<AnalysisResponse>('/analyze', request);
    return response.data;
  }

  async analyzeAsync(request: AnalysisRequest): Promise<JobResponse> {
    const response = await this.client.post<JobResponse>('/analyze/async', request);
    return response.data;
  }

  async getJobStatus(jobId: string): Promise<JobStatusResponse> {
    const response = await this.client.get<JobStatusResponse>(`/jobs/${jobId}`);
    return response.data;
  }

  async listJobs(limit: number = 50, status?: string): Promise<JobListResponse> {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (status) {
      params.append('status', status);
    }
    const response = await this.client.get<JobListResponse>(`/jobs?${params.toString()}`);
    return response.data;
  }

  async deleteJob(jobId: string): Promise<{ message: string }> {
    const response = await this.client.delete(`/jobs/${jobId}`);
    return response.data;
  }

  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }

  async getMetrics(): Promise<any> {
    const response = await this.client.get('/metrics');
    return response.data;
  }
}

// Get API URL from environment variables
// In production: https://tikun-olam-495684990330.us-central1.run.app
// In development: http://localhost:8000
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = new TikunAPI(API_URL);
export default api;
