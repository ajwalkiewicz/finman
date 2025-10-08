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
            <router-link to="/accounts" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
              Accounts
            </router-link>
            <span class="text-indigo-600 px-3 py-2 rounded-md text-sm font-medium">
              Analytics
            </span>
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
        <h1 class="text-2xl font-bold text-gray-900 mb-6">Analytics</h1>

        <!-- Base Currency Selection -->
        <div class="bg-white shadow sm:rounded-lg mb-8">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Exchange Rates</h3>
            <div class="flex items-center space-x-4 mb-4">
              <label for="base-currency" class="text-sm font-medium text-gray-700">Base Currency:</label>
              <select 
                id="base-currency"
                v-model="baseCurrency" 
                @change="handleCurrencyChange"
                class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="PLN">PLN</option>
                <option value="EUR">EUR</option>
                <option value="USD">USD</option>
                <option value="GTQ">GTQ</option>
              </select>
            </div>
            
            <!-- Exchange Rate Cards -->
            <div v-if="exchangeRates" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div 
                v-for="(rate, currency) in exchangeRates.rates" 
                :key="currency"
                class="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                :class="{ 'ring-2 ring-indigo-500 bg-indigo-50': currency === baseCurrency }"
                @click="setBaseCurrency(String(currency))"
              >
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-sm font-medium text-gray-500">1 {{ baseCurrency }} =</div>
                    <div class="text-lg font-bold text-gray-900">
                      {{ rate.toFixed(4) }} {{ currency }}
                    </div>
                  </div>
                  <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-semibold"
                       :class="getCurrencyColor(String(currency))">
                    {{ String(currency).substring(0, 2) }}
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="exchangeRates" class="mt-4 text-sm text-gray-500">
              Data fetched: {{ formatTimestamp(exchangeRates.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Expense Summary -->
        <div v-if="financeStore.expenseSummary" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <span class="text-white text-sm font-semibold">PLN</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">PLN Expenses</dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ formatCurrency(financeStore.expenseSummary.total_expense_pln, 'PLN') }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span class="text-white text-sm font-semibold">EUR</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">EUR Expenses</dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ formatCurrency(financeStore.expenseSummary.total_expense_eur, 'EUR') }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                    <span class="text-white text-sm font-semibold">USD</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">USD Expenses</dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ formatCurrency(financeStore.expenseSummary.total_expense_usd, 'USD') }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                    <span class="text-white text-sm font-semibold">GTQ</span>
                  </div>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">GTQ Expenses</dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ formatCurrency(financeStore.expenseSummary.total_expense_gtq, 'GTQ') }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Expenses by Category -->
        <div v-if="financeStore.expenseSummary && Object.keys(financeStore.expenseSummary.by_category).length > 0" class="bg-white shadow sm:rounded-lg mb-8">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Expenses by Category</h3>
            
            <div class="space-y-3">
              <div
                v-for="(amount, category) in sortedCategories"
                :key="category"
                class="flex items-center justify-between"
              >
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-indigo-500 rounded mr-3"></div>
                  <span class="text-sm font-medium text-gray-900">{{ category }}</span>
                </div>
                <span class="text-sm text-gray-600">{{ formatCurrency(amount, 'PLN') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Flow -->
        <div v-if="Object.keys(financeStore.accountFlow).length > 0" class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-6">Account Flow Analysis</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div
                v-for="(flow, accountName) in financeStore.accountFlow"
                :key="accountName"
                class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <h4 class="font-medium text-gray-900 mb-3 text-center">{{ accountName }}</h4>
                
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600">Incoming:</span>
                    <span class="text-sm font-medium text-green-600">
                      +{{ formatCurrency(flow.incoming, 'PLN') }}
                    </span>
                  </div>
                  
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600">Outgoing:</span>
                    <span class="text-sm font-medium text-red-600">
                      -{{ formatCurrency(flow.outgoing, 'PLN') }}
                    </span>
                  </div>
                  
                  <hr class="my-2">
                  
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-semibold text-gray-900">Net Flow:</span>
                    <span 
                      class="text-sm font-bold"
                      :class="flow.incoming - flow.outgoing >= 0 ? 'text-green-600' : 'text-red-600'"
                    >
                      {{ flow.incoming - flow.outgoing >= 0 ? '+' : '' }}{{ formatCurrency(flow.incoming - flow.outgoing, 'PLN') }}
                    </span>
                  </div>
                </div>

                <!-- Flow visualization bar -->
                <div class="mt-3">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full transition-all duration-300"
                      :class="flow.incoming - flow.outgoing >= 0 ? 'bg-green-500' : 'bg-red-500'"
                      :style="{ width: getFlowPercentage(flow) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!financeStore.expenseSummary && Object.keys(financeStore.accountFlow).length === 0" class="text-center py-12">
          <p class="text-gray-500">No data available for analysis. Add some transactions to get started.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useFinanceStore } from '@/stores/finance';
import { exchangeRatesAPI } from '@/services/api';
import type { ExchangeRatesResponse } from '@/types';

const authStore = useAuthStore();
const financeStore = useFinanceStore();

// Exchange rates state with localStorage persistence
const baseCurrency = ref<string>(localStorage.getItem('baseCurrency') || 'PLN');
const exchangeRates = ref<ExchangeRatesResponse | null>(null);

const sortedCategories = computed(() => {
  if (!financeStore.expenseSummary) return {};
  
  const entries = Object.entries(financeStore.expenseSummary.by_category);
  entries.sort((a, b) => b[1] - a[1]); // Sort by amount descending
  
  return Object.fromEntries(entries);
});

const maxFlow = computed(() => {
  if (Object.keys(financeStore.accountFlow).length === 0) return 1;
  
  return Math.max(
    ...Object.values(financeStore.accountFlow).map(flow => 
      Math.abs(flow.incoming - flow.outgoing)
    )
  );
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

const handleCurrencyChange = async () => {
  localStorage.setItem('baseCurrency', baseCurrency.value);
  await fetchExchangeRates();
};

const setBaseCurrency = async (currency: string) => {
  baseCurrency.value = currency;
  localStorage.setItem('baseCurrency', currency);
  await fetchExchangeRates();
};

const getCurrencyColor = (currency: string) => {
  const colors: { [key: string]: string } = {
    'PLN': 'bg-green-500',
    'EUR': 'bg-blue-500',
    'USD': 'bg-purple-500',
    'GTQ': 'bg-orange-500'
  };
  return colors[currency] || 'bg-gray-500';
};

const formatCurrency = (amount: number, currency: string) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount) + ' ' + currency;
};

const formatTimestamp = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  });
};

const getFlowPercentage = (flow: { incoming: number; outgoing: number }) => {
  const netFlow = Math.abs(flow.incoming - flow.outgoing);
  return Math.max(10, (netFlow / maxFlow.value) * 100); // Minimum 10% for visibility
};

onMounted(async () => {
  await Promise.all([
    financeStore.fetchTransactions(),
    financeStore.fetchAccounts(),
    financeStore.fetchAnalytics(),
    fetchExchangeRates()
  ]);
});
</script>