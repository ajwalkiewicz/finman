<template>
  <div class="subscription-manager">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Subscription</h3>
    
    <!-- Current Subscription Info -->
    <div v-if="subscriptionInfo" class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h4 class="text-base font-medium text-gray-900">
            {{ subscriptionInfo.subscription_name }} Plan
          </h4>
          <p class="text-sm text-gray-500">
            {{ subscriptionInfo.current_transactions }} / {{ subscriptionInfo.max_transactions }} transactions used
          </p>
          <p class="text-sm text-gray-500">
            {{ subscriptionInfo.current_accounts }} / {{ subscriptionInfo.max_accounts }} accounts used
          </p>
        </div>
        <div class="text-right">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                :class="getSubscriptionBadgeClass(subscriptionInfo.subscription_type)">
            {{ subscriptionInfo.subscription_name }}
          </span>
        </div>
      </div>
      
      <!-- Progress Bars -->
      <div class="space-y-3 mb-4">
        <div>
          <div class="flex justify-between text-xs text-gray-600 mb-1">
            <span>Transactions</span>
            <span>{{ subscriptionInfo.current_transactions }} / {{ subscriptionInfo.max_transactions }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div class="h-2 rounded-full transition-all duration-300"
                 :class="[
                   getProgressBarClass(subscriptionInfo.subscription_type),
                   subscriptionInfo.current_transactions > subscriptionInfo.max_transactions ? 'bg-red-600' : ''
                 ]"
                 :style="`width: ${Math.min((subscriptionInfo.current_transactions / subscriptionInfo.max_transactions) * 100, 100)}%`">
            </div>
          </div>
          <div v-if="subscriptionInfo.current_transactions > subscriptionInfo.max_transactions" 
               class="text-xs text-red-600 mt-1">
            Over limit by {{ subscriptionInfo.current_transactions - subscriptionInfo.max_transactions }}
          </div>
        </div>
        
        <div>
          <div class="flex justify-between text-xs text-gray-600 mb-1">
            <span>Accounts</span>
            <span>{{ subscriptionInfo.current_accounts }} / {{ subscriptionInfo.max_accounts }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div class="h-2 rounded-full transition-all duration-300"
                 :class="[
                   getProgressBarClass(subscriptionInfo.subscription_type),
                   subscriptionInfo.current_accounts > subscriptionInfo.max_accounts ? 'bg-red-600' : ''
                 ]"
                 :style="`width: ${Math.min((subscriptionInfo.current_accounts / subscriptionInfo.max_accounts) * 100, 100)}%`">
            </div>
          </div>
          <div v-if="subscriptionInfo.current_accounts > subscriptionInfo.max_accounts" 
               class="text-xs text-red-600 mt-1">
            Over limit by {{ subscriptionInfo.current_accounts - subscriptionInfo.max_accounts }}
          </div>
        </div>
      </div>
      
      <!-- Limit Warnings -->
      <div class="space-y-3">
        <!-- Transaction Limit Warning -->
        <div v-if="!subscriptionInfo.can_add_transaction" class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Transaction Limit Reached</h3>
              <p class="text-sm text-red-700 mt-1">
                You've reached your transaction limit for the {{ subscriptionInfo.subscription_name }} plan. 
                Upgrade to add more transactions.
              </p>
            </div>
          </div>
        </div>

        <!-- Account Limit Warning -->
        <div v-if="!subscriptionInfo.can_add_account" class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Account Limit Reached</h3>
              <p class="text-sm text-red-700 mt-1">
                You've reached your account limit for the {{ subscriptionInfo.subscription_name }} plan. 
                Upgrade to add more accounts.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      
      <!-- Approaching Limit Warnings -->
      <div class="space-y-3">
        <!-- Transaction approaching limit -->
        <div v-if="subscriptionInfo.can_add_transaction && subscriptionInfo.current_transactions >= subscriptionInfo.max_transactions * 0.8" 
             class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">Approaching Transaction Limit</h3>
              <p class="text-sm text-yellow-700 mt-1">
                You're approaching your transaction limit. Consider upgrading your plan.
              </p>
            </div>
          </div>
        </div>

        <!-- Account approaching limit -->
        <div v-if="subscriptionInfo.can_add_account && subscriptionInfo.current_accounts >= subscriptionInfo.max_accounts * 0.8" 
             class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">Approaching Account Limit</h3>
              <p class="text-sm text-yellow-700 mt-1">
                You're approaching your account limit. Consider upgrading your plan.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Subscription Plans -->
    <div v-if="subscriptionLimits" class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div v-for="(plan, key) in subscriptionLimits" :key="key"
           class="bg-white rounded-lg shadow p-6 border-2 transition-colors duration-200"
           :class="subscriptionInfo?.subscription_type === key ? 'border-blue-500' : 'border-gray-200 hover:border-gray-300'">
        
        <div class="text-center">
          <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ plan.name }}</h4>
          <div class="text-sm text-gray-600 mb-4 space-y-1">
            <p>Up to {{ plan.max_transactions }} transactions</p>
            <p>Up to {{ plan.max_accounts }} accounts</p>
          </div>
          
          <!-- Features -->
          <div class="mb-6">
            <ul class="text-sm text-gray-600 space-y-1">
              <li>{{ plan.max_transactions }} transactions</li>
              <li>{{ plan.max_accounts }} accounts</li>
              <li v-if="key !== 'free'">Priority support</li>
              <li v-if="key === 'pro'">Advanced analytics</li>
            </ul>
          </div>
          
          <!-- Action Button -->
          <button v-if="subscriptionInfo?.subscription_type !== key"
                  @click="upgradeSubscription(key as string)"
                  :disabled="updating"
                  class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200">
            <span v-if="updating">Updating...</span>
            <span v-else-if="key === 'free'">Downgrade to Free</span>
            <span v-else>Upgrade to {{ plan.name }}</span>
          </button>
          
          <div v-else class="w-full bg-green-100 text-green-800 font-medium py-2 px-4 rounded-md">
            Current Plan
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { subscriptionAPI } from '@/services/api';
import { useFinanceStore } from '@/stores/finance';
import { useAuthStore } from '@/stores/auth';
import type { SubscriptionLimits } from '@/types';

const financeStore = useFinanceStore();
const authStore = useAuthStore();

const subscriptionInfo = computed(() => financeStore.subscriptionInfo);
const loading = ref(false);
const updating = ref(false);
const subscriptionLimits = ref<SubscriptionLimits | null>(null);

const getSubscriptionBadgeClass = (type: string) => {
  switch (type) {
    case 'free':
      return 'bg-gray-100 text-gray-800';
    case 'plus':
      return 'bg-blue-100 text-blue-800';
    case 'pro':
      return 'bg-purple-100 text-purple-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const getProgressBarClass = (type: string) => {
  switch (type) {
    case 'free':
      return 'bg-gray-600';
    case 'plus':
      return 'bg-blue-600';
    case 'pro':
      return 'bg-purple-600';
    default:
      return 'bg-gray-600';
  }
};

const upgradeSubscription = async (subscriptionType: string) => {
  updating.value = true;
  try {
    await subscriptionAPI.updateSubscription(subscriptionType);
    // Refresh user info and subscription info
    await authStore.initializeAuth();
    await financeStore.fetchSubscriptionInfo();
  } catch (error) {
    console.error('Failed to update subscription:', error);
    alert('Failed to update subscription. Please try again.');
  } finally {
    updating.value = false;
  }
};

const fetchSubscriptionLimits = async () => {
  try {
    subscriptionLimits.value = await subscriptionAPI.getLimits();
  } catch (error) {
    console.error('Failed to fetch subscription limits:', error);
  }
};

onMounted(async () => {
  loading.value = true;
  try {
    await Promise.all([
      financeStore.fetchSubscriptionInfo(),
      fetchSubscriptionLimits()
    ]);
  } finally {
    loading.value = false;
  }
});
</script>