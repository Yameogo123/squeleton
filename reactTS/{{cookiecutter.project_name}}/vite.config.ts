/// <reference types="vitest/config" />
import { fileURLToPath, URL } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'
import { contentSecurityPolicy, securityHeaders } from './security-headers.ts'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_')
  process.env.VITE_API_URL ??= env.VITE_API_URL

  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
    },
    // dev server: no CSP (Vite injects inline HMR scripts), the rest of the headers apply
    server: { port: 5173, strictPort: true, headers: securityHeaders },
    // `npm run preview` serves the production build with the real CSP: test it there
    preview: { port: 4173, headers: { ...securityHeaders, 'Content-Security-Policy': contentSecurityPolicy } },
    build: {
      sourcemap: false, // don't ship source code to production
      target: 'es2022',
    },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./src/tests/setupTests.ts'],
      css: false,
    },
  }
})
