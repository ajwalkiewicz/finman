import { defineStore } from 'pinia';
import { ref } from 'vue';
import { transactionsAPI, accountsAPI, analyticsAPI, subscriptionAPI } from '@/services/api';
import type { Transaction, Account, ExpenseSummary, AccountFlow, SubscriptionInfo, SubscriptionLimitError } from '@/types';

export const useFinanceStore = defineStore('finance', () => {
  const transactions = ref<Transaction[]>([]);
  const accounts = ref<Account[]>([]);
  const expenseSummary = ref<ExpenseSummary | null>(null);
  const accountFlow = ref<AccountFlow>({});
  const subscriptionInfo = ref<SubscriptionInfo | null>(null);
  const loading = ref(false);
  
  // Transactions
  const fetchTransactions = async () => {
    loading.value = true;
    try {
      transactions.value = await transactionsAPI.getAll();
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
    } finally {
      loading.value = false;
    }
  };
  
  const createTransaction = async (transaction: Omit<Transaction, 'id' | 'is_expense' | 'owner_id' | 'created_at'>) => {
    try {
      const newTransaction = await transactionsAPI.create(transaction);
      transactions.value.push(newTransaction);
      // Refresh subscription info to update transaction count
      await fetchSubscriptionInfo();
      // Note: Analytics refresh is now manual to prevent excessive API calls
      return newTransaction;
    } catch (error: any) {
      // Check if it's a subscription limit error
      if (error?.response?.data?.detail?.type === 'subscription_limit_error') {
        const limitError: SubscriptionLimitError = {
          type: 'subscription_limit_error',
          message: error.response.data.detail.message
        };
        throw limitError;
      }
      console.error('Failed to create transaction:', error);
      throw error;
    }
  };
  
  const updateTransaction = async (id: number, transaction: Omit<Transaction, 'id' | 'is_expense' | 'owner_id' | 'created_at'>) => {
    try {
      const updatedTransaction = await transactionsAPI.update(id, transaction);
      const index = transactions.value.findIndex(t => t.id === id);
      if (index !== -1) {
        transactions.value[index] = updatedTransaction;
      }
      // Note: Analytics refresh is now manual to prevent excessive API calls
      return updatedTransaction;
    } catch (error) {
      console.error('Failed to update transaction:', error);
      throw error;
    }
  };
  
  const deleteTransaction = async (id: number) => {
    try {
      await transactionsAPI.delete(id);
      transactions.value = transactions.value.filter(t => t.id !== id);
      // Refresh subscription info to update transaction count
      await fetchSubscriptionInfo();
      // Note: Analytics refresh is now manual to prevent excessive API calls
    } catch (error) {
      console.error('Failed to delete transaction:', error);
      throw error;
    }
  };
  
  // Accounts
  const fetchAccounts = async () => {
    try {
      accounts.value = await accountsAPI.getAll();
    } catch (error) {
      console.error('Failed to fetch accounts:', error);
    }
  };
  
  const createAccount = async (account: Omit<Account, 'id' | 'created_at'>) => {
    try {
      const newAccount = await accountsAPI.create(account);
      accounts.value.push(newAccount);
      // Refresh subscription info to update account count
      await fetchSubscriptionInfo();
      return newAccount;
    } catch (error: any) {
      // Check if it's a subscription limit error
      if (error?.response?.data?.detail?.type === 'subscription_limit_error') {
        const limitError: SubscriptionLimitError = {
          type: 'subscription_limit_error',
          message: error.response.data.detail.message
        };
        throw limitError;
      }
      console.error('Failed to create account:', error);
      throw error;
    }
  };
  
  const updateAccount = async (id: number, account: Omit<Account, 'id' | 'created_at'>) => {
    try {
      const updatedAccount = await accountsAPI.update(id, account);
      const index = accounts.value.findIndex(a => a.id === id);
      if (index !== -1) {
        accounts.value[index] = updatedAccount;
      }
      return updatedAccount;
    } catch (error) {
      console.error('Failed to update account:', error);
      throw error;
    }
  };
  
  const deleteAccount = async (id: number) => {
    try {
      await accountsAPI.delete(id);
      accounts.value = accounts.value.filter(a => a.id !== id);
      // Refresh subscription info to update account count
      await fetchSubscriptionInfo();
    } catch (error) {
      console.error('Failed to delete account:', error);
      throw error;
    }
  };
  
  // Analytics
  const fetchAnalytics = async () => {
    try {
      const [expenses, flow] = await Promise.all([
        analyticsAPI.getExpenseSummary(),
        analyticsAPI.getAccountFlow()
      ]);
      expenseSummary.value = expenses;
      accountFlow.value = flow;
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    }
  };
  
  // Subscription
  const fetchSubscriptionInfo = async () => {
    try {
      subscriptionInfo.value = await subscriptionAPI.getInfo();
    } catch (error) {
      console.error('Failed to fetch subscription info:', error);
    }
  };

  // Manual analytics refresh for bulk operations
  const refreshAnalytics = async () => {
    await fetchAnalytics();
  };

  return {
    transactions,
    accounts,
    expenseSummary,
    accountFlow,
    subscriptionInfo,
    loading,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    fetchAccounts,
    createAccount,
    updateAccount,
    deleteAccount,
    fetchAnalytics,
    refreshAnalytics,
    fetchSubscriptionInfo
  };
});