<template>
    <main class="max-w-7xl mx-auto py-4 sm:py-6 px-4 sm:px-6 lg:px-8">
      <div class="space-y-6">
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Analytics</h1>

        <!-- Base Currency Selection -->
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Exchange Rates</h3>
            <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4 space-y-2 sm:space-y-0 mb-4">
              <label for="base-currency" class="text-sm font-medium text-gray-700 flex-shrink-0">Base Currency:</label>
              <select 
                id="base-currency"
                v-model="baseCurrency" 
                @change="handleCurrencyChange"
                class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-auto"
              >
                <option value="PLN">PLN</option>
                <option value="EUR">EUR</option>
                <option value="USD">USD</option>
                <option value="GTQ">GTQ</option>
              </select>
            </div>
            
            <!-- Exchange Rate Cards -->
            <div v-if="exchangeRates" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
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
        <div v-if="financeStore.expenseSummary" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6">
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
        <div v-if="financeStore.expenseSummary && Object.keys(financeStore.expenseSummary.by_category).length > 0" class="bg-white shadow sm:rounded-lg">
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

        <!-- Total Balance Overview -->
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-2 sm:mb-0">Total Balance</h3>
              <div class="text-right">
                <div class="text-2xl font-bold" :class="totalBalanceData.totalBalance >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ formatCurrency(totalBalanceData.totalBalance, totalBalanceData.baseCurrency) }}
                </div>
                <div class="text-sm text-gray-500">Across all accounts in {{ totalBalanceData.baseCurrency }}</div>
              </div>
            </div>
            
            <!-- Account Breakdown -->
            <div v-if="totalBalanceData.balancesByAccount.length > 0" class="border-t border-gray-200 pt-4">
              <h4 class="text-sm font-medium text-gray-900 mb-3">Account Breakdown</h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <div
                  v-for="account in totalBalanceData.balancesByAccount"
                  :key="account.name"
                  class="bg-gray-50 rounded-lg p-3 border border-gray-200"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center">
                      <div 
                        class="w-3 h-3 rounded-full mr-2 flex-shrink-0"
                        :style="{ backgroundColor: account.labelColor }"
                      ></div>
                      <span class="text-sm font-medium text-gray-900 truncate">{{ account.name }}</span>
                    </div>
                    <div class="text-right ml-2">
                      <div class="text-sm font-semibold" :class="account.balance >= 0 ? 'text-green-600' : 'text-red-600'">
                        {{ formatCurrency(account.balance, account.currency) }}
                      </div>
                      <div v-if="account.currency !== totalBalanceData.baseCurrency" class="text-xs text-gray-500">
                        ≈ {{ formatCurrency(account.balanceInBaseCurrency, totalBalanceData.baseCurrency) }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="border-t border-gray-200 pt-4 text-center text-gray-500">
              <p>No account balances to display</p>
            </div>
          </div>
        </div>

        <!-- Premium Features Notice for Free Plan Users -->
        <div v-if="!hasChartsAccess" class="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-8 w-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-indigo-900">Unlock Advanced Analytics</h3>
              <p class="text-sm text-indigo-700 mt-1">
                Get detailed insights with interactive charts showing cash flow analysis and account balance trends over time.
              </p>
              <div class="mt-4">
                <router-link 
                  to="/settings" 
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  Upgrade Plan
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Cash Flow Overview (Income vs Expense) -->
        <div v-if="hasChartsAccess && cashFlowData.dailyBalances.length > 0" class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-6">Cash Flow Overview</h3>
            <p class="text-sm text-gray-600 mb-6">Daily net cash flow from all income and expense transactions</p>
            
            <div class="border border-gray-200 rounded-lg p-6">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
                <h4 class="text-lg font-semibold text-gray-900 mb-2 sm:mb-0">Total Cash Flow</h4>
                <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4 text-sm text-gray-600">
                  <span>Net: <span class="font-medium" :class="cashFlowData.netFlow >= 0 ? 'text-green-600' : 'text-red-600'">{{ formatCurrency(cashFlowData.netFlow, 'PLN') }}</span></span>
                  <span>Peak: <span class="font-medium text-green-600">{{ formatCurrency(cashFlowData.maxBalance, 'PLN') }}</span></span>
                  <span>Low: <span class="font-medium text-red-600">{{ formatCurrency(cashFlowData.minBalance, 'PLN') }}</span></span>
                </div>
              </div>
              
              <!-- Chart.js Chart Container -->
              <div class="h-80 bg-gray-50 rounded-lg p-4">
                <Line
                  v-if="cashFlowChartData.datasets.length > 0"
                  :key="`cash-flow-${cashFlowData.dailyBalances.length}`"
                  :data="cashFlowChartData"
                  :options="cashFlowChartOptions"
                />
                <div v-else class="flex items-center justify-center h-full text-gray-500">
                  <div class="text-center">
                    <p class="text-lg">No chart data available</p>
                    <p class="text-sm">Chart access: {{ hasChartsAccess }}</p>
                    <p class="text-sm">Data points: {{ cashFlowData.dailyBalances.length }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Balance Charts -->
        <div v-if="hasChartsAccess && accountBalanceData.length > 0" class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-6">Account Balance Over Time</h3>
            <p class="text-sm text-gray-600 mb-6">Track how your account balances change throughout the month</p>
            
            <div class="space-y-8">
              <div
                v-for="account in accountBalanceData"
                :key="account.name"
                class="border border-gray-200 rounded-lg p-6"
              >
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
                  <h4 class="text-lg font-semibold text-gray-900 mb-2 sm:mb-0">{{ account.name }}</h4>
                  <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4 text-sm text-gray-600">
                    <span>Current: <span class="font-medium" :class="account.currentBalance >= 0 ? 'text-green-600' : 'text-red-600'">{{ formatCurrency(account.currentBalance, account.baseCurrency) }}</span></span>
                    <span>Peak: <span class="font-medium text-green-600">{{ formatCurrency(account.maxBalance, account.baseCurrency) }}</span></span>
                    <span>Low: <span class="font-medium text-red-600">{{ formatCurrency(account.minBalance, account.baseCurrency) }}</span></span>
                  </div>
                </div>
                
                <!-- Chart.js Chart Container -->
                <div class="h-80 bg-gray-50 rounded-lg p-4">
                  <Line
                    :data="getAccountChartData(account)"
                    :options="getAccountChartOptions(account)"
                  />
                </div>
                
                <!-- Account summary -->
                <div class="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
                  <div class="text-center p-3 bg-green-50 rounded-lg">
                    <div class="text-green-600 font-medium">Total In</div>
                    <div class="text-green-800 font-semibold">{{ formatCurrency(account.totalIncoming, account.baseCurrency) }}</div>
                  </div>
                  <div class="text-center p-3 bg-red-50 rounded-lg">
                    <div class="text-red-600 font-medium">Total Out</div>
                    <div class="text-red-800 font-semibold">{{ formatCurrency(account.totalOutgoing, account.baseCurrency) }}</div>
                  </div>
                  <div class="text-center p-3 bg-blue-50 rounded-lg">
                    <div class="text-blue-600 font-medium">Net Flow</div>
                    <div class="text-blue-800 font-semibold" :class="account.netFlow >= 0 ? 'text-green-800' : 'text-red-800'">
                      {{ account.netFlow >= 0 ? '+' : '' }}{{ formatCurrency(account.netFlow, account.baseCurrency) }}
                    </div>
                  </div>
                  <div class="text-center p-3 bg-gray-50 rounded-lg">
                    <div class="text-gray-600 font-medium">Transactions</div>
                    <div class="text-gray-800 font-semibold">{{ account.transactionCount }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!financeStore.expenseSummary && accountBalanceData.length === 0 && cashFlowData.transactionCount === 0" class="text-center py-12">
          <p class="text-gray-500">No data available for analysis. Add some transactions to get started.</p>
        </div>
      </div>
    </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useFinanceStore } from '@/stores/finance';
import { exchangeRatesAPI } from '@/services/api';
import type { ExchangeRatesResponse } from '@/types';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'vue-chartjs';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const financeStore = useFinanceStore();

// Exchange rates state with localStorage persistence
const baseCurrency = ref<string>(localStorage.getItem('baseCurrency') || 'PLN');
const exchangeRates = ref<ExchangeRatesResponse | null>(null);

// Check if user has access to analytics charts (premium feature)
const hasChartsAccess = computed(() => {
  const subscription = financeStore.subscriptionInfo;
  if (!subscription) return false;
  return subscription.subscription_name !== 'Free';
});

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

const sortedCategories = computed(() => {
  if (!financeStore.expenseSummary) return {};
  
  const entries = Object.entries(financeStore.expenseSummary.by_category);
  entries.sort((a, b) => b[1] - a[1]); // Sort by amount descending
  
  return Object.fromEntries(entries);
});

// Account balance data computation
const accountBalanceData = computed(() => {
  // Don't calculate if user doesn't have access to charts
  if (!hasChartsAccess.value) return [];
  
  const accounts = financeStore.accounts;
  const transactions = financeStore.transactions;
  
  if (!accounts.length || !transactions.length) return [];
  
  return accounts.filter(account => 
    account.name !== 'Income' && account.name !== 'Expense' // Exclude Income/Expense from individual charts
  ).map(account => {
    const accountBaseCurrency = account.base_currency || 'PLN';
    
    // Calculate daily balances for the account
    const dailyBalances: { day: number; balance: number }[] = [];
    let runningBalance = 0;
    
    // Process each day of the month
    for (let day = 1; day <= 31; day++) {
      const dayTransactions = transactions.filter(t => t.day_of_month === day);
      
      // Calculate balance change for this day
      let dayChange = 0;
      dayTransactions.forEach(transaction => {
        // Skip transactions without proper data
        if (!transaction.currency || typeof transaction.amount !== 'number') {
          return;
        }
        
        // Convert transaction amount to account's base currency
        const convertedAmount = convertAmount(transaction.amount, transaction.currency, accountBaseCurrency);
        
        if (transaction.destination_account === account.name) {
          // Money coming into this account
          dayChange += convertedAmount;
        }
        if (transaction.origin_account === account.name) {
          // Money going out of this account
          dayChange -= convertedAmount;
        }
      });
      
      runningBalance += dayChange;
      dailyBalances.push({ day, balance: runningBalance });
    }
    
    // Calculate totals
    let totalIncoming = 0;
    let totalOutgoing = 0;
    let transactionCount = 0;
    
    transactions.forEach(transaction => {
      // Skip transactions without proper data
      if (!transaction.currency || typeof transaction.amount !== 'number') {
        return;
      }
      
      // Convert transaction amount to account's base currency
      const convertedAmount = convertAmount(transaction.amount, transaction.currency, accountBaseCurrency);
      
      if (transaction.destination_account === account.name) {
        totalIncoming += convertedAmount;
        transactionCount++;
      }
      if (transaction.origin_account === account.name) {
        totalOutgoing += convertedAmount;
        transactionCount++;
      }
    });
    
    const balances = dailyBalances.map(d => d.balance);
    const minBalance = Math.min(...balances, 0);
    const maxBalance = Math.max(...balances, 0);
    const currentBalance = balances[balances.length - 1] || 0;
    const netFlow = totalIncoming - totalOutgoing;
    
    return {
      name: account.name,
      dailyBalances,
      minBalance,
      maxBalance,
      currentBalance,
      totalIncoming,
      totalOutgoing,
      netFlow,
      transactionCount,
      baseCurrency: accountBaseCurrency
    };
  }).filter(account => account.transactionCount > 0); // Only show accounts with transactions
});

// Total balance calculation across all accounts
const totalBalanceData = computed(() => {
  const accounts = financeStore.accounts;
  const transactions = financeStore.transactions;
  
  if (!accounts.length || !transactions.length) {
    return {
      totalBalance: 0,
      balancesByAccount: [],
      baseCurrency: baseCurrency.value
    };
  }
  
  // Calculate current balance for each account in the selected base currency
  const balancesByAccount = accounts.filter(account => 
    account.name !== 'Income' && account.name !== 'Expense'
  ).map(account => {
    const accountBaseCurrency = account.base_currency || 'PLN';
    
    // Calculate the current balance for this account
    let currentBalance = 0;
    transactions.forEach(transaction => {
      if (!transaction.currency || typeof transaction.amount !== 'number') {
        return;
      }
      
      const convertedAmount = convertAmount(transaction.amount, transaction.currency, accountBaseCurrency);
      
      if (transaction.destination_account === account.name) {
        currentBalance += convertedAmount;
      }
      if (transaction.origin_account === account.name) {
        currentBalance -= convertedAmount;
      }
    });
    
    // Convert account balance to the selected base currency for total calculation
    const balanceInBaseCurrency = convertAmount(currentBalance, accountBaseCurrency, baseCurrency.value);
    
    return {
      name: account.name,
      balance: currentBalance,
      currency: accountBaseCurrency,
      balanceInBaseCurrency,
      labelColor: account.label_color || '#3B82F6'
    };
  });
  
  const totalBalance = balancesByAccount.reduce((sum, account) => sum + account.balanceInBaseCurrency, 0);
  
  return {
    totalBalance,
    balancesByAccount: balancesByAccount.filter(account => Math.abs(account.balance) > 0.01), // Only show accounts with non-zero balances
    baseCurrency: baseCurrency.value
  };
});



// Cash flow data computation (Income vs Expense)
const cashFlowData = computed(() => {
  // Don't calculate if user doesn't have access to charts
  if (!hasChartsAccess.value) {
    return {
      dailyBalances: [],
      minBalance: 0,
      maxBalance: 0,
      netFlow: 0,
      totalIncome: 0,
      totalExpenses: 0,
      transactionCount: 0
    };
  }
  
  const transactions = financeStore.transactions;
  
  if (!transactions.length) {
    return {
      dailyBalances: [],
      minBalance: 0,
      maxBalance: 0,
      netFlow: 0,
      totalIncome: 0,
      totalExpenses: 0,
      transactionCount: 0
    };
  }
  
  const dailyBalances: { day: number; balance: number }[] = [];
  let runningBalance = 0;
  let totalIncome = 0;
  let totalExpenses = 0;
  let transactionCount = 0;
  
  // Process each day of the month
  for (let day = 1; day <= 31; day++) {
    const dayTransactions = transactions.filter(t => t.day_of_month === day);
    
    // Calculate balance change for this day
    let dayChange = 0;
    dayTransactions.forEach(transaction => {
      // Skip transactions without proper data
      if (!transaction.currency || typeof transaction.amount !== 'number') {
        return;
      }
      
      // Convert transaction amount to PLN
      const convertedAmount = convertAmount(transaction.amount, transaction.currency, 'PLN');
      
      // Income transactions (no origin account or origin is 'Income')
      if (!transaction.origin_account || transaction.origin_account === 'Income') {
        dayChange += convertedAmount;
        totalIncome += convertedAmount;
        transactionCount++;
      }
      // Expense transactions (no destination account or destination is 'Expense')
      else if (!transaction.destination_account || transaction.destination_account === 'Expense') {
        dayChange -= convertedAmount;
        totalExpenses += convertedAmount;
        transactionCount++;
      }
    });
    
    runningBalance += dayChange;
    dailyBalances.push({ day, balance: runningBalance });
  }
  
  const balances = dailyBalances.map(d => d.balance);
  const minBalance = Math.min(...balances, 0);
  const maxBalance = Math.max(...balances, 0);
  const netFlow = totalIncome - totalExpenses;
  
  return {
    dailyBalances,
    minBalance,
    maxBalance,
    netFlow,
    totalIncome,
    totalExpenses,
    transactionCount
  };
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

// Chart.js configuration for cash flow chart
const cashFlowChartData = computed(() => {
  if (!hasChartsAccess.value || !cashFlowData.value.dailyBalances.length) {
    console.log('No access or no data:', { hasAccess: hasChartsAccess.value, dataLength: cashFlowData.value.dailyBalances.length });
    return {
      labels: [],
      datasets: []
    };
  }

  const labels = cashFlowData.value.dailyBalances.map(d => `Day ${d.day}`);
  const data = cashFlowData.value.dailyBalances.map(d => d.balance);
  
  console.log('Chart data:', { labels: labels.slice(0, 5), data: data.slice(0, 5), hasChartsAccess: hasChartsAccess.value });

  return {
    labels,
    datasets: [
      {
        label: 'Cash Flow Balance',
        data,
        borderColor: 'rgb(99, 102, 241)',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: 'rgb(99, 102, 241)',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
      }
    ]
  };
});

const cashFlowChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      mode: 'index' as const,
      intersect: false,
      callbacks: {
        label: (context: any) => {
          const value = context.parsed.y;
          return `Balance: ${formatCurrency(value, 'PLN')}`;
        }
      }
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Days of Month'
      },
      grid: {
        display: true,
        color: 'rgba(229, 231, 235, 0.5)'
      }
    },
    y: {
      title: {
        display: true,
        text: 'Balance (PLN)'
      },
      grid: {
        display: true,
        color: 'rgba(229, 231, 235, 0.5)'
      },
      ticks: {
        callback: (value: any) => formatCurrency(value, 'PLN')
      }
    }
  },
  elements: {
    line: {
      borderWidth: 2,
    },
    point: {
      radius: 3,
      hoverRadius: 6,
    }
  }
}));

// Chart.js configuration for individual account charts
const getAccountChartData = (account: any) => {
  const labels = account.dailyBalances.map((d: any) => `Day ${d.day}`);
  const data = account.dailyBalances.map((d: any) => d.balance);

  return {
    labels,
    datasets: [
      {
        label: `${account.name} Balance`,
        data,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: 'origin',
        tension: 0.3,
        pointRadius: 3,
        pointHoverRadius: 5,
        pointBackgroundColor: 'rgb(59, 130, 246)',
      }
    ]
  };
};

const getAccountChartOptions = (account: any) => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: false,
    },
    legend: {
      display: false,
    },
    tooltip: {
      mode: 'index' as const,
      intersect: false,
      callbacks: {
        label: (context: any) => {
          const value = context.parsed.y;
          return `Balance: ${formatCurrency(value, account.baseCurrency)}`;
        }
      }
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Days of Month'
      },
      grid: {
        display: true,
        color: 'rgba(229, 231, 235, 0.5)'
      }
    },
    y: {
      title: {
        display: true,
        text: `Balance (${account.baseCurrency})`
      },
      grid: {
        display: true,
        color: 'rgba(229, 231, 235, 0.5)'
      },
      ticks: {
        callback: (value: any) => formatCurrency(value, account.baseCurrency)
      }
    }
  },
  interaction: {
    mode: 'nearest' as const,
    axis: 'x' as const,
    intersect: false
  }
});

// Initialize and fetch data

onMounted(async () => {
  await Promise.all([
    financeStore.fetchTransactions(),
    financeStore.fetchAccounts(),
    financeStore.fetchAnalytics(),
    financeStore.fetchSubscriptionInfo(),
    fetchExchangeRates()
  ]);
});
</script>