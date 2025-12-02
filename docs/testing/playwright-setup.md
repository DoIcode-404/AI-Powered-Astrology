# Playwright E2E Testing Setup Guide

## Overview

This guide provides comprehensive instructions for setting up, configuring, and running Playwright-based end-to-end tests for the Astrology Flutter Application. These tests validate critical user journeys from a user's perspective using a real browser.

## Prerequisites

### System Requirements
- Node.js 16+ and npm/yarn
- Python 3.8+ (for backend API server)
- Git
- A text editor or IDE (VS Code recommended)

### Project Requirements
- Flutter app built and deployable to web
- Backend API server running locally or accessible via environment variables
- Test data and mock API responses configured

## Installation

### 1. Install Node.js Dependencies

```bash
# Navigate to project root
cd /path/to/project

# Install Playwright and dependencies
npm install --save-dev @playwright/test

# Or with yarn
yarn add --dev @playwright/test
```

### 2. Install Playwright Browsers

```bash
# Install required browsers (Chromium, Firefox, WebKit)
npx playwright install

# Or specific browsers
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

### 3. Verify Installation

```bash
# Check Playwright version
npx playwright --version

# Run a quick test
npx playwright test --help
```

## Project Structure

```
tests/
├── e2e/
│   ├── onboarding.spec.ts
│   ├── horoscope.spec.ts
│   ├── birth-chart.spec.ts
│   ├── compatibility.spec.ts
│   └── auth.spec.ts
├── fixtures/
│   ├── test-data.ts
│   ├── mock-api-responses.ts
│   └── auth.fixture.ts
├── helpers/
│   ├── common-selectors.ts
│   ├── navigation-helpers.ts
│   └── api-mock-helpers.ts
├── config/
│   └── test-config.ts
└── playwright.config.ts
```

## Configuration

### 1. Create `playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 2. Environment Configuration

Create `.env.test`:

```env
# API Configuration
API_BASE_URL=http://localhost:3000
API_TIMEOUT=30000

# Test Database
TEST_DB_URL=mongodb://localhost:27017/astrology_test

# App Configuration
APP_URL=http://localhost:5000
APP_ENV=test

# Authentication
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=TestPassword123!

# Feature Flags
ENABLE_MOCK_API=true
ENABLE_TEST_DATA=true
```

## Starting Services

### 1. Start Flutter Web App (Development)

```bash
# Build Flutter web app
flutter build web

# Or run in development mode
flutter run -d chrome

# App should be accessible at http://localhost:5000
```

### 2. Start Backend API Server

```bash
# From server directory
cd server

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# API should be accessible at http://localhost:3000
```

### 3. Prepare Test Database

```bash
# Start MongoDB (if using local instance)
mongod --dbpath ./data

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Seed test data
npm run seed:test-data
```

## Writing Tests

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
    await page.goto('/');
    await page.fill('input[name="email"]', 'test@example.com');
  });

  test('user can complete workflow', async ({ page }) => {
    // Act
    await page.click('button[type="submit"]');

    // Wait for navigation
    await page.waitForURL('**/dashboard');

    // Assert
    await expect(page.locator('text=Welcome')).toBeVisible();
  });
});
```

### Using Test Fixtures

Create `tests/fixtures/auth.fixture.ts`:

```typescript
import { test as base } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard');

    // Provide authenticated page to test
    await use(page);

    // Cleanup after test
    await page.goto('/logout');
  },
});
```

Use in tests:

```typescript
import { test } from './fixtures/auth.fixture';

test('authenticated user can view dashboard', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.locator('text=Dashboard')).toBeVisible();
});
```

### Mocking API Responses

```typescript
test('handles API error gracefully', async ({ page }) => {
  // Mock API error response
  await page.route('**/api/horoscope/**', route => {
    route.abort('failed');
  });

  await page.goto('/horoscope');

  // Verify error message displays
  await expect(page.locator('text=Failed to load horoscope')).toBeVisible();
});
```

### Common Test Patterns

#### Waiting for Elements

```typescript
// Wait for specific element
await page.waitForSelector('[data-testid="horoscope-card"]');

// Wait for element to be visible
await expect(page.locator('[data-testid="horoscope-card"]')).toBeVisible();

// Wait for element to be hidden
await expect(page.locator('.loading-spinner')).toBeHidden();

// Wait for network activity
await page.waitForLoadState('networkidle');
```

#### Filling Forms

```typescript
// Fill text input
await page.fill('input[name="email"]', 'test@example.com');

// Select dropdown option
await page.selectOption('select[name="timezone"]', 'America/New_York');

// Check checkbox
await page.check('input[type="checkbox"]');

// Type slowly (useful for triggering input handlers)
await page.type('input[name="search"]', 'Aries', { delay: 100 });
```

#### Navigation & URL

```typescript
// Navigate to URL
await page.goto('/dashboard');

// Wait for URL change
await page.waitForURL('**/success');

// Get current URL
const url = page.url();

// Go back
await page.goBack();
```

## Running Tests

### Run All Tests

```bash
# Run all E2E tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific test file
npx playwright test tests/e2e/horoscope.spec.ts

# Run tests matching pattern
npx playwright test --grep "horoscope"
```

### Run Tests in Debug Mode

```bash
# Open Playwright Inspector
npx playwright test --debug

# Run in UI mode (interactive)
npx playwright test --ui
```

### Run Specific Browsers

```bash
# Chrome only
npx playwright test --project=chromium

# Mobile testing
npx playwright test --project="Mobile Chrome"

# All projects
npx playwright test
```

## Viewing Test Results

### HTML Report

```bash
# View test results in browser
npx playwright show-report

# Report includes:
# - Test results and timing
# - Screenshots (on failure)
# - Videos (on failure)
# - Trace files (for debugging)
```

### Console Output

```bash
# Verbose output
npx playwright test --reporter=verbose

# List tests without running
npx playwright test --list
```

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Start services
        run: |
          npm run start:app &
          npm run start:api &
          sleep 10

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Best Practices

### Selectors
```typescript
// ✅ Prefer data-testid (most reliable)
await page.click('[data-testid="submit-button"]');

// ✅ Use semantic selectors
await page.click('button:has-text("Submit")');

// ❌ Avoid brittle CSS selectors
await page.click('.button.primary.large'); // Changes frequently
```

### Waits
```typescript
// ✅ Use explicit waits
await page.waitForSelector('[data-testid="result"]');

// ✅ Wait for network activity
await page.waitForLoadState('networkidle');

// ❌ Avoid arbitrary delays
// await page.waitForTimeout(5000); // Bad practice
```

### Test Independence
```typescript
// ✅ Each test is completely independent
test('user can create horoscope', async ({ page }) => {
  await page.goto('/');
  // Complete workflow...
});

// ❌ Don't rely on test order
// This test depends on previous test setting up state
test('user can view created horoscope', async ({ page }) => {
  // Assumes previous test ran successfully
});
```

## Troubleshooting

### Common Issues

#### Tests Timeout
```bash
# Increase timeout for specific test
test('long-running test', async ({ page }) => {
  // ...
}, { timeout: 60000 });

# Or in config
timeout: 60000,
```

#### Browser Fails to Start
```bash
# Reinstall browsers
npx playwright install --with-deps

# Check for missing system dependencies (Linux)
npx playwright install-deps
```

#### Flaky Tests
- Add explicit waits instead of delays
- Use `waitForLoadState('networkidle')`
- Ensure test data is reset between runs
- Check for race conditions in your code

#### Tests Pass Locally, Fail in CI
- Verify environment variables are set in CI
- Check that services are fully started before tests
- Ensure test database is clean
- Review CI logs for error messages

## Performance Optimization

### Parallel Execution
```typescript
// Run tests in parallel (default)
fullyParallel: true,

// Control worker count
workers: 4,
```

### Test Sharding (Distribute across machines)
```bash
# Run first shard (CI machine 1)
npx playwright test --shard=1/3

# Run second shard (CI machine 2)
npx playwright test --shard=2/3

# Run third shard (CI machine 3)
npx playwright test --shard=3/3
```

## Advanced Features

### Visual Comparisons

```typescript
test('horoscope card layout is correct', async ({ page }) => {
  await page.goto('/horoscope');

  // Take screenshot and compare
  await expect(page).toHaveScreenshot('horoscope-card.png');
});
```

### Accessibility Testing

```typescript
import { injectAxe, checkA11y } from 'axe-playwright';

test('page is accessible', async ({ page }) => {
  await page.goto('/');

  // Inject axe core
  await injectAxe(page);

  // Check accessibility
  await checkA11y(page);
});
```

## Useful Resources

- [Playwright Documentation](https://playwright.dev)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Tests](https://playwright.dev/docs/debug)
- [Test Configuration](https://playwright.dev/docs/test-configuration)

## Getting Help

For Playwright-specific questions and expert guidance on E2E test design and implementation, refer to the [testing-agent](../agents/testing-agent.md).

## Quick Reference Commands

```bash
# Install & Setup
npm install --save-dev @playwright/test
npx playwright install

# Running Tests
npx playwright test                    # Run all tests
npx playwright test --headed           # See browser
npx playwright test --debug            # Debug mode
npx playwright test --ui               # Interactive mode
npx playwright test tests/e2e/horoscope.spec.ts  # Specific file

# Viewing Results
npx playwright show-report             # View HTML report

# CI/CD
npx playwright test --shard=1/3        # Run first shard
```

---

**Last Updated**: November 2024
**Maintained by**: Testing Agent
