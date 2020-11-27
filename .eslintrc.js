module.exports = {
  env: {
    browser: true,
    es2021: true,
    jquery: true
  },
  extends: [
    'eslint:recommended',
    'standard'
  ],
  parserOptions: {
    ecmaVersion: 12
  },
  rules: {
    "semi": ["error", "always"],
    "quotes": ["error", "double"]
  }
}
