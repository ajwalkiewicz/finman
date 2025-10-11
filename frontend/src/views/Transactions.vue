<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-semibold text-gray-900">Finance Manager</router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </router-link>
            <span class="text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">
              Transactions
            </span>
            <router-link to="/accounts" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Accounts
            </router-link>
            <router-link to="/analytics" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Analytics
            </router-link>
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

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-gray-900">Transactions</h1>
          <button
            @click="showModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Add Transaction
          </button>
        </div>

        <!-- Transaction List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <div class="px-4 py-5 sm:px-6">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">All Transactions</h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500">Manage your household transactions</p>
              </div>
              <div class="flex items-center space-x-2">
                <label for="sort-select" class="text-sm font-medium text-gray-700">Sort by:</label>
                <select 
                  id="sort-select"
                  v-model="sortBy" 
                  @change="updateSort"
                  class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="day">Day</option>
                  <option value="title">Transaction Name</option>
                  <option value="origin_account">From Account</option>
                  <option value="destination_account">To Account</option>
                  <option value="amount">Amount</option>
                </select>
                <button 
                  @click="toggleSortDirection"
                  class="p-2 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  :title="sortDirection === 'asc' ? 'Sort ascending' : 'Sort descending'"
                >
                  <svg class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('title')" style="width: 20%; min-width: 120px; max-width: 200px;">
                    <div class="flex items-center space-x-1">
                      <span>Transaction</span>
                      <svg v-if="sortBy === 'title'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('origin_account')">
                    <div class="flex items-center space-x-1">
                      <span>From Account</span>
                      <svg v-if="sortBy === 'origin_account'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('destination_account')">
                    <div class="flex items-center space-x-1">
                      <span>To Account</span>
                      <svg v-if="sortBy === 'destination_account'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('amount')">
                    <div class="flex items-center space-x-1">
                      <span>Amount</span>
                      <svg v-if="sortBy === 'amount'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('day')">
                    <div class="flex items-center space-x-1">
                      <span>Day</span>
                      <svg v-if="sortBy === 'day'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="transaction in sortedTransactions" :key="transaction.id" class="hover:bg-gray-50">
                  <td class="px-4 py-4" style="width: 20%; min-width: 120px; max-width: 200px;">
                    <div class="flex items-center">
                      <div class="flex-shrink-0">
                        <div class="w-3 h-3 rounded-full" :class="getTransactionTypeColor(transaction)"></div>
                      </div>
                      <div class="ml-4 min-w-0 flex-1">
                        <div class="text-sm font-medium text-gray-900 break-words">{{ transaction.title }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                      :class="getAccountBadgeClass(transaction.origin_account)"
                      :style="getAccountBadgeStyle(transaction.origin_account)"
                    >
                      {{ transaction.origin_account || '-' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                      :class="getAccountBadgeClass(transaction.destination_account)"
                      :style="getAccountBadgeStyle(transaction.destination_account)"
                    >
                      {{ transaction.destination_account || '-' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatCurrency(transaction.amount, transaction.currency) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ transaction.day_of_month }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                    {{ transaction.description }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex space-x-2">
                      <button
                        @click="editTransaction(transaction)"
                        class="inline-flex items-center text-indigo-600 hover:text-indigo-900"
                      >
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                        Edit
                      </button>
                      <button
                        @click="deleteTransaction(transaction.id!)"
                        class="inline-flex items-center text-red-600 hover:text-red-900"
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
          </div>
          
          <div v-if="financeStore.transactions.length === 0" class="text-center py-12">
            <p class="text-gray-500">No transactions found. Add your first transaction to get started.</p>
          </div>
        </div>

        <!-- Transaction Modal -->
        <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div class="mt-3">
              <h3 class="text-lg font-medium text-gray-900 mb-4">
                {{ editingTransaction ? 'Edit Transaction' : 'Add Transaction' }}
              </h3>
              
              <form @submit.prevent="handleSubmit" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Title</label>
                  <input
                    v-model="form.title"
                    type="text"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Origin Account</label>
                  <select
                    v-model="form.origin_account"
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">No source (Income)</option>
                    <option v-for="account in financeStore.accounts" :key="account.id" :value="account.name">
                      {{ account.name }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Destination Account</label>
                  <select
                    v-model="form.destination_account"
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">Expense (No destination)</option>
                    <option v-for="account in financeStore.accounts" :key="account.id" :value="account.name">
                      {{ account.name }}
                    </option>
                  </select>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Amount</label>
                    <input
                      v-model.number="form.amount"
                      type="number"
                      step="0.01"
                      min="0"
                      required
                      class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">Currency</label>
                    <select
                      v-model="form.currency"
                      required
                      class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="PLN">PLN</option>
                      <option value="EUR">EUR</option>
                      <option value="USD">USD</option>
                      <option value="GTQ">GTQ</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Day of Month</label>
                  <input
                    v-model.number="form.day_of_month"
                    type="number"
                    min="1"
                    max="31"
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    v-model="form.description"
                    rows="3"
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  ></textarea>
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
                    {{ submitting ? 'Saving...' : (editingTransaction ? 'Update' : 'Add') }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useFinanceStore } from '@/stores/finance';
import type { Transaction } from '@/types';

const authStore = useAuthStore();
const financeStore = useFinanceStore();

const showModal = ref(false);
const editingTransaction = ref<Transaction | null>(null);
const submitting = ref(false);

// Sorting state
const sortBy = ref<string>('day');
const sortDirection = ref<'asc' | 'desc'>('asc');

const form = reactive({
  title: '',
  origin_account: null as string | null,
  destination_account: null as string | null,
  amount: 0,
  currency: 'PLN',
  day_of_month: 1,
  description: ''
});

// Sorted transactions computed property
const sortedTransactions = computed(() => {
  const transactions = [...financeStore.transactions];
  
  transactions.sort((a: Transaction, b: Transaction) => {
    let aValue: any;
    let bValue: any;
    
    switch (sortBy.value) {
      case 'title':
        aValue = a.title?.toLowerCase() || '';
        bValue = b.title?.toLowerCase() || '';
        break;
      case 'origin_account':
        aValue = a.origin_account?.toLowerCase() || '';
        bValue = b.origin_account?.toLowerCase() || '';
        break;
      case 'destination_account':
        aValue = a.destination_account?.toLowerCase() || '';
        bValue = b.destination_account?.toLowerCase() || '';
        break;
      case 'amount':
        aValue = a.amount || 0;
        bValue = b.amount || 0;
        break;
      case 'day':
      default:
        aValue = a.day_of_month || 0;
        bValue = b.day_of_month || 0;
        break;
    }
    
    if (sortDirection.value === 'asc') {
      return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
    } else {
      return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
    }
  });
  
  return transactions;
});

// Sorting methods
const setSortBy = (field: string) => {
  if (sortBy.value === field) {
    toggleSortDirection();
  } else {
    sortBy.value = field;
    sortDirection.value = 'asc';
  }
};

const toggleSortDirection = () => {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
};

const updateSort = () => {
  // This is called when the select dropdown changes
  // The sortBy value is already updated by v-model
  sortDirection.value = 'asc';
};

const getTransactionTypeColor = (transaction: any) => {
  if (transaction.origin_account === 'Income') {
    return 'bg-green-400'; // Income
  } else if (transaction.destination_account === 'Expense') {
    return 'bg-red-400'; // Expense
  } else {
    return 'bg-blue-400'; // Transfer
  }
};

const getAccountBadgeClass = (accountName: string | null) => {
  if (!accountName) return 'bg-gray-100 text-gray-800';
  
  // Find the account by name to get its color
  const account = financeStore.accounts.find(acc => acc.name === accountName);
  if (account?.label_color) {
    return '';  // Return empty string to use inline styles instead
  }
  
  // Fallback to predefined colors for system accounts
  switch (accountName) {
    case 'Income':
      return 'bg-green-100 text-green-800';
    case 'Expense':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const getAccountBadgeStyle = (accountName: string | null) => {
  if (!accountName) return {};
  
  // Find the account by name to get its color
  const account = financeStore.accounts.find(acc => acc.name === accountName);
  if (account?.label_color) {
    // Convert hex color to RGB for background with opacity
    const hex = account.label_color.replace('#', '');
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);
    
    return {
      backgroundColor: `rgba(${r}, ${g}, ${b}, 0.1)`,
      color: account.label_color,
      borderColor: `rgba(${r}, ${g}, ${b}, 0.3)`,
      border: '1px solid'
    };
  }
  
  return {};
};

const formatCurrency = (amount: number, currency: string) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount) + ' ' + currency;
};

const resetForm = () => {
  form.title = '';
  form.origin_account = null;
  form.destination_account = null;
  form.amount = 0;
  form.currency = 'PLN';
  form.day_of_month = 1;
  form.description = '';
};

const closeModal = () => {
  showModal.value = false;
  editingTransaction.value = null;
  resetForm();
};

const editTransaction = (transaction: Transaction) => {
  editingTransaction.value = transaction;
  form.title = transaction.title;
  form.origin_account = transaction.origin_account;
  form.destination_account = transaction.destination_account;
  form.amount = transaction.amount;
  form.currency = transaction.currency;
  form.day_of_month = transaction.day_of_month;
  form.description = transaction.description;
  showModal.value = true;
};

const handleSubmit = async () => {
  submitting.value = true;
  try {
    if (editingTransaction.value) {
      await financeStore.updateTransaction(editingTransaction.value.id!, form);
    } else {
      await financeStore.createTransaction(form);
    }
    closeModal();
  } catch (error) {
    console.error('Failed to save transaction:', error);
  } finally {
    submitting.value = false;
  }
};

const deleteTransaction = async (id: number) => {
  if (confirm('Are you sure you want to delete this transaction?')) {
    try {
      await financeStore.deleteTransaction(id);
    } catch (error) {
      console.error('Failed to delete transaction:', error);
    }
  }
};

onMounted(async () => {
  await Promise.all([
    financeStore.fetchTransactions(),
    financeStore.fetchAccounts()
  ]);
});
</script>