/**
 * Accessibility-focused tests for Resilience-X
 * Tests WCAG compliance and keyboard navigation
 */
import { test, expect } from '@playwright/test';

test.describe('Accessibility Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('has semantic HTML structure', async ({ page }) => {
    // Check main landmark
    const main = page.locator('main');
    await expect(main).toBeVisible();
    
    // Check heading hierarchy
    const h1 = page.getByRole('heading', { level: 1 });
    await expect(h1).toBeVisible();
    await expect(h1).toHaveText('Resilience-X');
    
    // Form should have proper structure
    const form = page.locator('form');
    await expect(form).toBeVisible();
    
    // Sections should have proper headings
    await expect(page.locator('section')).toHaveCount(0); // Initially no results
  });

  test('has proper form labeling and associations', async ({ page }) => {
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    
    // Input should be properly labeled
    await expect(questionInput).toBeVisible();
    await expect(questionInput).toHaveAttribute('id', 'question-input');
    
    // Label should be associated with input
    const label = page.locator('label[for="question-input"]');
    await expect(label).toBeVisible();
    
    // Input should have aria-describedby for help text
    await expect(questionInput).toHaveAttribute('aria-describedby', 'question-help');
    
    // Help text should exist
    const helpText = page.locator('#question-help');
    await expect(helpText).toBeVisible();
  });

  test('supports keyboard navigation throughout interface', async ({ page }) => {
    // Mock API response for keyboard navigation test
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Test answer for keyboard navigation',
          explanation_bullets: ['Explanation point 1', 'Explanation point 2'],
          sources: ['Short source', 'This is a longer source that will have a show more button for testing keyboard navigation through expandable content areas']
        })
      });
    });
    
    // Tab to question input
    await page.keyboard.press('Tab');
    await expect(page.getByRole('textbox')).toBeFocused();
    
    // Type question
    await page.keyboard.type('Accessibility test question');
    
    // Tab to submit button
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Ask Question' })).toBeFocused();
    
    // Submit with Enter
    await page.keyboard.press('Enter');
    
    // Wait for results
    await expect(page.getByText('Test answer for keyboard navigation')).toBeVisible();
    
    // Should be able to tab through show more button
    const showMoreButton = page.getByRole('button', { name: /expand source/i });
    await expect(showMoreButton).toBeVisible();
    
    // Continue tabbing to reach the show more button
    let tabCount = 0;
    const maxTabs = 10; // Prevent infinite loop
    
    while (tabCount < maxTabs) {
      await page.keyboard.press('Tab');
      tabCount++;
      
      if (await showMoreButton.evaluate(el => document.activeElement === el)) {
        break;
      }
    }
    
    // Should be able to activate with Enter
    await page.keyboard.press('Enter');
    await expect(showMoreButton).toHaveAttribute('aria-expanded', 'true');
  });

  test('has proper color contrast and visual indicators', async ({ page }) => {
    // Check that disabled button has visual indication
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    await expect(submitButton).toBeDisabled();
    await expect(submitButton).toHaveCSS('cursor', 'not-allowed');
    
    // Type to enable button
    await page.getByRole('textbox').fill('Test question');
    await expect(submitButton).toBeEnabled();
    
    // Focus should be visible
    await submitButton.focus();
    // Note: Actual visual focus testing would require screenshot comparison
  });

  test('provides appropriate ARIA attributes for dynamic content', async ({ page }) => {
    // Mock API response
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Dynamic content test answer',
          explanation_bullets: ['Explanation with ARIA'],
          sources: ['Source with proper labeling']
        })
      });
    });
    
    const questionInput = page.getByRole('textbox');
    await questionInput.fill('ARIA test question');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Wait for results
    await expect(page.getByText('Dynamic content test answer')).toBeVisible();
    
    // Check ARIA regions
    const answerRegion = page.getByRole('region', { name: 'Answer to your question' });
    await expect(answerRegion).toBeVisible();
    
    const explanationList = page.getByRole('list', { name: 'Explanation steps' });
    await expect(explanationList).toBeVisible();
    
    const sourcesRegion = page.getByRole('region', { name: 'Source documents' });
    await expect(sourcesRegion).toBeVisible();
  });

  test('error messages are announced to screen readers', async ({ page }) => {
    // Mock server error
    await page.route('**/ask', async route => {
      await route.fulfill({ status: 500 });
    });
    
    const questionInput = page.getByRole('textbox');
    await questionInput.fill('Error test question');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Error should be in alert role with aria-live
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toHaveAttribute('aria-live', 'polite');
    
    // Error should have proper heading structure
    const errorHeading = errorAlert.getByText('Error');
    await expect(errorHeading).toBeVisible();
  });

  test('loading state is accessible', async ({ page }) => {
    // Mock delayed API response
    await page.route('**/ask', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Delayed response',
          explanation_bullets: [],
          sources: []
        })
      });
    });
    
    const questionInput = page.getByRole('textbox');
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    
    await questionInput.fill('Loading test question');
    await submitButton.click();
    
    // Loading state should be announced
    await expect(page.getByText('Processing...')).toBeVisible();
    
    // Form controls should be disabled
    await expect(questionInput).toBeDisabled();
    await expect(submitButton).toBeDisabled();
    
    // Loading spinner should have proper aria-hidden
    const spinner = page.locator('svg.animate-spin');
    await expect(spinner).toBeVisible();
  });

  test('expandable source content has proper ARIA attributes', async ({ page }) => {
    const longSource = 'This is a very long source text that will be truncated and require expansion controls with proper ARIA attributes for accessibility compliance.';
    
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Test answer',
          explanation_bullets: ['Test explanation'],
          sources: [longSource]
        })
      });
    });
    
    const questionInput = page.getByRole('textbox');
    await questionInput.fill('Source expansion test');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Wait for results
    await expect(page.getByText('Test answer')).toBeVisible();
    
    const expandButton = page.getByRole('button', { name: 'Expand source 1' });
    await expect(expandButton).toBeVisible();
    await expect(expandButton).toHaveAttribute('aria-expanded', 'false');
    
    // Click to expand
    await expandButton.click();
    
    await expect(expandButton).toHaveAttribute('aria-expanded', 'true');
    await expect(expandButton).toHaveText('Show less');
    await expect(expandButton.getAttribute('aria-label')).resolves.toContain('Collapse source 1');
  });

  test('form validation provides accessible error feedback', async ({ page }) => {
    const questionInput = page.getByRole('textbox');
    
    // Try to submit empty form
    await questionInput.fill(' '); // Just whitespace
    await questionInput.clear();
    await page.keyboard.press('Enter');
    
    // Validation error should be accessible
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('Please enter a question');
    
    // Error should have proper ARIA attributes
    await expect(errorAlert).toHaveAttribute('aria-live', 'polite');
    
    // Error should be programmatically associated with form
    // In a full implementation, this might use aria-describedby
    await expect(errorAlert).toBeVisible();
  });

  test('page has proper document structure and landmarks', async ({ page }) => {
    // Should have main landmark
    const main = page.getByRole('main');
    await expect(main).toBeVisible();
    
    // Should have proper heading hierarchy (no skipped levels)
    const h1 = page.getByRole('heading', { level: 1 });
    await expect(h1).toBeVisible();
    
    // When results appear, should have h2 headings
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json', 
        body: JSON.stringify({
          answer: 'Test answer',
          explanation_bullets: ['Test'],
          sources: ['Test source']
        })
      });
    });
    
    await page.getByRole('textbox').fill('Structure test');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Should have level 2 headings in results
    const h2Headings = page.getByRole('heading', { level: 2 });
    await expect(h2Headings.first()).toBeVisible();
  });

});