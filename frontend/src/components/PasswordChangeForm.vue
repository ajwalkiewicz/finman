<template>
  <div class="password-change-form">
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Change Password
        </h3>
        <div class="mt-2 max-w-xl text-sm text-gray-500">
          <p>Update your password to keep your account secure.</p>
        </div>
        
        <form @submit.prevent="handleSubmit" class="mt-5 space-y-6">
          <!-- Current Password -->
          <div>
            <label for="current-password" class="block text-sm font-medium text-gray-700">
              Current Password
            </label>
            <div class="mt-1">
              <input
                id="current-password"
                v-model="currentPassword"
                type="password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Enter your current password"
              />
            </div>
          </div>

          <!-- New Password -->
          <div>
            <label for="new-password" class="block text-sm font-medium text-gray-700">
              New Password
            </label>
            <div class="mt-1">
              <PasswordStrengthInput
                v-model="newPassword"
                input-id="new-password"
                placeholder="Enter new password"
                :show-strength-meter="true"
                :show-requirements="true"
                :error="passwordError"
                :username="currentUsername"
                @validation-change="onPasswordValidationChange"
                required
              />
            </div>
          </div>

          <!-- Confirm New Password -->
          <div>
            <label for="confirm-password" class="block text-sm font-medium text-gray-700">
              Confirm New Password
            </label>
            <div class="mt-1">
              <input
                id="confirm-password"
                v-model="confirmPassword"
                type="password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                :class="{
                  'border-red-500': confirmPassword && confirmPassword !== newPassword,
                  'border-green-500': confirmPassword && confirmPassword === newPassword && newPassword.length > 0
                }"
                placeholder="Confirm your new password"
              />
              <p v-if="confirmPassword && confirmPassword !== newPassword" class="mt-1 text-sm text-red-600">
                Passwords do not match
              </p>
              <p v-else-if="confirmPassword && confirmPassword === newPassword && newPassword.length > 0" class="mt-1 text-sm text-green-600">
                Passwords match
              </p>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end">
            <button
              type="submit"
              :disabled="loading || !canSubmit"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Changing...' : 'Change Password' }}
            </button>
          </div>
        </form>

        <!-- Success Message -->
        <div v-if="successMessage" class="mt-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          {{ successMessage }}
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          <div v-if="typeof error === 'string'">
            {{ error }}
          </div>
          <div v-else-if="error.type === 'password_validation_error'">
            <p class="font-medium">{{ error.message }}</p>
            <ul class="mt-2 list-disc list-inside text-sm">
              <li v-for="requirement in error.requirements" :key="requirement">
                {{ requirement }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { authAPI } from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import PasswordStrengthInput from '@/components/PasswordStrengthInput.vue';

const authStore = useAuthStore();

const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref<string | any>('');
const successMessage = ref('');
const passwordError = ref('');
const isPasswordValid = ref(false);

const currentUsername = computed(() => authStore.user?.username || '');

const canSubmit = computed(() => {
  return (
    currentPassword.value &&
    newPassword.value &&
    confirmPassword.value &&
    newPassword.value === confirmPassword.value &&
    isPasswordValid.value &&
    !loading.value
  );
});

const onPasswordValidationChange = (valid: boolean) => {
  isPasswordValid.value = valid;
  if (valid) {
    passwordError.value = '';
  }
};

const resetForm = () => {
  currentPassword.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
  error.value = '';
  passwordError.value = '';
  isPasswordValid.value = false;
};

const handleSubmit = async () => {
  if (!canSubmit.value) return;

  loading.value = true;
  error.value = '';
  successMessage.value = '';

  try {
    const response = await authAPI.changePassword(currentPassword.value, newPassword.value);
    successMessage.value = response.message;
    resetForm();
    
    // Auto-hide success message after 5 seconds
    setTimeout(() => {
      successMessage.value = '';
    }, 5000);
    
  } catch (err: any) {
    console.error('Password change error:', err);
    
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      if (typeof detail === 'object' && detail.type === 'password_validation_error') {
        error.value = detail;
      } else {
        error.value = typeof detail === 'string' ? detail : 'Failed to change password. Please try again.';
      }
    } else {
      error.value = 'Failed to change password. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.password-change-form {
  max-width: 600px;
}
</style>