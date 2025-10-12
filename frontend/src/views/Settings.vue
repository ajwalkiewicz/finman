<template>
  <div class="settings-page">
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="md:flex md:items-center md:justify-between mb-8">
        <div class="flex-1 min-w-0">
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Settings
          </h2>
          <p class="mt-1 text-sm text-gray-500">
            Manage your account settings and preferences
          </p>
        </div>
      </div>

      <!-- Settings Tabs -->
      <div class="mb-8">
        <div class="sm:hidden">
          <label for="tabs" class="sr-only">Select a tab</label>
          <select
            id="tabs"
            v-model="activeTab"
            class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
          >
            <option value="security">Security</option>
            <option value="profile">Profile</option>
          </select>
        </div>
        <div class="hidden sm:block">
          <nav class="flex space-x-8" aria-label="Tabs">
            <button
              @click="activeTab = 'security'"
              :class="[
                activeTab === 'security'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              Security
            </button>
            <button
              @click="activeTab = 'profile'"
              :class="[
                activeTab === 'profile'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              Profile
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="space-y-6">
        <!-- Security Tab -->
        <div v-if="activeTab === 'security'" class="space-y-6">
          <!-- Password Change -->
          <PasswordChangeForm />
          
          <!-- Additional Security Settings -->
          <div class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Security Information
              </h3>
              <div class="mt-2 max-w-xl text-sm text-gray-500">
                <p>Your account security information and tips.</p>
              </div>
              <div class="mt-5">
                <div class="rounded-md bg-blue-50 p-4">
                  <div class="flex">
                    <div class="flex-shrink-0">
                      <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                      </svg>
                    </div>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-blue-800">
                        Security Tips
                      </h3>
                      <div class="mt-2 text-sm text-blue-700">
                        <ul class="list-disc list-inside space-y-1">
                          <li>Use a strong, unique password for your account</li>
                          <li>Don't share your login credentials with anyone</li>
                          <li>Log out from shared computers</li>
                          <li>Change your password regularly</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Tab -->
        <div v-if="activeTab === 'profile'" class="space-y-6">
          <!-- User Information -->
          <div class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Profile Information
              </h3>
              <div class="mt-2 max-w-xl text-sm text-gray-500">
                <p>Your account information and preferences.</p>
              </div>
              <div class="mt-5 space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Username</label>
                  <div class="mt-1 text-sm text-gray-900">{{ user?.username || 'Loading...' }}</div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Account Created</label>
                  <div class="mt-1 text-sm text-gray-900">
                    {{ user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Loading...' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import PasswordChangeForm from '@/components/PasswordChangeForm.vue';

const authStore = useAuthStore();
const activeTab = ref('security');
const user = ref(authStore.user);

onMounted(async () => {
  // Ensure we have the latest user data
  if (!user.value) {
    await authStore.initializeAuth();
    user.value = authStore.user;
  }
});
</script>

<style scoped>
.settings-page {
  min-height: calc(100vh - 4rem);
}
</style>