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
              
              <!-- Chart Container -->
              <div class="relative h-80 bg-gray-50 rounded-lg p-4 overflow-hidden mb-2">
                <!-- Y-axis labels -->
                <div class="absolute left-0 top-4 h-64 flex flex-col justify-between text-xs text-gray-800 font-semibold">
                  <span class="bg-white px-1 rounded shadow-sm">{{ formatCurrency(cashFlowData.maxBalance, 'PLN') }}</span>
                  <span class="bg-white px-1 rounded shadow-sm">{{ formatCurrency((cashFlowData.maxBalance + cashFlowData.minBalance) / 2, 'PLN') }}</span>
                  <span class="bg-white px-1 rounded shadow-sm">{{ formatCurrency(cashFlowData.minBalance, 'PLN') }}</span>
                </div>
                
                <!-- Chart area -->
                <div class="ml-16 mr-4 h-64 relative">
                  <!-- Zero line -->
                  <div 
                    v-if="cashFlowData.minBalance < 0 && cashFlowData.maxBalance > 0"
                    class="absolute w-full border-t border-gray-400 border-dashed"
                    :style="{ bottom: getZeroLinePosition(cashFlowData) + '%' }"
                  ></div>
                  
                  <!-- Balance line chart -->
                  <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <!-- Background grid -->
                    <defs>
                      <pattern id="cashflow-grid" width="10" height="10" patternUnits="userSpaceOnUse">
                        <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#e5e7eb" stroke-width="0.5"/>
                      </pattern>
                    </defs>
                    <rect width="100%" height="100%" fill="url(#cashflow-grid)" />
                    
                    <!-- Positive area (above zero) -->
                    <path
                      :d="getCashFlowAreaPath(cashFlowData.dailyBalances, cashFlowData.minBalance, cashFlowData.maxBalance, true)"
                      fill="rgba(34, 197, 94, 0.2)"
                      stroke="none"
                    />
                    
                    <!-- Negative area (below zero) -->
                    <path
                      :d="getCashFlowAreaPath(cashFlowData.dailyBalances, cashFlowData.minBalance, cashFlowData.maxBalance, false)"
                      fill="rgba(239, 68, 68, 0.2)"
                      stroke="none"
                    />
                    
                    <!-- Balance line -->
                    <path
                      :d="getLinePath(cashFlowData.dailyBalances, cashFlowData.minBalance, cashFlowData.maxBalance)"
                      fill="none"
                      stroke="#6366f1"
                      stroke-width="1.2"
                      vector-effect="non-scaling-stroke"
                    />
                    
                    <!-- Data points -->
                    <circle
                      v-for="(point, index) in cashFlowData.dailyBalances"
                      :key="index"
                      :cx="(point.day / 31) * 100"
                      :cy="100 - ((point.balance - cashFlowData.minBalance) / (cashFlowData.maxBalance - cashFlowData.minBalance)) * 100"
                      r="1.5"
                      :fill="point.balance >= 0 ? '#22c55e' : '#ef4444'"
                      vector-effect="non-scaling-stroke"
                    />
                  </svg>
                </div>
              </div>
              
              <!-- X-axis labels - Closer to the chart -->
              <div class="ml-16 mr-4 mb-4">
                <div class="flex justify-between text-base text-gray-900 font-bold border-t border-gray-300 pt-1">
                  <span class="bg-gray-100 px-2 py-1 rounded">1</span>
                  <span class="bg-gray-100 px-2 py-1 rounded">5</span>
                  <span class="bg-gray-100 px-2 py-1 rounded">10</span>
                  <span class="bg-gray-100 px-2 py-1 rounded">15</span>
                  <span class="bg-gray-100 px-2 py-1 rounded">20</span>
                  <span class="bg-gray-100 px-2 py-1 rounded">25</span>
                  <span class="bg-gray-100 px-2 py-1 rounded">31</span>
                </div>
                <div class="text-center text-sm text-gray-700 mt-1 font-semibold">
                  Days of Month
                </div>
              </div>
              
              <!-- Cash flow summary -->
              <div class="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
                <div class="text-center p-3 bg-green-50 rounded-lg">
                  <div class="text-green-600 font-medium">Total Income</div>
                  <div class="text-green-800 font-semibold">{{ formatCurrency(cashFlowData.totalIncome, 'PLN') }}</div>
                </div>
                <div class="text-center p-3 bg-red-50 rounded-lg">
                  <div class="text-red-600 font-medium">Total Expenses</div>
                  <div class="text-red-800 font-semibold">{{ formatCurrency(cashFlowData.totalExpenses, 'PLN') }}</div>
                </div>
                <div class="text-center p-3 bg-blue-50 rounded-lg">
                  <div class="text-blue-600 font-medium">Net Cash Flow</div>
                  <div class="text-blue-800 font-semibold" :class="cashFlowData.netFlow >= 0 ? 'text-green-800' : 'text-red-800'">
                    {{ cashFlowData.netFlow >= 0 ? '+' : '' }}{{ formatCurrency(cashFlowData.netFlow, 'PLN') }}
                  </div>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded-lg">
                  <div class="text-gray-600 font-medium">Transactions</div>
                  <div class="text-gray-800 font-semibold">{{ cashFlowData.transactionCount }}</div>
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
                
                <!-- Chart Container -->
                <div class="relative h-80 bg-gray-50 rounded-lg p-4 overflow-hidden mb-2">
                  <!-- Y-axis labels -->
                  <div class="absolute left-0 top-4 h-64 flex flex-col justify-between text-xs text-gray-800 font-semibold">
                    <span class="bg-white px-1 rounded shadow-sm">{{ formatCurrency(account.maxBalance, account.baseCurrency) }}</span>
                    <span class="bg-white px-1 rounded shadow-sm">{{ formatCurrency((account.maxBalance + account.minBalance) / 2, account.baseCurrency) }}</span>
                    <span class="bg-white px-1 rounded shadow-sm">{{ formatCurrency(account.minBalance, account.baseCurrency) }}</span>
                  </div>
                  
                  <!-- Chart area -->
                  <div class="ml-16 mr-4 h-64 relative">
                    <!-- Zero line -->
                    <div 
                      v-if="account.minBalance < 0 && account.maxBalance > 0"
                      class="absolute w-full border-t border-gray-400 border-dashed"
                      :style="{ bottom: getZeroLinePosition(account) + '%' }"
                    ></div>
                    
                    <!-- Balance line chart -->
                    <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                      <!-- Background grid -->
                      <defs>
                        <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#e5e7eb" stroke-width="0.5"/>
                        </pattern>
                      </defs>
                      <rect width="100%" height="100%" fill="url(#grid)" />
                      
                      <!-- Balance area -->
                      <path
                        :d="getAreaPath(account.dailyBalances, account.minBalance, account.maxBalance)"
                        fill="rgba(59, 130, 246, 0.1)"
                        stroke="none"
                      />
                      
                      <!-- Balance line -->
                      <path
                        :d="getLinePath(account.dailyBalances, account.minBalance, account.maxBalance)"
                        fill="none"
                        stroke="#3b82f6"
                        stroke-width="0.8"
                        vector-effect="non-scaling-stroke"
                      />
                      
                      <!-- Data points -->
                      <circle
                        v-for="(point, index) in account.dailyBalances"
                        :key="index"
                        :cx="(point.day / 31) * 100"
                        :cy="100 - ((point.balance - account.minBalance) / (account.maxBalance - account.minBalance)) * 100"
                        r="1"
                        fill="#3b82f6"
                        vector-effect="non-scaling-stroke"
                      />
                    </svg>
                  </div>
                </div>
                
                <!-- X-axis labels - Closer to the chart -->
                <div class="ml-16 mr-4 mb-4">
                  <div class="flex justify-between text-base text-gray-900 font-bold border-t border-gray-300 pt-1">
                    <span class="bg-gray-100 px-2 py-1 rounded">1</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">5</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">10</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">15</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">20</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">25</span>
                    <span class="bg-gray-100 px-2 py-1 rounded">31</span>
                  </div>
                  <div class="text-center text-sm text-gray-700 mt-1 font-semibold">
                    Days of Month
                  </div>
                </div>
                
                <!-- Account summary -->
                <div class="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
                  <div class="text-center p-3 bg-green-50 rounded-lg">
                    <div class="text-green-600 font-medium">Total In</div>
                    <div class="text-green-800 font-semibold">{{ formatCurrency(account.totalIncoming, 'PLN') }}</div>
                  </div>
                  <div class="text-center p-3 bg-red-50 rounded-lg">
                    <div class="text-red-600 font-medium">Total Out</div>
                    <div class="text-red-800 font-semibold">{{ formatCurrency(account.totalOutgoing, 'PLN') }}</div>
                  </div>
                  <div class="text-center p-3 bg-blue-50 rounded-lg">
                    <div class="text-blue-600 font-medium">Net Flow</div>
                    <div class="text-blue-800 font-semibold" :class="account.netFlow >= 0 ? 'text-green-800' : 'text-red-800'">
                      {{ account.netFlow >= 0 ? '+' : '' }}{{ formatCurrency(account.netFlow, 'PLN') }}
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

// Chart helper functions
const getZeroLinePosition = (account: any) => {
  if (account.minBalance >= 0) return 0;
  if (account.maxBalance <= 0) return 100;
  
  const range = account.maxBalance - account.minBalance;
  return (Math.abs(account.minBalance) / range) * 100;
};

const getLinePath = (dailyBalances: { day: number; balance: number }[], minBalance: number, maxBalance: number) => {
  if (dailyBalances.length === 0) return '';
  
  const range = maxBalance - minBalance || 1; // Prevent division by zero
  
  const pathPoints = dailyBalances.map(point => {
    const x = (point.day / 31) * 100;
    const y = 100 - ((point.balance - minBalance) / range) * 100;
    return `${x},${y}`;
  });
  
  return `M ${pathPoints.join(' L ')}`;
};

const getAreaPath = (dailyBalances: { day: number; balance: number }[], minBalance: number, maxBalance: number) => {
  if (dailyBalances.length === 0) return '';
  
  const range = maxBalance - minBalance || 1;
  const zeroY = 100 - ((0 - minBalance) / range) * 100;
  
  const pathPoints = dailyBalances.map(point => {
    const x = (point.day / 31) * 100;
    const y = 100 - ((point.balance - minBalance) / range) * 100;
    return `${x},${y}`;
  });
  
  // Create area path: start from first point, draw line, then close to zero line
  const firstX = (dailyBalances[0].day / 31) * 100;
  const lastX = (dailyBalances[dailyBalances.length - 1].day / 31) * 100;
  
  return `M ${firstX},${zeroY} L ${pathPoints.join(' L ')} L ${lastX},${zeroY} Z`;
};

const getCashFlowAreaPath = (dailyBalances: { day: number; balance: number }[], minBalance: number, maxBalance: number, positive: boolean) => {
  if (dailyBalances.length === 0) return '';
  
  const range = maxBalance - minBalance || 1;
  const zeroY = 100 - ((0 - minBalance) / range) * 100;
  
  // Filter points based on whether we want positive or negative area
  const relevantPoints = dailyBalances.filter(point => positive ? point.balance >= 0 : point.balance < 0);
  
  if (relevantPoints.length === 0) return '';
  
  // Build path for the relevant area
  let path = '';
  let currentSegment: { day: number; balance: number }[] = [];
  
  for (let i = 0; i < dailyBalances.length; i++) {
    const point = dailyBalances[i];
    const isRelevant = positive ? point.balance >= 0 : point.balance < 0;
    
    if (isRelevant) {
      currentSegment.push(point);
    } else {
      // End current segment if it exists
      if (currentSegment.length > 0) {
        path += buildSegmentPath(currentSegment, minBalance, maxBalance, zeroY);
        currentSegment = [];
      }
    }
  }
  
  // Handle final segment
  if (currentSegment.length > 0) {
    path += buildSegmentPath(currentSegment, minBalance, maxBalance, zeroY);
  }
  
  return path;
};

const buildSegmentPath = (segment: { day: number; balance: number }[], minBalance: number, maxBalance: number, zeroY: number) => {
  if (segment.length === 0) return '';
  
  const range = maxBalance - minBalance || 1;
  
  const pathPoints = segment.map(point => {
    const x = (point.day / 31) * 100;
    const y = 100 - ((point.balance - minBalance) / range) * 100;
    return `${x},${y}`;
  });
  
  const firstX = (segment[0].day / 31) * 100;
  const lastX = (segment[segment.length - 1].day / 31) * 100;
  
  return `M ${firstX},${zeroY} L ${pathPoints.join(' L ')} L ${lastX},${zeroY} Z `;
};

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