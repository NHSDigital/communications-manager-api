const {
  rules: baseBestPracticesRules,
} = require("eslint-config-airbnb-base/rules/best-practices");

module.exports = {
  root: true,
  env: {
    browser: true,
    jest: true,
    node: true,
  },
  parser: "@typescript-eslint/parser",
  extends: [
    "airbnb",
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:import/typescript",
    "plugin:react/recommended",
    "plugin:security/recommended",
    "prettier",
  ],
  plugins: [
    "@typescript-eslint",
    "html",
    "import",
    "react",
    "react-hooks",
    "security",
  ],
  globals: {
    Atomics: "readonly",
    React: "writable",
    SharedArrayBuffer: "readonly",
  },
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-non-null-assertion": 0,
    "@typescript-eslint/no-shadow": "error",
    "@typescript-eslint/no-unused-vars": [
      "error",
      {
        ...baseBestPracticesRules["no-unused-vars"],
        ignoreRestSiblings: true,
        argsIgnorePattern: "^_",
      },
    ],
    camelcase: "warn",
    "class-methods-use-this": 0,
    "comma-dangle": ["error", "only-multiline"],
    "import/no-extraneous-dependencies": [
      "error",
      {
        devDependencies: [
          ".eslintrc.js",
          "next.config.js",
          "**/*.test.[jt]s?(x)",
          "**/dotenvConfig.js",
          "**/webpack.config.js",
          "**/__test__/**/*.js",
          "**/tests/**/*.[jt]s?(x)",
          "**/test-config/*.js",
        ],
      },
    ],
    "import/no-unresolved": [
      "error",
      {
        ignore: [
          "jose", // jose uses package exports which the current resolver does not understand
          "aws-lambda", // linting not able to find resolve the path even though it does resolve building
        ],
      },
    ],
    "no-plusplus": [
      "error",
      {
        allowForLoopAfterthoughts: true,
      },
    ],
    "import/prefer-default-export": 0,
    "jsx-a11y/anchor-is-valid": [0],
    "linebreak-style": ["error", "unix"],
    "no-await-in-loop": "off",
    "no-case-declarations": 0,
    "no-nested-ternary": 0,
    "no-return-await": 0,
    "no-restricted-syntax": [
      "error",
      "ForInStatement",
      "LabeledStatement",
      "WithStatement",
    ],
    "no-shadow": 0,
    "no-underscore-dangle": 0,
    "no-use-before-define": 0,
    radix: 0,
    "react-hooks/exhaustive-deps": "error",
    "react-hooks/rules-of-hooks": "error",
    "react/function-component-definition": 0,
    "react/jsx-filename-extension": 0,
    "react/jsx-no-useless-fragment": ["error", { allowExpressions: true }],
    "react/jsx-props-no-spreading": 0,
    "react/react-in-jsx-scope": "off",
    "security/detect-object-injection": 0,
    "@next/next/no-img-element": "off",
    "import/extensions": 0,
  },
  overrides: [
    {
      // see: https://github.com/B2o5T/graphql-eslint  // TODO: go through the readme an implment graphql eslint properly
      files: ["*.graphql"],
      parser: "@graphql-eslint/eslint-plugin",
      plugins: ["@graphql-eslint"],
      rules: {
        "@graphql-eslint/known-type-names": "error",
      },
      parserOptions: {
        schema: "**/*.graphql",
      },
    },
    {
      files: [
        "sandbox/index.js",
        "**/Performance_MessageBatches.Create.Validate.js",
      ],
      rules: {
        "no-console": "off",
      },
    },
    {
      files: ["test/integration/**"],
      rules: {
        "import/no-extraneous-dependencies": [
          "error",
          { optionalDependencies: false, bundledDependencies: false },
        ],
      },
    },
    {
      files: ["*.js"],
      rules: {
        "@typescript-eslint/explicit-module-boundary-types": 0,
        "@typescript-eslint/no-var-requires": "off",
        "@typescript-eslint/no-empty-function":
          baseBestPracticesRules["no-empty-function"],
      },
    },
    {
      files: ["*.test.*"],
      rules: {
        "@typescript-eslint/no-explicit-any": "off",
      },
    },
    {
      files: ["*.tsx"],
      rules: {
        "react/require-default-props": 0,
      },
    },
    {
      files: ["**/*bearer_token.js"],
      rules: {
        "no-undef": "off",
        camelcase: "off",
        "no-restricted-globals": "off",
        "@typescript-eslint/no-unused-vars": "off",
      },
    },
    {
      files: ["**/HealthCheck.SetResponse.js"],
      rules: {
        "no-undef": "off",
        camelcase: "off",
      },
    },
    {
      files: [
        "**/SetResponseDefaults.js",
        "**/SetBackendCorrelationId.js",
        "**/Routing.CheckValid.js",
        "**/NhsAppAccounts.Ok.Response.js",
        "**/*.Create.*.js",
        "**/500DuplicateTemplates.ExtractDuplicates.js",
      ],
      rules: {
        "no-undef": "off",
      },
    },
    {
      files: ["**/validationChecks.js"],
      rules: {
        "no-undef": "off",
        "@typescript-eslint/no-unused-vars": "off",
        "@typescript-eslint/no-shadow": "off",
      },
    },
    {
      files: [
        "**/helpers/validationErrors.js",
        "**/helpers/responseHelpers.js",
      ],
      rules: {
        "@typescript-eslint/no-unused-vars": "off",
      },
    },
    {
      files: [
        "**/Performance_MessageBatches.Create.Validate.js"
      ],
      rules: {
        "@typescript-eslint/no-unused-vars": "off",
        "no-eval": "off",
      },
    },
  ],
  ignorePatterns: [
    ".next",
    "target",
    "jest.config.js",
    "chd_api_types.ts",
    "**/data_layer/**/*.ts",
  ],
};
