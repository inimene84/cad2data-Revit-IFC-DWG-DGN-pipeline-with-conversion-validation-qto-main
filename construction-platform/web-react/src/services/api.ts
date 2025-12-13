import axios, { AxiosInstance } from 'axios';

// API base URL - use relative path to work with nginx proxy
// If REACT_APP_API_URL is set and starts with /, use it directly (relative path)
// Otherwise fall back to /api (relative path for nginx proxy)
const API_BASE_URL = process.env.REACT_APP_API_URL?.startsWith('/')
  ? process.env.REACT_APP_API_URL
  : (process.env.REACT_APP_API_URL || '/api');

// Create axios instance with default config
export const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // File operations
  uploadFile: (file: File, projectName?: string, workflowType?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (projectName) formData.append('project_name', projectName);
    if (workflowType) formData.append('workflow_type', workflowType);

    return api.post('/extract-pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  extractPDF: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/extract-pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  extractExcel: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/extract-excel', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  processCAD: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/process-cad', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Materials operations
  calculateMaterials: (materials: any[], region: string = 'Tartu') => {
    return api.post('/calculate-materials', { materials, region });
  },

  // Report operations
  generateReport: (data: {
    project_name: string;
    summary: any;
    materials: any[];
    region?: string;
    include_vat?: boolean;
    include_suppliers?: boolean;
  }) => {
    return api.post('/generate-report', data);
  },

  // Project operations
  getProjects: () => api.get('/api/projects'),
  getProject: (id: string) => api.get(`/api/projects/${id}`),
  createProject: (data: any) => api.post('/api/projects', data),
  updateProject: (id: string, data: any) => api.put(`/api/projects/${id}`, data),
  deleteProject: (id: string) => api.delete(`/api/projects/${id}`),

  // Analytics
  getStats: () => api.get('/api/stats'),
  getAnalytics: (period?: string) => api.get('/api/analytics', { params: { period } }),

  // 3D Operations
  generate3DModel: (projectId: string) => api.post(`/api/3d/generate/${projectId}`),
  get3DModel: (projectId: string) => api.get(`/api/3d/model/${projectId}`),
  update3DAnnotations: (projectId: string, annotations: any[]) =>
    api.put(`/api/3d/annotations/${projectId}`, { annotations }),

  // Chat operations
  sendMessage: (message: string, context?: any) => {
    return api.post('/api/chat', { message, context });
  },

  // Health check
  healthCheck: () => api.get('/health'),
};

export default api;
