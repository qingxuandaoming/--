import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  define: {
    global: 'globalThis',
  },
  optimizeDeps: {
    exclude: ['mysql2']
  },
  build: {
    rollupOptions: {
      external: ['mysql2', 'fs', 'path', 'crypto']
    }
  }
})
