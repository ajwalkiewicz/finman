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
          <ul class="divide-y divide-gray-200">
            <li v-for="transaction in financeStore.transactions" :key="transaction.id" class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-3 h-3 rounded-full" :class="transaction.is_expense ? 'bg-red-400' : 'bg-green-400'"></div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ transaction.title }}</div>
                    <div class="text-sm text-gray-500">{{ transaction.description }}</div>
                    <div class="text-xs text-gray-400">
                      {{ transaction.origin_account || 'No source' }} → {{ transaction.destination_account || 'Expense' }}
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <div class="text-right">
                    <div class="text-sm font-medium text-gray-900">
                      {{ formatCurrency(transaction.amount, transaction.currency) }}
                    </div>
                    <div class="text-sm text-gray-500">Day {{ transaction.day_of_month }}</div>
                  </div>
                  <div class="flex space-x-2">
                    <button
                      @click="editTransaction(transaction)"
                      class="text-indigo-600 hover:text-indigo-900 text-sm"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteTransaction(transaction.id!)"
                      class="text-red-600 hover:text-red-900 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </li>
          </ul>
          
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
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useFinanceStore } from '@/stores/finance';
import type { Transaction } from '@/types';

const authStore = useAuthStore();
const financeStore = useFinanceStore();

const showModal = ref(false);
const editingTransaction = ref<Transaction | null>(null);
const submitting = ref(false);

const form = reactive({
  title: '',
  origin_account: null as string | null,
  destination_account: null as string | null,
  amount: 0,
  currency: 'PLN',
  day_of_month: 1,
  description: ''
});

const formatCurrency = (amount: number, currency: string) => {
  return new Intl.NumberFormat('pl-PL', {
    style: 'currency',
    currency: currency === 'GTQ' ? 'PLN' : currency,
    minimumFractionDigits: 2
  }).format(amount) + (currency === 'GTQ' ? ' GTQ' : '');
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