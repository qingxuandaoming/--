import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
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
  },
  server: {
    host: '127.0.0.1',
    proxy: {
      // Python后端 - 装备和爬虫相关API
      '/api/equipment': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      },
      '/api/crawler': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      },
      // Java后端 - 其他所有API
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
