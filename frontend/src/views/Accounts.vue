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
            <router-link to="/transactions" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Transactions
            </router-link>
            <span class="text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">
              Accounts
            </span>
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
          <h1 class="text-2xl font-bold text-gray-900">Accounts</h1>
          <button
            @click="showModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Add Account
          </button>
        </div>

        <!-- Account List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-md mb-8">
          <ul class="divide-y divide-gray-200">
            <li v-for="account in financeStore.accounts" :key="account.id" class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-10 h-10 bg-indigo-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-sm font-semibold">{{ account.name.charAt(0).toUpperCase() }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ account.name }}</div>
                    <div class="text-sm text-gray-500">{{ account.account_type }}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div v-if="financeStore.accountFlow[account.name]" class="text-sm text-gray-900">
                    <div class="text-green-600">+{{ formatCurrency(financeStore.accountFlow[account.name].incoming) }}</div>
                    <div class="text-red-600">-{{ formatCurrency(financeStore.accountFlow[account.name].outgoing) }}</div>
                  </div>
                </div>
              </div>
            </li>
          </ul>
          
          <div v-if="financeStore.accounts.length === 0" class="text-center py-12">
            <p class="text-gray-500">No accounts found. Add your first account to get started.</p>
          </div>
        </div>

        <!-- Account Flow Summary -->
        <div v-if="Object.keys(financeStore.accountFlow).length > 0" class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Money Flow Between Accounts</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                v-for="(flow, accountName) in financeStore.accountFlow"
                :key="accountName"
                class="border border-gray-200 rounded-lg p-4"
              >
                <h4 class="font-medium text-gray-900 mb-2">{{ accountName }}</h4>
                <div class="space-y-1">
                  <div class="flex justify-between text-sm">
                    <span class="text-green-600">Incoming:</span>
                    <span class="text-green-600 font-medium">{{ formatCurrency(flow.incoming) }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="text-red-600">Outgoing:</span>
                    <span class="text-red-600 font-medium">{{ formatCurrency(flow.outgoing) }}</span>
                  </div>
                  <hr class="my-2">
                  <div class="flex justify-between text-sm font-medium">
                    <span class="text-gray-900">Net:</span>
                    <span :class="flow.incoming - flow.outgoing >= 0 ? 'text-green-600' : 'text-red-600'">
                      {{ formatCurrency(flow.incoming - flow.outgoing) }}
                    </span>
                  </div>
                </div>
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
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useFinanceStore } from '@/stores/finance';

const authStore = useAuthStore();
const financeStore = useFinanceStore();

const showModal = ref(false);
const submitting = ref(false);

const form = reactive({
  name: '',
  account_type: 'bank'
});

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('pl-PL', {
    style: 'currency',
    currency: 'PLN',
    minimumFractionDigits: 2
  }).format(amount);
};

const resetForm = () => {
  form.name = '';
  form.account_type = 'bank';
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const handleSubmit = async () => {
  submitting.value = true;
  try {
    await financeStore.createAccount(form);
    closeModal();
  } catch (error) {
    console.error('Failed to create account:', error);
  } finally {
    submitting.value = false;
  }
};

onMounted(async () => {
  await Promise.all([
    financeStore.fetchAccounts(),
    financeStore.fetchAnalytics()
  ]);
});
</script>