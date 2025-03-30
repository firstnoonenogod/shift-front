// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Global page headers
  app: {
    head: {
      title: 'ShirtShop',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
      link: []
    }
  },

  // Development server configuration
  devServer: {
    port: 3000,
  },

  // Modules
  modules: [],

  // Auto import components
  components: true,

  // CSS global styles
  css: ['~/assets/css/main.css'],

  // Build configuration
  build: {},

  // Enable Vue devtools
  devtools: { enabled: true },

  compatibilityDate: '2025-02-27'
})