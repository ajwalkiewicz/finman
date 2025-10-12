import { useAuthStore } from "@/stores/auth";
import Accounts from "@/views/Accounts.vue";
import Analytics from "@/views/Analytics.vue";
import Dashboard from "@/views/Dashboard.vue";
import Login from "@/views/Login.vue";
import Settings from "@/views/Settings.vue";
import Transactions from "@/views/Transactions.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresGuest: true },
  },
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/transactions",
    name: "Transactions",
    component: Transactions,
    meta: { requiresAuth: true },
  },
  {
    path: "/accounts",
    name: "Accounts",
    component: Accounts,
    meta: { requiresAuth: true },
  },
  {
    path: "/analytics",
    name: "Analytics",
    component: Analytics,
    meta: { requiresAuth: true },
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next("/");
  } else {
    next();
  }
});

export default router;
