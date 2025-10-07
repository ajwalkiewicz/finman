import axios from 'axios';
import type { Transaction, Account, User, ExpenseSummary, AccountFlow, AuthResponse, ExchangeRatesResponse } from '@/types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: async (username: string, password: string): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/token', formData);
    return response.data;
  },
  
  register: async (username: string, password: string): Promise<User> => {
    const response = await api.post('/register', { username, password });
    return response.data;
  },
  
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  }
};

// Transactions API
export const transactionsAPI = {
  getAll: async (): Promise<Transaction[]> => {
    const response = await api.get('/transactions/');
    return response.data;
  },
  
  getById: async (id: number): Promise<Transaction> => {
    const response = await api.get(`/transactions/${id}`);
    return response.data;
  },
  
  create: async (transaction: Omit<Transaction, 'id' | 'is_expense' | 'owner_id' | 'created_at'>): Promise<Transaction> => {
    const response = await api.post('/transactions/', transaction);
    return response.data;
  },
  
  update: async (id: number, transaction: Omit<Transaction, 'id' | 'is_expense' | 'owner_id' | 'created_at'>): Promise<Transaction> => {
    const response = await api.put(`/transactions/${id}`, transaction);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/transactions/${id}`);
  }
};

// Accounts API
export const accountsAPI = {
  getAll: async (): Promise<Account[]> => {
    const response = await api.get('/accounts/');
    return response.data;
  },
  
  create: async (account: Omit<Account, 'id' | 'created_at'>): Promise<Account> => {
    const response = await api.post('/accounts/', account);
    return response.data;
  }
};

// Analytics API
export const analyticsAPI = {
  getExpenseSummary: async (): Promise<ExpenseSummary> => {
    const response = await api.get('/analytics/expenses');
    return response.data;
  },
  
  getAccountFlow: async (): Promise<AccountFlow> => {
    const response = await api.get('/analytics/accounts');
    return response.data;
  }
};

// Exchange Rates API
export const exchangeRatesAPI = {
  getRates: async (baseCurrency: string = 'PLN'): Promise<ExchangeRatesResponse> => {
    const response = await axios.get(`http://localhost:8001/api/rates?base=${baseCurrency}`);
    return response.data;
  }
};