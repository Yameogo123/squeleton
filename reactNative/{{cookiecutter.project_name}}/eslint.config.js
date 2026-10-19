// https://docs.expo.dev/guides/using-eslint/
const { defineConfig } = require('eslint/config');
const expoConfig = require('eslint-config-expo/flat');

module.exports = defineConfig([
  expoConfig,
  {
    ignores: ['dist/*', '.expo/*', 'coverage/*'],
    rules: {
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'react/no-danger': 'error',
      'no-eval': 'error',
      'no-implied-eval': 'error',
    },
  },
]);
