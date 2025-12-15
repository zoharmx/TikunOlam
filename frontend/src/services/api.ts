import axios, { AxiosInstance } from 'axios';
import type {
  AnalysisRequest,
  AnalysisResponse,
  JobResponse,
  JobStatusResponse,
} from '../types';

class TikunAPI {
  private client: AxiosInstance;

  constructor(baseURL: string = '/api') {
    this.client = axios.create({
      baseURL,
      timeout: 300000, // 5 minutes for long analysis
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

  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }

  async getMetrics(): Promise<any> {
    const response = await this.client.get('/metrics');
    return response.data;
  }
}

export const api = new TikunAPI();
export default api;
