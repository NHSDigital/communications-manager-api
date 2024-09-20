module.exports = {
  root: true,
  parser: "@babel/eslint-parser",
  parserOptions: {
    requireConfigFile: false,
  },
  env: {
    browser: true,
    jest: true,
    node: true,
  },
  extends: [
    'airbnb-base',
    'eslint:recommended',
    'plugin:security/recommended',
    'prettier',
  ],
  plugins: [
    'html',
    'import',
    'security',
  ],
  rules: {
    camelcase: 'warn',
    'class-methods-use-this': 0,
    'comma-dangle': ['error', 'only-multiline'],
    'import/no-extraneous-dependencies': [
      'error',
      {
        devDependencies: [
          '.eslintrc.js',
          '**/*.test.[jt]s?(x)',
          '**/__test__/**/*.js',
          '**/tests/**/*.[jt]s?(x)',
          '**/test-config/*.js',
        ],
      },
    ],
    'import/no-unresolved': [
      'error',
      {
        ignore: [
          'jose', // jose uses package exports which the current resolver does not understand
          'aws-lambda', // linting not able to find resolve the path even though it does resolve building
        ],
      },
    ],
    'no-plusplus': [
      'error',
      {
        allowForLoopAfterthoughts: true,
      },
    ],
    'import/prefer-default-export': 0,
    'jsx-a11y/anchor-is-valid': [0],
    'linebreak-style': ['error', 'unix'],
    'no-await-in-loop': 'off',
    'no-case-declarations': 0,
    'no-nested-ternary': 0,
    'no-return-await': 0,
    'no-restricted-syntax': [
      'error',
      'ForInStatement',
      'LabeledStatement',
      'WithStatement',
    ],
    'no-shadow': 0,
    'no-underscore-dangle': 0,
    'no-use-before-define': 0,
    radix: 0,
    'security/detect-object-injection': 0,
    'import/extensions': 0,
  },
  overrides: [
    {
      files: ['sandbox/**'],
      rules: {
        'security/detect-non-literal-fs-filename': 'off',
      },
    },
    {
      files: ['sandbox/index.js'],
      rules: {
        'no-console': 'off',
      },
    },
  ],
  ignorePatterns: [
    'target',
    'jest.config.js',
  ],
};
