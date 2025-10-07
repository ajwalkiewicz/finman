import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authAPI } from '@/services/api';
import type { User } from '@/types';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem('token'));
  
  const isAuthenticated = computed(() => !!token.value);
  
  const login = async (username: string, password: string) => {
    try {
      const response = await authAPI.login(username, password);
      token.value = response.access_token;
      localStorage.setItem('token', response.access_token);
      
      // Get user info
      user.value = await authAPI.getCurrentUser();
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };
  
  const register = async (username: string, password: string) => {
    try {
      await authAPI.register(username, password);
      return await login(username, password);
    } catch (error) {
      console.error('Registration failed:', error);
      return false;
    }
  };
  
  const logout = () => {
    user.value = null;
    token.value = null;
    localStorage.removeItem('token');
  };
  
  const initializeAuth = async () => {
    if (token.value) {
      try {
        user.value = await authAPI.getCurrentUser();
      } catch (error) {
        logout();
      }
    }
  };
  
  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    initializeAuth
  };
});