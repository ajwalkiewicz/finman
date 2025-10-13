<template>


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
                        @click="confirmDelete(transaction)"
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

        <!-- CSV Import/Export Section -->
        <div class="mt-6 bg-white shadow overflow-hidden sm:rounded-md">
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Import/Export Transactions</h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">Import transactions from CSV or export current transactions</p>
          </div>
          <div class="px-4 py-5 sm:px-6">
            <div class="flex flex-col sm:flex-row gap-4">
              <!-- Import Section -->
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-2">Import from CSV</label>
                <div class="flex items-center space-x-2">
                  <input
                    ref="fileInput"
                    type="file"
                    accept=".csv"
                    @change="handleFileUpload"
                    class="hidden"
                  />
                  <button
                    @click="fileInput?.click()"
                    class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                    </svg>
                    Choose CSV File
                  </button>
                  <span v-if="selectedFile" class="text-sm text-gray-600">{{ selectedFile.name }}</span>
                </div>
                <p class="mt-1 text-xs text-gray-500">
                  Expected format: title, origin_account, destination_account, amount, currency, day_of_month, description
                </p>
                <button
                  v-if="selectedFile"
                  @click="importFromCSV"
                  :disabled="importing"
                  class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                >
                  <svg v-if="!importing" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
                  </svg>
                  <svg v-else class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ importing ? `Importing... ${importProgress}%` : 'Import Transactions' }}
                </button>
              </div>

              <!-- Export Section -->
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-2">Export to CSV</label>
                <button
                  @click="exportToCSV"
                  :disabled="financeStore.transactions.length === 0 || exporting"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  <svg v-if="!exporting" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <svg v-else class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ exporting ? 'Exporting...' : 'Export All Transactions' }}
                </button>
                <p class="mt-1 text-xs text-gray-500">
                  Downloads all transactions as CSV file
                </p>
              </div>
            </div>

            <!-- Import Results -->
            <div v-if="importResults" class="mt-4 p-4 rounded-md" :class="importResults.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg v-if="importResults.success" class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium" :class="importResults.success ? 'text-green-800' : 'text-red-800'">
                    {{ importResults.success ? 'Import Successful' : 'Import Failed' }}
                  </h3>
                  <div class="mt-2 text-sm" :class="importResults.success ? 'text-green-700' : 'text-red-700'">
                    <p>{{ importResults.message }}</p>
                    <ul v-if="importResults.details && importResults.details.length > 0" class="list-disc list-inside mt-1">
                      <li v-for="detail in importResults.details" :key="detail">{{ detail }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
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

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div class="mt-3">
              <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.232 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                </svg>
              </div>
              
              <h3 class="text-lg font-medium text-gray-900 text-center mb-2">Delete Transaction</h3>
              
              <p class="text-sm text-gray-600 text-center mb-4">
                Are you sure you want to delete the transaction "<strong>{{ selectedTransaction?.title }}</strong>"? 
                This action cannot be undone.
              </p>
              
              <div class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <p class="text-xs text-yellow-800">
                  <strong>Warning:</strong> Deleting this transaction will permanently remove it from your records and may affect your account balances and analytics.
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
                  {{ deleteSubmitting ? 'Deleting...' : 'Delete Transaction' }}
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
import type { Transaction } from '@/types';

const financeStore = useFinanceStore();

const showModal = ref(false);
const editingTransaction = ref<Transaction | null>(null);
const submitting = ref(false);

// Delete modal state
const showDeleteModal = ref(false);
const selectedTransaction = ref<Transaction | null>(null);
const deleteSubmitting = ref(false);

// CSV Import/Export state
const selectedFile = ref<File | null>(null);
const importing = ref(false);
const importProgress = ref(0);
const exporting = ref(false);
const importResults = ref<{
  success: boolean;
  message: string;
  details?: string[];
} | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

// Rate limiting configuration
const RATE_LIMIT_DELAY = 1000; // Minimum delay between requests in ms

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
    // Note: No need to refetch transactions/accounts as the store updates them automatically
  } catch (error) {
    console.error('Failed to save transaction:', error);
  } finally {
    submitting.value = false;
  }
};

const confirmDelete = (transaction: Transaction) => {
  selectedTransaction.value = transaction;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  selectedTransaction.value = null;
};

const handleDelete = async () => {
  if (!selectedTransaction.value?.id) return;
  
  deleteSubmitting.value = true;
  try {
    await financeStore.deleteTransaction(selectedTransaction.value.id);
    // Note: No need to refetch transactions as the store updates them automatically
    closeDeleteModal();
  } catch (error) {
    console.error('Failed to delete transaction:', error);
  } finally {
    deleteSubmitting.value = false;
  }
};

// CSV Import/Export Methods
const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file && file.type === 'text/csv') {
    selectedFile.value = file;
    importResults.value = null; // Clear previous results
  } else {
    alert('Please select a valid CSV file.');
    target.value = '';
  }
};

const parseCSVLine = (line: string): string[] => {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }
  
  result.push(current.trim());
  return result;
};

const parseCSV = (csvText: string): any[] => {
  const lines = csvText.split('\n').filter(line => line.trim());
  if (lines.length < 2) return [];
  
  const headers = parseCSVLine(lines[0]).map(h => h.replace(/"/g, ''));
  const expectedHeaders = ['title', 'origin_account', 'destination_account', 'amount', 'currency', 'day_of_month', 'description'];
  
  // Check if headers match expected format
  const hasValidHeaders = expectedHeaders.every(header => 
    headers.some(h => h.toLowerCase() === header.toLowerCase())
  );
  
  if (!hasValidHeaders) {
    throw new Error(`Invalid CSV format. Expected headers: ${expectedHeaders.join(', ')}`);
  }
  
  const data = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]).map(v => v.replace(/"/g, ''));
    if (values.length >= headers.length) {
      const row: any = {};
      headers.forEach((header, index) => {
        const normalizedHeader = header.toLowerCase();
        if (expectedHeaders.includes(normalizedHeader) && index < values.length) {
          row[normalizedHeader] = values[index];
        }
      });
      
      // Only add row if it has the required fields
      if (row.title && row.amount && row.currency && row.day_of_month) {
        data.push(row);
      }
    }
  }
  
  return data;
};

const createAccountIfNotExists = async (accountName: string): Promise<void> => {
  if (!accountName || accountName === '' || accountName.toLowerCase() === 'income' || accountName.toLowerCase() === 'expense') {
    return; // Skip system accounts or empty names
  }
  
  // Check if account already exists
  const existingAccount = financeStore.accounts.find(acc => 
    acc.name.toLowerCase() === accountName.toLowerCase()
  );
  
  if (!existingAccount) {
    try {
      await financeStore.createAccount({
        name: accountName,
        account_type: 'checking',
        base_currency: 'PLN',
        label_color: '#' + Math.floor(Math.random()*16777215).toString(16) // Random color
      });
    } catch (error) {
      console.error(`Failed to create account ${accountName}:`, error);
    }
  }
};

const transactionExists = (transaction: any): boolean => {
  return financeStore.transactions.some(t => 
    t.title === transaction.title &&
    t.amount === parseFloat(transaction.amount) &&
    t.day_of_month === parseInt(transaction.day_of_month) &&
    t.origin_account === (transaction.origin_account || null) &&
    t.destination_account === (transaction.destination_account || null)
  );
};

const importFromCSV = async () => {
  if (!selectedFile.value) return;
  
  importing.value = true;
  importResults.value = null;
  
  try {
    const fileText = await selectedFile.value.text();
    const csvData = parseCSV(fileText);
    
    if (csvData.length === 0) {
      throw new Error('No valid data found in CSV file');
    }
    
    let importedCount = 0;
    let skippedCount = 0;
    let errorCount = 0;
    const errors: string[] = [];
    
    // Create accounts first
    const accountsToCreate = new Set<string>();
    csvData.forEach(row => {
      if (row.origin_account && row.origin_account !== '') {
        accountsToCreate.add(row.origin_account);
      }
      if (row.destination_account && row.destination_account !== '') {
        accountsToCreate.add(row.destination_account);
      }
    });
    
    for (const accountName of accountsToCreate) {
      await createAccountIfNotExists(accountName);
    }
    
    // Only refresh accounts if we actually created new ones
    if (accountsToCreate.size > 0) {
      await financeStore.fetchAccounts();
    }
    
    // Import transactions with rate limiting
    const batchSize = 4; // Process 4 transactions at a time
    importProgress.value = 0;
    
    for (let i = 0; i < csvData.length; i += batchSize) {
      const batch = csvData.slice(i, i + batchSize);
      
      // Update progress
      importProgress.value = Math.round((i / csvData.length) * 100);
      
      // Process batch with rate limiting
      await new Promise(resolve => setTimeout(resolve, RATE_LIMIT_DELAY));
      
      const batchPromises = batch.map(async (row, batchIndex) => {
        const rowIndex = i + batchIndex;
        
        try {
          // Validate required fields
          if (!row.title || !row.amount || !row.currency || !row.day_of_month) {
            errors.push(`Row ${rowIndex + 2}: Missing required fields (title, amount, currency, day_of_month)`);
            errorCount++;
            return;
          }
          
          const transactionData = {
            title: row.title,
            origin_account: row.origin_account || null,
            destination_account: row.destination_account || null,
            amount: parseFloat(row.amount.replace(/[^0-9.,]/g, '').replace(',', '.')),
            currency: row.currency,
            day_of_month: parseInt(row.day_of_month),
            description: row.description || ''
          };
          
          // Validate amount and day
          if (isNaN(transactionData.amount) || transactionData.amount <= 0) {
            errors.push(`Row ${rowIndex + 2}: Invalid amount`);
            errorCount++;
            return;
          }
          
          if (isNaN(transactionData.day_of_month) || transactionData.day_of_month < 1 || transactionData.day_of_month > 31) {
            errors.push(`Row ${rowIndex + 2}: Invalid day of month`);
            errorCount++;
            return;
          }
          
          // Check if transaction already exists
          if (transactionExists(transactionData)) {
            skippedCount++;
            return;
          }
          
          await financeStore.createTransaction(transactionData);
          importedCount++;
          
        } catch (error) {
          errors.push(`Row ${rowIndex + 2}: ${error instanceof Error ? error.message : 'Unknown error'}`);
          errorCount++;
        }
      });
      
      await Promise.allSettled(batchPromises);
    }
    
    // Complete progress
    importProgress.value = 100;
    
    importResults.value = {
      success: errorCount === 0 || importedCount > 0,
      message: `Import completed: ${importedCount} imported, ${skippedCount} skipped (duplicates), ${errorCount} errors`,
      details: errors.length > 0 ? errors.slice(0, 10) : undefined // Show only first 10 errors
    };
    
    // Refresh analytics only after bulk import if transactions were imported
    if (importedCount > 0) {
      await financeStore.refreshAnalytics();
    }
    
    // Clear the file input
    selectedFile.value = null;
    if (fileInput.value) {
      fileInput.value.value = '';
    }
    
  } catch (error) {
    importResults.value = {
      success: false,
      message: `Import failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  } finally {
    importing.value = false;
    importProgress.value = 0;
  }
};

const exportToCSV = () => {
  if (financeStore.transactions.length === 0) return;
  
  exporting.value = true;
  
  try {
    const headers = ['title', 'origin_account', 'destination_account', 'amount', 'currency', 'day_of_month', 'description'];
    const csvContent = [
      headers.join(','),
      ...financeStore.transactions.map(transaction => [
        `"${transaction.title}"`,
        `"${transaction.origin_account || ''}"`,
        `"${transaction.destination_account || ''}"`,
        transaction.amount,
        transaction.currency,
        transaction.day_of_month,
        `"${transaction.description || ''}"`
      ].join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `transactions_export_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
    
  } catch (error) {
    console.error('Export failed:', error);
    alert('Failed to export transactions. Please try again.');
  } finally {
    exporting.value = false;
  }
};

onMounted(async () => {
  // Only fetch transactions and accounts - analytics will be loaded when needed
  await Promise.all([
    financeStore.fetchTransactions(),
    financeStore.fetchAccounts()
  ]);
});
</script>