<template>
    <main class="max-w-7xl mx-auto py-4 sm:py-6 px-4 sm:px-6 lg:px-8">
      <div class="space-y-6">
        <!-- Income and Expense Summary Cards -->
        <div v-if="financeStore.expenseSummary" class="mb-6">
          <!-- Base Currency Selection -->
          <div class="mb-4 bg-white rounded-lg p-4 shadow">
            <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4 space-y-2 sm:space-y-0">
              <label for="dashboard-base-currency" class="text-sm font-medium text-gray-700 flex-shrink-0">Base currency:</label>
              <select 
                id="dashboard-base-currency"
                v-model="baseCurrency" 
                @change="handleCurrencyChange"
                class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-auto"
              >
                <option value="PLN">PLN</option>
                <option value="EUR">EUR</option>
                <option value="USD">USD</option>
                <option value="GTQ">GTQ</option>
              </select>
              <span v-if="exchangeRates" class="text-xs text-gray-500 break-words">
                Rates from: {{ formatTimestamp(exchangeRates.timestamp) }}
              </span>
            </div>
          </div>

          <!-- First Row: Main Summary Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6">
            <!-- Total Income -->
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-sm font-semibold">+</span>
                    </div>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total Income</dt>
                      <dd class="text-lg font-medium text-gray-900">
                        {{ formatCurrency(totalIncomeConverted, baseCurrency) }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <!-- Total Expenses -->
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                      <span class="text-white text-sm font-semibold">-</span>
                    </div>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total Expenses</dt>
                      <dd class="text-lg font-medium text-gray-900">
                        {{ formatCurrency(totalExpensesConverted, baseCurrency) }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <!-- Net Balance -->
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center" :class="netBalanceConverted >= 0 ? 'bg-green-500' : 'bg-red-500'">
                      <span class="text-white text-sm font-semibold">{{ netBalanceConverted >= 0 ? '=' : '=' }}</span>
                    </div>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Net Balance</dt>
                      <dd class="text-lg font-medium" :class="netBalanceConverted >= 0 ? 'text-green-600' : 'text-red-600'">
                        {{ formatCurrency(netBalanceConverted, baseCurrency) }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Second Row: Currency-specific Expenses -->
          <div v-if="financeStore.expenseSummary" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6">
            <!-- PLN Expenses -->
            <div 
              class="bg-white overflow-hidden shadow rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md"
              :class="{ 'ring-2 ring-blue-500 bg-blue-50': baseCurrency === 'PLN' }"
              @click="setBaseCurrency('PLN')"
            >
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
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

            <!-- EUR Expenses -->
            <div 
              class="bg-white overflow-hidden shadow rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md"
              :class="{ 'ring-2 ring-purple-500 bg-purple-50': baseCurrency === 'EUR' }"
              @click="setBaseCurrency('EUR')"
            >
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
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

            <!-- USD Expenses -->
            <div 
              class="bg-white overflow-hidden shadow rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md"
              :class="{ 'ring-2 ring-green-500 bg-green-50': baseCurrency === 'USD' }"
              @click="setBaseCurrency('USD')"
            >
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
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

            <!-- GTQ Expenses -->
            <div 
              class="bg-white overflow-hidden shadow rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md"
              :class="{ 'ring-2 ring-orange-500 bg-orange-50': baseCurrency === 'GTQ' }"
              @click="setBaseCurrency('GTQ')"
            >
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
        </div>

        <!-- All Transactions -->
        <div class="bg-white shadow overflow-hidden sm:rounded-md mb-8">
          <div class="px-4 py-5 sm:px-6">
            <div class="space-y-4">
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">All Transactions</h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500">Complete list of household transactions</p>
              </div>
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-end space-y-2 sm:space-y-0 sm:space-x-2">
                <label for="sort-select" class="text-sm font-medium text-gray-700 sm:flex-shrink-0">Sort by:</label>
                <div class="flex items-center space-x-2">
                  <select 
                    id="sort-select"
                    v-model="sortBy" 
                    @change="updateSort"
                    class="flex-1 sm:flex-initial border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="day">Day</option>
                    <option value="title">Transaction Name</option>
                    <option value="origin_account">From Account</option>
                    <option value="destination_account">To Account</option>
                    <option value="amount">Amount</option>
                  </select>
                  <button 
                    @click="toggleSortDirection"
                    class="p-2 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 flex-shrink-0"
                    :title="sortDirection === 'asc' ? 'Sort ascending' : 'Sort descending'"
                  >
                    <svg class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('title')">
                    <div class="flex items-center space-x-1">
                      <span>Transaction</span>
                      <svg v-if="sortBy === 'title'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('origin_account')">
                    <div class="flex items-center space-x-1">
                      <span>From Account</span>
                      <svg v-if="sortBy === 'origin_account'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('destination_account')">
                    <div class="flex items-center space-x-1">
                      <span>To Account</span>
                      <svg v-if="sortBy === 'destination_account'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('amount')">
                    <div class="flex items-center space-x-1">
                      <span>Amount</span>
                      <svg v-if="sortBy === 'amount'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" @click="setSortBy('day')">
                    <div class="flex items-center space-x-1">
                      <span class="sm:hidden">Day</span>
                      <span class="hidden sm:inline">Day</span>
                      <svg v-if="sortBy === 'day'" class="w-4 h-4 transform transition-transform" :class="{ 'rotate-180': sortDirection === 'desc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                      </svg>
                    </div>
                  </th>
                  <th scope="col" class="hidden lg:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="transaction in sortedTransactions" :key="transaction.id" class="hover:bg-gray-50">
                  <td class="px-3 sm:px-6 py-4">
                    <div class="flex items-start">
                      <div class="flex-shrink-0 mt-1">
                        <div class="w-3 h-3 rounded-full" :class="getTransactionTypeColor(transaction)"></div>
                      </div>
                      <div class="ml-3 min-w-0 flex-1">
                        <div class="text-sm font-medium text-gray-900 truncate">{{ transaction.title }}</div>
                        <div class="sm:hidden text-xs text-gray-500 mt-1">
                          {{ transaction.origin_account }} → {{ transaction.destination_account }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="hidden sm:table-cell px-6 py-4 whitespace-nowrap">
                    <span 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                      :class="getAccountBadgeClass(transaction.origin_account)"
                      :style="getAccountBadgeStyle(transaction.origin_account)"
                    >
                      {{ transaction.origin_account || '-' }}
                    </span>
                  </td>
                  <td class="hidden sm:table-cell px-6 py-4 whitespace-nowrap">
                    <span 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                      :class="getAccountBadgeClass(transaction.destination_account)"
                      :style="getAccountBadgeStyle(transaction.destination_account)"
                    >
                      {{ transaction.destination_account || '-' }}
                    </span>
                  </td>
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatCurrency(transaction.amount, transaction.currency) }}
                  </td>
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ transaction.day_of_month }}
                  </td>
                  <td class="hidden lg:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ transaction.description }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
            <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
              <router-link
                to="/transactions"
                class="inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Manage Transactions
              </router-link>
              <router-link
                to="/accounts"
                class="inline-flex justify-center items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Manage Accounts
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import { exchangeRatesAPI } from '@/services/api';
import type { Transaction, ExchangeRatesResponse } from '@/types';

const financeStore = useFinanceStore();

// Sorting state
const sortBy = ref<string>('day');
const sortDirection = ref<'asc' | 'desc'>('asc');

// Exchange rate state with localStorage persistence
const baseCurrency = ref<string>(localStorage.getItem('baseCurrency') || 'PLN');
const exchangeRates = ref<ExchangeRatesResponse | null>(null);

const totalIncome = computed(() => {
  if (!financeStore.expenseSummary) return 0;
  return financeStore.expenseSummary.total_income_pln + 
         financeStore.expenseSummary.total_income_eur + 
         financeStore.expenseSummary.total_income_usd +
         (financeStore.expenseSummary.total_income_gtq);
});

const totalExpenses = computed(() => {
  if (!financeStore.expenseSummary) return 0;
  return financeStore.expenseSummary.total_expense_pln + 
         financeStore.expenseSummary.total_expense_eur + 
         financeStore.expenseSummary.total_expense_usd +
         (financeStore.expenseSummary.total_expense_gtq);
});

// Currency conversion function
const convertAmount = (amount: number, fromCurrency: string, toCurrency: string): number => {
  if (!exchangeRates.value || fromCurrency === toCurrency) {
    return amount;
  }
  
  const rates = exchangeRates.value.rates;
  const baseRate = rates[fromCurrency] || 1;
  const targetRate = rates[toCurrency] || 1;
  
  // Convert to base currency first, then to target currency
  const amountInBase = amount / baseRate;
  return amountInBase * targetRate;
};

// Converted totals computed properties
const totalIncomeConverted = computed(() => {
  if (!financeStore.expenseSummary || !exchangeRates.value) {
    return totalIncome.value;
  }
  
  const incomeEUR = convertAmount(financeStore.expenseSummary.total_income_eur, 'EUR', baseCurrency.value);
  const incomeUSD = convertAmount(financeStore.expenseSummary.total_income_usd, 'USD', baseCurrency.value);
  const incomePLN = convertAmount(financeStore.expenseSummary.total_income_pln, 'PLN', baseCurrency.value);
  const incomeGTQ = convertAmount(financeStore.expenseSummary.total_income_gtq, 'GTQ', baseCurrency.value);
  
  return incomeEUR + incomeUSD + incomePLN + incomeGTQ;
});

const totalExpensesConverted = computed(() => {
  if (!financeStore.expenseSummary || !exchangeRates.value) {
    return totalExpenses.value;
  }
  
  const expenseEUR = convertAmount(financeStore.expenseSummary.total_expense_eur, 'EUR', baseCurrency.value);
  const expenseUSD = convertAmount(financeStore.expenseSummary.total_expense_usd, 'USD', baseCurrency.value);
  const expensePLN = convertAmount(financeStore.expenseSummary.total_expense_pln, 'PLN', baseCurrency.value);
  const expenseGTQ = convertAmount(financeStore.expenseSummary.total_expense_gtq, 'GTQ', baseCurrency.value);
  
  return expenseEUR + expenseUSD + expensePLN + expenseGTQ;
});

const netBalanceConverted = computed(() => {
  return totalIncomeConverted.value - totalExpensesConverted.value;
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

// Utility functions
const formatTimestamp = (timestamp: number): string => {
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

onMounted(async () => {
  await Promise.all([
    financeStore.fetchTransactions(),
    financeStore.fetchAccounts(),
    financeStore.fetchAnalytics(),
    fetchExchangeRates()
  ]);
});
</script>