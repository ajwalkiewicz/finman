<template>
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <h1 class="text-lg sm:text-xl font-semibold text-gray-900 truncate">Finance Manager</h1>
        </div>

        <!-- Mobile menu button -->
        <div class="flex items-center lg:hidden">
          <button
            @click="isMenuOpen = !isMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
          >
            <span class="sr-only">Open main menu</span>
            <svg class="h-6 w-6" :class="{ 'hidden': isMenuOpen, 'block': !isMenuOpen }" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg class="h-6 w-6" :class="{ 'block': isMenuOpen, 'hidden': !isMenuOpen }" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Desktop Navigation Links -->
        <div class="hidden lg:flex items-center space-x-4">
          <RouterLink to="/" 
              :class="[
                isActiveLink('/')
                  ? 'text-indigo-600'
                  : 'text-gray-700 hover:text-gray-900',
                'text-sm',
                'rounded-md',
                'px-3',
                'py-2',
              ]"
              >
              Dashboard
          </RouterLink>
          <RouterLink to="/transactions" 
              :class="[
                isActiveLink('/transactions')
                  ? 'text-indigo-600'
                  : 'text-gray-700 hover:text-gray-900',
                'text-sm',
                'rounded-md',
                'px-3',
                'py-2',
              ]"
              >
              Transactions
          </RouterLink>
          <RouterLink to="/accounts" 
              :class="[
                isActiveLink('/accounts')
                  ? 'text-indigo-600'
                  : 'text-gray-700 hover:text-gray-900',
                'text-sm',
                'rounded-md',
                'px-3',
                'py-2',
              ]"
              >
              Accounts
          </RouterLink>
          <RouterLink to="/analytics" 
              :class="[
                isActiveLink('/analytics')
                  ? 'text-indigo-600'
                  : 'text-gray-700 hover:text-gray-900',
                'text-sm',
                'rounded-md',
                'px-3',
                'py-2',
              ]"
              >
              Analytics
          </RouterLink>
          <RouterLink to="/settings" 
              :class="[
                isActiveLink('/settings')
                  ? 'text-indigo-600'
                  : 'text-gray-700 hover:text-gray-900',
                'text-sm',
                'rounded-md',
                'px-3',
                'py-2',
              ]"
            >
            Settings
          </RouterLink>
          <button
            @click="authStore.logout(); $router.push('/login')"
            class="bg-red-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </div>
      
      <!-- Mobile Navigation Menu -->
      <div class="lg:hidden" :class="{ 'block': isMenuOpen, 'hidden': !isMenuOpen }">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-200">
          <RouterLink
            to="/"
            @click="isMenuOpen = false"
            :class="[
              isActiveLink('/') 
                ? 'bg-indigo-50 border-indigo-500 text-indigo-700' 
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition duration-150 ease-in-out'
            ]"
          >
            Dashboard
          </RouterLink>
          <RouterLink
            to="/transactions"
            @click="isMenuOpen = false"
            :class="[
              isActiveLink('/transactions') 
                ? 'bg-indigo-50 border-indigo-500 text-indigo-700' 
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition duration-150 ease-in-out'
            ]"
          >
            Transactions
          </RouterLink>
          <RouterLink
            to="/accounts"
            @click="isMenuOpen = false"
            :class="[
              isActiveLink('/accounts') 
                ? 'bg-indigo-50 border-indigo-500 text-indigo-700' 
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition duration-150 ease-in-out'
            ]"
          >
            Accounts
          </RouterLink>
          <RouterLink
            to="/analytics"
            @click="isMenuOpen = false"
            :class="[
              isActiveLink('/analytics') 
                ? 'bg-indigo-50 border-indigo-500 text-indigo-700' 
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition duration-150 ease-in-out'
            ]"
          >
            Analytics
          </RouterLink>
          <RouterLink
            to="/settings"
            @click="isMenuOpen = false"
            :class="[
              isActiveLink('/settings') 
                ? 'bg-indigo-50 border-indigo-500 text-indigo-700' 
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition duration-150 ease-in-out'
            ]"
          >
            Settings
          </RouterLink>
          <button
            @click="authStore.logout(); $router.push('/login'); isMenuOpen = false"
            class="block w-full text-left pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-red-600 hover:text-red-700 hover:border-red-300 transition duration-150 ease-in-out"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, useRoute } from "vue-router";
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const isMenuOpen = ref(false);

const isActiveLink = (routePath: string) => {
  return useRoute().path === routePath;
};
</script>