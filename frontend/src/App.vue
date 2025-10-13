<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { RouterView, useRoute } from "vue-router";
import Navigation from "@/components/Navigation.vue";

const authStore = useAuthStore();
const route = useRoute();

// Show navigation only when user is authenticated and not on guest-only pages
const showNavigation = computed(() => {
  return authStore.isAuthenticated && !route.meta.requiresGuest;
});

onMounted(() => {
  authStore.initializeAuth();
});
</script>

<template>
  <div id="app">
    <div class="min-h-screen bg-gray-50">
      <Navigation v-if="showNavigation" />
      <div class="w-full overflow-x-hidden">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>