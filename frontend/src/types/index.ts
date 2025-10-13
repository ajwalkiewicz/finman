export interface Transaction {
  id?: number;
  title: string;
  origin_account: string | null;
  destination_account: string | null;
  amount: number;
  currency: string;
  day_of_month: number;
  description: string;
  is_expense?: boolean;
  owner_id?: number;
  created_at?: string;
}

export interface Account {
  id?: number;
  name: string;
  account_type: string;
  base_currency: string;
  label_color: string;
  owner_id?: number;
  created_at?: string;
}

export interface User {
  id: number;
  username: string;
  subscription_type: string;
  created_at: string;
}

export interface ExpenseSummary {
  total_income_pln: number;
  total_income_eur: number;
  total_income_usd: number;
  total_income_gtq: number;
  total_expense_pln: number;
  total_expense_eur: number;
  total_expense_usd: number;
  total_expense_gtq: number;
  by_category: Record<string, number>;
}

export interface AccountFlow {
  [accountName: string]: {
    incoming: number;
    outgoing: number;
  };
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ExchangeRatesResponse {
  success: boolean;
  timestamp: number;
  base: string;
  date: string;
  rates: {
    [currency: string]: number;
  };
}

export interface SubscriptionInfo {
  subscription_type: string;
  max_transactions: number;
  current_transactions: number;
  max_accounts: number;
  current_accounts: number;
  subscription_name: string;
  can_add_transaction: boolean;
  can_add_account: boolean;
}

export interface SubscriptionLimits {
  free: {
    max_transactions: number;
    max_accounts: number;
    name: string;
  };
  plus: {
    max_transactions: number;
    max_accounts: number;
    name: string;
  };
  pro: {
    max_transactions: number;
    max_accounts: number;
    name: string;
  };
}

export interface SubscriptionLimitError {
  type: 'subscription_limit_error';
  message: string;
}
