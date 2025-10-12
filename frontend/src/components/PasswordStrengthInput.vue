<template>
  <div class="password-strength-meter">
    <!-- Password input field -->
    <div class="relative">
      <input
        :id="inputId"
        v-model="internalValue"
        :type="showPassword ? 'text' : 'password'"
        :placeholder="placeholder"
        :required="required"
        class="appearance-none block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        @input="handleInput"
        @blur="handleBlur"
      />
      
      <!-- Show/Hide password button -->
      <button
        type="button"
        @click="togglePasswordVisibility"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <svg
          class="h-5 w-5 text-gray-400 hover:text-gray-600"
          :class="{ 'text-gray-600': showPassword }"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            v-if="!showPassword"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
          />
          <path
            v-else
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"
          />
        </svg>
      </button>
    </div>
    
    <!-- Password strength indicator -->
    <div v-if="internalValue && showStrengthMeter" class="mt-2">
      <!-- Strength bar -->
      <div class="w-full bg-gray-200 rounded-full h-2 mb-2">
        <div
          class="h-2 rounded-full transition-all duration-300"
          :style="{ 
            width: `${validationResult.score}%`, 
            backgroundColor: strengthColor 
          }"
        ></div>
      </div>
      
      <!-- Strength label -->
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium" :style="{ color: strengthColor }">
          {{ strengthLabel }}
        </span>
        <span class="text-xs text-gray-500">
          {{ validationResult.score }}% strong
        </span>
      </div>
    </div>
    
    <!-- Requirements list -->
    <div v-if="internalValue && showRequirements" class="mt-3">
      <p class="text-sm font-medium text-gray-700 mb-2">Password Requirements:</p>
      <ul class="space-y-1">
        <li
          v-for="(requirement, index) in validationResult.requirements"
          :key="index"
          class="flex items-center text-xs"
        >
          <svg
            class="w-4 h-4 mr-2 flex-shrink-0"
            :class="{
              'text-green-500': requirement.isValid,
              'text-red-500': !requirement.isValid
            }"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              v-if="requirement.isValid"
              fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd"
            />
            <path
              v-else
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
          <span
            :class="{
              'text-green-700': requirement.isValid,
              'text-red-700': !requirement.isValid
            }"
          >
            {{ requirement.text }}
          </span>
        </li>
      </ul>
    </div>
    
    <!-- Error message -->
    <div v-if="error" class="mt-2 text-sm text-red-600">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { PasswordValidator, type PasswordValidationResult } from '@/utils/passwordValidator';

interface Props {
  modelValue: string;
  placeholder?: string;
  required?: boolean;
  showStrengthMeter?: boolean;
  showRequirements?: boolean;
  inputId?: string;
  error?: string;
}

interface Emits {
  (e: 'update:modelValue', value: string): void;
  (e: 'validation-change', isValid: boolean): void;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Enter password',
  required: false,
  showStrengthMeter: true,
  showRequirements: true,
  inputId: 'password'
});

const emit = defineEmits<Emits>();

const internalValue = ref(props.modelValue);
const showPassword = ref(false);

const validationResult = computed<PasswordValidationResult>(() => {
  return PasswordValidator.validatePassword(internalValue.value);
});

const strengthLabel = computed(() => {
  const level = PasswordValidator.getStrengthLevel(validationResult.value.score);
  return level.charAt(0).toUpperCase() + level.slice(1);
});

const strengthColor = computed(() => {
  return PasswordValidator.getStrengthColor(validationResult.value.score);
});

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleInput = () => {
  emit('update:modelValue', internalValue.value);
  emit('validation-change', validationResult.value.isValid);
};

const handleBlur = () => {
  // Additional validation on blur if needed
};

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  internalValue.value = newValue;
});

// Watch validation result and emit changes
watch(validationResult, (result) => {
  emit('validation-change', result.isValid);
}, { immediate: true });
</script>

<style scoped>
.password-strength-meter {
  width: 100%;
}
</style>