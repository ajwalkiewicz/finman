<template>
    <main class="max-w-7xl mx-auto py-4 sm:py-6 px-4 sm:px-6 lg:px-8">
      <div class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-4 sm:space-y-0">
          <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Accounts</h1>
          <button
            @click="showModal = true"
            :disabled="!subscriptionInfo?.can_add_account"
            class="inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white w-full sm:w-auto"
            :class="subscriptionInfo?.can_add_account ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-400 cursor-not-allowed'"
          >
            Add Account
          </button>
        </div>

        <!-- Subscription Status Warning -->
        <div v-if="subscriptionInfo && !subscriptionInfo.can_add_account" 
             class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Account Limit Reached</h3>
              <p class="text-sm text-red-700 mt-1">
                You've used {{ subscriptionInfo.current_accounts }} of {{ subscriptionInfo.max_accounts }} 
                accounts allowed in your {{ subscriptionInfo.subscription_name }} plan. 
                <router-link to="/settings" class="font-medium underline hover:text-red-900">
                  Upgrade your subscription
                </router-link> to add more accounts.
              </p>
            </div>
          </div>
        </div>

        <div v-else-if="subscriptionInfo && subscriptionInfo.current_accounts >= subscriptionInfo.max_accounts * 0.8" 
             class="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-6">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">Approaching Account Limit</h3>
              <p class="text-sm text-yellow-700 mt-1">
                You've used {{ subscriptionInfo.current_accounts }} of {{ subscriptionInfo.max_accounts }} 
                accounts. Consider 
                <router-link to="/settings" class="font-medium underline hover:text-yellow-900">
                  upgrading your subscription
                </router-link> to avoid hitting the limit.
              </p>
            </div>
          </div>
        </div>

        <!-- Account List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th 
                      @click="setSortBy('name')"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Account Name</span>
                        <svg v-if="sortBy === 'name'" :class="sortDirection === 'asc' ? 'transform rotate-180' : ''" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                      </div>
                    </th>
                    <th 
                      @click="setSortBy('account_type')"
                      class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Type</span>
                        <svg v-if="sortBy === 'account_type'" :class="sortDirection === 'asc' ? 'transform rotate-180' : ''" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                      </div>
                    </th>
                    <th 
                      @click="setSortBy('base_currency')"
                      class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Currency</span>
                        <svg v-if="sortBy === 'base_currency'" :class="sortDirection === 'asc' ? 'transform rotate-180' : ''" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                      </div>
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Flow Summary
                    </th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="account in sortedAccounts" :key="account.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                          <div 
                            class="w-10 h-10 rounded-full flex items-center justify-center"
                            :style="{ backgroundColor: account.label_color || '#3B82F6' }"
                          >
                            <span class="text-white text-sm font-semibold">{{ account.name.charAt(0).toUpperCase() }}</span>
                          </div>
                        </div>
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900">{{ account.name }}</div>
                          <div class="text-sm text-gray-500">{{ account.created_at ? formatDate(account.created_at) : 'N/A' }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getAccountTypeClass(account.account_type)">
                        {{ formatAccountType(account.account_type) }}
                      </span>
                    </td>
                    <td class="px-4 py-4 whitespace-nowrap">
                      <button 
                        @click="openCurrencyModal(account)"
                        :disabled="account.account_type === 'system'"
                        class="inline-flex items-center px-3 py-1 text-sm font-medium rounded-full bg-gray-100 text-gray-800 hover:bg-gray-200 transition-colors duration-200 disabled:cursor-not-allowed disabled:hover:bg-gray-100"
                        :title="account.account_type === 'system' ? 'System account currency cannot be changed' : 'Click to change base currency'"
                      >
                        {{ account.base_currency || 'PLN' }}
                      </button>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <template v-if="getAccountFlowInBaseCurrency(account.name)">
                        <div class="text-sm">
                          <div class="flex justify-between items-center mb-1">
                            <span class="text-green-600 text-xs">In:</span>
                            <span class="text-green-600 font-medium text-xs">{{ formatCurrency(getAccountFlowInBaseCurrency(account.name)!.incoming, getAccountFlowInBaseCurrency(account.name)!.currency) }}</span>
                          </div>
                          <div class="flex justify-between items-center mb-1">
                            <span class="text-red-600 text-xs">Out:</span>
                            <span class="text-red-600 font-medium text-xs">{{ formatCurrency(getAccountFlowInBaseCurrency(account.name)!.outgoing, getAccountFlowInBaseCurrency(account.name)!.currency) }}</span>
                          </div>
                          <div class="flex justify-between items-center pt-1 border-t border-gray-200">
                            <span class="text-gray-900 text-xs font-medium">Net:</span>
                            <span class="font-medium text-xs" :class="getAccountFlowInBaseCurrency(account.name)!.net >= 0 ? 'text-green-600' : 'text-red-600'">
                              {{ formatCurrency(getAccountFlowInBaseCurrency(account.name)!.net, getAccountFlowInBaseCurrency(account.name)!.currency) }}
                            </span>
                          </div>
                        </div>
                      </template>
                      <span v-else class="text-sm text-gray-400">No flow data</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div class="flex items-center justify-end space-x-3">
                        <button
                          @click="openEditModal(account)"
                          :disabled="account.account_type === 'system'"
                          class="inline-flex items-center text-indigo-600 hover:text-indigo-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                          :title="account.account_type === 'system' ? 'System accounts cannot be edited' : 'Edit account'"
                        >
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                          </svg>
                          Edit
                        </button>
                        <button
                          @click="confirmDelete(account)"
                          :disabled="account.account_type === 'system'"
                          class="inline-flex items-center text-red-600 hover:text-red-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                          :title="account.account_type === 'system' ? 'System accounts cannot be deleted' : 'Delete account'"
                        >
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                          </svg>
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              
              <div v-if="filteredAccounts.length === 0" class="text-center py-12">
                <p class="text-gray-500">No accounts found. Add your first account to get started.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Modal -->
        <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div class="mt-3">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Add Account</h3>
              
              <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Account Name</label>
                  <input
                    v-model="form.name"
                    type="text"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="e.g., Millenium, Santander, Cash"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Account Type</label>
                  <select
                    v-model="form.account_type"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="bank">Bank Account</option>
                    <option value="card">Credit/Debit Card</option>
                    <option value="wallet">Digital Wallet</option>
                    <option value="cash">Cash</option>
                    <option value="investment">Investment Account</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Base Currency</label>
                  <select
                    v-model="form.base_currency"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="PLN">PLN (Polish Złoty)</option>
                    <option value="EUR">EUR (Euro)</option>
                    <option value="USD">USD (US Dollar)</option>
                    <option value="GTQ">GTQ (Guatemalan Quetzal)</option>
                  </select>
                  <p class="mt-1 text-xs text-gray-500">This currency will be used for account balance calculations and flow displays.</p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Label Color</label>
                  <div class="mt-2 flex items-center space-x-3">
                    <input
                      v-model="form.label_color"
                      type="color"
                      class="h-8 w-16 border border-gray-300 rounded cursor-pointer"
                    />
                    <span class="text-sm text-gray-600">{{ form.label_color }}</span>
                  </div>
                  <p class="mt-1 text-xs text-gray-500">Choose a color to help identify this account visually.</p>
                </div>

                <div class="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    @click="closeModal"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    :disabled="submitting"
                    class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {{ submitting ? 'Adding...' : 'Add Account' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Currency Change Modal -->
        <div v-if="showCurrencyModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div class="mt-3">
              <h3 class="text-lg font-medium text-gray-900 mb-4">
                Change Base Currency for {{ selectedAccount?.name }}
              </h3>
              
              <div class="space-y-3">
                <p class="text-sm text-gray-600 mb-4">
                  Select the new base currency for this account. All transaction flows will be converted and displayed in this currency.
                </p>
                
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="currency in ['PLN', 'EUR', 'USD', 'GTQ']"
                    :key="currency"
                    @click="updateAccountCurrency(currency)"
                    :disabled="currencySubmitting || selectedAccount?.base_currency === currency"
                    :class="[
                      'px-4 py-3 text-sm font-medium rounded-md border transition-colors duration-200',
                      selectedAccount?.base_currency === currency
                        ? 'bg-indigo-100 border-indigo-300 text-indigo-700 cursor-not-allowed'
                        : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400'
                    ]"
                  >
                    {{ currency }}
                    <span v-if="selectedAccount?.base_currency === currency" class="ml-1 text-xs">(current)</span>
                  </button>
                </div>

                <div class="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    @click="closeCurrencyModal"
                    :disabled="currencySubmitting"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 disabled:opacity-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit Account Modal -->
        <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div class="mt-3">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Account</h3>
              
              <form @submit.prevent="handleEditSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Account Name</label>
                  <input
                    v-model="editForm.name"
                    type="text"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="e.g., Millenium, Santander, Cash"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Account Type</label>
                  <select
                    v-model="editForm.account_type"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="bank">Bank Account</option>
                    <option value="card">Credit/Debit Card</option>
                    <option value="wallet">Digital Wallet</option>
                    <option value="cash">Cash</option>
                    <option value="investment">Investment Account</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Base Currency</label>
                  <select
                    v-model="editForm.base_currency"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="PLN">PLN (Polish Złoty)</option>
                    <option value="EUR">EUR (Euro)</option>
                    <option value="USD">USD (US Dollar)</option>
                    <option value="GTQ">GTQ (Guatemalan Quetzal)</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Label Color</label>
                  <div class="mt-2 flex items-center space-x-3">
                    <input
                      v-model="editForm.label_color"
                      type="color"
                      class="h-8 w-16 border border-gray-300 rounded cursor-pointer"
                    />
                    <span class="text-sm text-gray-600">{{ editForm.label_color }}</span>
                  </div>
                  <p class="mt-1 text-xs text-gray-500">Choose a color to help identify this account visually.</p>
                </div>

                <div class="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    @click="closeEditModal"
                    :disabled="editSubmitting"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 disabled:opacity-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    :disabled="editSubmitting"
                    class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    {{ editSubmitting ? 'Updating...' : 'Update Account' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div class="mt-3">
              <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.232 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                </svg>
              </div>
              
              <h3 class="text-lg font-medium text-gray-900 text-center mb-2">Delete Account</h3>
              
              <p class="text-sm text-gray-600 text-center mb-4">
                Are you sure you want to delete the account "<strong>{{ selectedAccount?.name }}</strong>"? 
                This action cannot be undone.
              </p>
              
              <div class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <p class="text-xs text-yellow-800">
                  <strong>Warning:</strong> Deleting this account may affect existing transactions that reference it. Make sure to update or remove related transactions first.
                </p>
              </div>

              <div class="flex justify-center space-x-3">
                <button
                  type="button"
                  @click="closeDeleteModal"
                  :disabled="deleteSubmitting"
                  class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  @click="handleDelete"
                  :disabled="deleteSubmitting"
                  class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 disabled:opacity-50"
                >
                  {{ deleteSubmitting ? 'Deleting...' : 'Delete Account' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import { exchangeRatesAPI } from '@/services/api';
import { accountsAPI } from '@/services/api';
import type { Account, ExchangeRatesResponse } from '@/types';


// Exchange rates state with localStorage persistence
const baseCurrency = ref<string>(localStorage.getItem('baseCurrency') || 'PLN');
const exchangeRates = ref<ExchangeRatesResponse | null>(null);

const financeStore = useFinanceStore();
const subscriptionInfo = computed(() => financeStore.subscriptionInfo);

const showModal = ref(false);
const showEditModal = ref(false);
const showCurrencyModal = ref(false);
const showDeleteModal = ref(false);
const selectedAccount = ref<Account | null>(null);
const currencySubmitting = ref(false);
const submitting = ref(false);
const editSubmitting = ref(false);
const deleteSubmitting = ref(false);

// Sorting state
const sortBy = ref<string>('name');
const sortDirection = ref<'asc' | 'desc'>('asc');

const form = reactive({
  name: '',
  account_type: 'bank',
  base_currency: 'PLN',
  label_color: '#3B82F6'
});

const editForm = reactive({
  name: '',
  account_type: 'bank',
  base_currency: 'PLN',
  label_color: '#3B82F6'
});

// Filter out Income and Expense accounts (internal calculation accounts)
const filteredAccounts = computed(() => {
  return financeStore.accounts.filter(account => 
    account.name !== 'Income' && account.name !== 'Expense'
  );
});

// Sorting functionality
const setSortBy = (field: string) => {
  if (sortBy.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortBy.value = field;
    sortDirection.value = 'asc';
  }
};

const sortedAccounts = computed(() => {
  const accounts = [...filteredAccounts.value];
  
  accounts.sort((a, b) => {
    let aValue: any;
    let bValue: any;
    
    switch (sortBy.value) {
      case 'name':
        aValue = a.name;
        bValue = b.name;
        break;
      case 'account_type':
        aValue = a.account_type;
        bValue = b.account_type;
        break;
      case 'base_currency':
        aValue = a.base_currency || 'PLN';
        bValue = b.base_currency || 'PLN';
        break;
      default:
        aValue = a.name;
        bValue = b.name;
    }
    
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      const comparison = aValue.toLowerCase().localeCompare(bValue.toLowerCase());
      return sortDirection.value === 'asc' ? comparison : -comparison;
    }
    
    return sortDirection.value === 'asc' ? 
      (aValue < bValue ? -1 : aValue > bValue ? 1 : 0) :
      (aValue > bValue ? -1 : aValue < bValue ? 1 : 0);
  });
  
  return accounts;
});

// Exchange rate functions
const fetchExchangeRates = async () => {
  try {
    const rates = await exchangeRatesAPI.getRates(baseCurrency.value);
    exchangeRates.value = rates;
  } catch (error) {
    console.error('Failed to fetch exchange rates:', error);
  }
};

// Currency conversion function
const convertAmount = (amount: number, fromCurrency: string, toCurrency: string): number => {
  if (!exchangeRates.value || fromCurrency === toCurrency) {
    return amount;
  }
  
  const rates = exchangeRates.value.rates;
  const fromRate = rates[fromCurrency] || 1;
  const toRate = rates[toCurrency] || 1;
  
  // Convert to base currency (PLN) first, then to target currency
  const amountInPLN = amount / fromRate;
  return amountInPLN * toRate;
};

// Calculate account flows in each account's base currency
const accountFlowsConverted = computed(() => {
  const converted: Record<string, any> = {};
  
  filteredAccounts.value.forEach(account => {
    const baseCurrency = account.base_currency || 'PLN';
    let incoming = 0;
    let outgoing = 0;
    
    // Calculate flows from individual transactions, converting each to the account's base currency
    financeStore.transactions.forEach(transaction => {
      // Skip transactions without proper data
      if (!transaction.currency || typeof transaction.amount !== 'number') {
        return;
      }
      
      const transactionCurrency = transaction.currency;
      const transactionAmount = transaction.amount;
      
      // Convert transaction amount to account's base currency
      const convertedAmount = convertAmount(transactionAmount, transactionCurrency, baseCurrency);
      
      // Debug logging for currency conversion
      if (transactionCurrency !== baseCurrency && (transaction.destination_account === account.name || transaction.origin_account === account.name)) {
        console.log(`Converting ${transactionAmount} ${transactionCurrency} to ${convertedAmount.toFixed(2)} ${baseCurrency} for account ${account.name}`);
      }
      
      // Check if this transaction affects this account
      if (transaction.destination_account === account.name) {
        // Money coming into this account
        incoming += convertedAmount;
      }
      
      if (transaction.origin_account === account.name) {
        // Money going out of this account
        outgoing += convertedAmount;
      }
    });
    
    converted[account.name] = {
      incoming: Math.round(incoming * 100) / 100, // Round to 2 decimal places
      outgoing: Math.round(outgoing * 100) / 100,
      net: Math.round((incoming - outgoing) * 100) / 100,
      currency: baseCurrency
    };
  });
  
  return converted;
});

const getAccountFlowInBaseCurrency = (accountName: string) => {
  return accountFlowsConverted.value[accountName] || null;
};

const formatCurrency = (amount: number, currency: string = 'PLN') => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount) + ' ' + currency;
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date);
};

const formatAccountType = (type: string) => {
  const typeMap: Record<string, string> = {
    'bank': 'Bank Account',
    'card': 'Credit/Debit Card',
    'wallet': 'Digital Wallet',
    'cash': 'Cash',
    'investment': 'Investment',
    'system': 'System',
    'other': 'Other'
  };
  return typeMap[type] || type;
};

const getAccountTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    'bank': 'bg-blue-100 text-blue-800',
    'card': 'bg-purple-100 text-purple-800',
    'wallet': 'bg-green-100 text-green-800',
    'cash': 'bg-yellow-100 text-yellow-800',
    'investment': 'bg-indigo-100 text-indigo-800',
    'system': 'bg-gray-100 text-gray-800',
    'other': 'bg-gray-100 text-gray-800'
  };
  return classMap[type] || 'bg-gray-100 text-gray-800';
};

const resetForm = () => {
  form.name = '';
  form.account_type = 'bank';
  form.base_currency = 'PLN';
  form.label_color = '#3B82F6';
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const handleSubmit = async () => {
  submitting.value = true;
  try {
    await financeStore.createAccount(form);
    
    // Refetch transactions to recalculate flows for the new account
    await financeStore.fetchTransactions();
    
    closeModal();
  } catch (error: any) {
    console.error('Failed to create account:', error);
    // Handle subscription limit error
    if (error?.type === 'subscription_limit_error') {
      alert(`Account Limit Reached: ${error.message}`);
    } else {
      alert('Failed to create account. Please try again.');
    }
  } finally {
    submitting.value = false;
  }
};

const openCurrencyModal = (account: Account) => {
  selectedAccount.value = account;
  showCurrencyModal.value = true;
};

const closeCurrencyModal = () => {
  showCurrencyModal.value = false;
  selectedAccount.value = null;
};

const updateAccountCurrency = async (newCurrency: string) => {
  if (!selectedAccount.value?.id) return;
  
  currencySubmitting.value = true;
  try {
    const updatedAccount = {
      name: selectedAccount.value.name,
      account_type: selectedAccount.value.account_type,
      base_currency: newCurrency,
      label_color: selectedAccount.value.label_color || '#3B82F6'
    };
    
    await accountsAPI.update(selectedAccount.value.id, updatedAccount);
    
    // Update the local store and refetch data
    await Promise.all([
      financeStore.fetchAccounts(),
      financeStore.fetchTransactions(),
      fetchExchangeRates()
    ]);
    
    closeCurrencyModal();
  } catch (error) {
    console.error('Failed to update account currency:', error);
  } finally {
    currencySubmitting.value = false;
  }
};

const openEditModal = (account: Account) => {
  selectedAccount.value = account;
  editForm.name = account.name;
  editForm.account_type = account.account_type;
  editForm.base_currency = account.base_currency || 'PLN';
  editForm.label_color = account.label_color || '#3B82F6';
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  selectedAccount.value = null;
  editForm.name = '';
  editForm.account_type = 'bank';
  editForm.base_currency = 'PLN';
  editForm.label_color = '#3B82F6';
};

const handleEditSubmit = async () => {
  if (!selectedAccount.value?.id) return;
  
  editSubmitting.value = true;
  try {
    await financeStore.updateAccount(selectedAccount.value.id, editForm);
    
    // Refetch all data including transactions and exchange rates
    await Promise.all([
      financeStore.fetchTransactions(),
      financeStore.fetchAnalytics(),
      fetchExchangeRates()
    ]);
    
    closeEditModal();
  } catch (error) {
    console.error('Failed to update account:', error);
  } finally {
    editSubmitting.value = false;
  }
};

const confirmDelete = (account: Account) => {
  selectedAccount.value = account;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  selectedAccount.value = null;
};

const handleDelete = async () => {
  if (!selectedAccount.value?.id) return;
  
  deleteSubmitting.value = true;
  try {
    await financeStore.deleteAccount(selectedAccount.value.id);
    
    // Refetch analytics and transactions after deletion
    await Promise.all([
      financeStore.fetchTransactions(),
      financeStore.fetchAnalytics()
    ]);
    
    closeDeleteModal();
  } catch (error) {
    console.error('Failed to delete account:', error);
  } finally {
    deleteSubmitting.value = false;
  }
};

onMounted(async () => {
  await Promise.all([
    financeStore.fetchAccounts(),
    financeStore.fetchTransactions(),
    financeStore.fetchAnalytics(),
    financeStore.fetchSubscriptionInfo(),
    fetchExchangeRates()
  ]);
});
</script>