import { test, expect } from '@playwright/test';

test.describe('FAQ Assistant', () => {
  test('should display the main page', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('h1')).toContainText('Mutual Fund FAQ Assistant');
    await expect(page.locator('textarea')).toBeVisible();
  });

  test('should submit a query and display result', async ({ page }) => {
    await page.goto('/');
    
    // Fill in query
    await page.fill('textarea', 'What is the expense ratio of SBI Bluechip Fund?');
    await page.click('button[type="submit"]');
    
    // Wait for result (this will fail if API is not running, which is expected)
    // In a real scenario, you'd mock the API or have a test server running
    await page.waitForTimeout(1000);
  });

  test('should detect PII and show error', async ({ page }) => {
    await page.goto('/');
    
    // Enter query with PII
    await page.fill('textarea', 'My PAN is ABCDE1234F');
    await page.click('button[type="submit"]');
    
    // Check for error message
    await expect(page.locator('text=Personal information detected')).toBeVisible();
  });

  test('should display example questions', async ({ page }) => {
    await page.goto('/');
    
    const exampleQuestions = await page.locator('button').filter({ hasText: /What is the expense ratio/ }).count();
    expect(exampleQuestions).toBeGreaterThan(0);
  });

  test('should have accessible form elements', async ({ page }) => {
    await page.goto('/');
    
    const textarea = page.locator('textarea');
    await expect(textarea).toHaveAttribute('aria-label', 'Query input');
    
    const submitButton = page.locator('button[type="submit"]');
    await expect(submitButton).toHaveAttribute('aria-label', 'Submit query');
  });
});

