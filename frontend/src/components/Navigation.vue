<template>
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <h1 class="text-xl font-semibold text-gray-900">Finance Manager</h1>
        </div>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-4">
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
    </div>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router";
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const isActiveLink = (routePath: string) => {
  return useRoute().path === routePath;
};
</script>