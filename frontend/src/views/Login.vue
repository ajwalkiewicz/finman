<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Finance Manager
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        {{ isLogin ? 'Sign in to your account' : 'Create a new account' }}
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Username
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="username"
                type="text"
                required
                :class="[
                  'appearance-none block w-full px-3 py-2 border rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                  !isLogin && usernameError ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300'
                ]"
                @blur="validateUsername"
                @input="validateUsername"
              />
              <div v-if="!isLogin && usernameError" class="mt-1 text-sm text-red-600">
                {{ usernameError }}
              </div>
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <!-- Use regular input for login -->
              <input
                v-if="isLogin"
                id="password"
                v-model="password"
                type="password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
              
              <!-- Use password strength component for registration -->
              <PasswordStrengthInput
                v-else
                v-model="password"
                input-id="password"
                placeholder="Enter password"
                :show-strength-meter="true"
                :show-requirements="true"
                :error="passwordError"
                :username="username"
                @validation-change="onPasswordValidationChange"
                required
              />
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="text-sm">
              <button
                type="button"
                @click="toggleMode"
                class="font-medium text-indigo-600 hover:text-indigo-500"
              >
                {{ isLogin ? 'Need an account? Register' : 'Already have an account? Sign in' }}
              </button>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading || (!isLogin && (!isPasswordValid || !isUsernameValid))"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Loading...' : (isLogin ? 'Sign in' : 'Register') }}
            </button>
          </div>
        </form>

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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import PasswordStrengthInput from '@/components/PasswordStrengthInput.vue';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const isLogin = ref(true);
const loading = ref(false);
const error = ref<string | any>('');
const passwordError = ref('');
const isPasswordValid = ref(false);
const usernameError = ref('');
const isUsernameValid = ref(false);

const validateUsername = () => {
  if (isLogin.value) {
    usernameError.value = '';
    isUsernameValid.value = true;
    return;
  }

  const usernameRegex = /^[a-zA-Z_]{6,}$/;
  if (!username.value) {
    usernameError.value = 'Username is required';
    isUsernameValid.value = false;
  } else if (!usernameRegex.test(username.value)) {
    usernameError.value = 'Username must be at least 6 characters long and contain only English letters (a-z, A-Z) and underscores';
    isUsernameValid.value = false;
  } else {
    usernameError.value = '';
    isUsernameValid.value = true;
  }
  
  // Revalidate password when username changes
  if (!isLogin.value && password.value) {
    // Force password revalidation by triggering the computed property
    // This will be handled automatically by the PasswordStrengthInput component
    // when the username prop changes
  }
};

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  error.value = '';
  passwordError.value = '';
  usernameError.value = '';
  password.value = '';
  validateUsername();
};

const onPasswordValidationChange = (valid: boolean) => {
  isPasswordValid.value = valid;
  if (valid) {
    passwordError.value = '';
  }
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  passwordError.value = '';

  try {
    let success;
    if (isLogin.value) {
      success = await authStore.login(username.value, password.value);
    } else {
      success = await authStore.register(username.value, password.value);
    }

    if (success) {
      router.push('/');
    } else {
      error.value = isLogin.value ? 'Invalid credentials' : 'Registration failed';
    }
  } catch (err: any) {
    console.error('Authentication error:', err);
    
    if (err.response?.data?.detail) {
      const detail = err.response.data.detail;
      if (typeof detail === 'object' && detail.type === 'password_validation_error') {
        error.value = detail;
      } else {
        error.value = typeof detail === 'string' ? detail : 'An error occurred. Please try again.';
      }
    } else {
      error.value = 'An error occurred. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};
</script>