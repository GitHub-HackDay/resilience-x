/**
 * End-to-end tests for Resilience-X main page
 * Tests the complete user journey and accessibility
 */
import { test, expect } from '@playwright/test';

test.describe('Resilience-X Main Page', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('has correct title and heading', async ({ page }) => {
    // Verify page title
    await expect(page).toHaveTitle('Resilience-X');
    
    // Verify main heading
    await expect(page.getByRole('heading', { name: 'Resilience-X', level: 1 })).toBeVisible();
    
    // Verify subtitle
    await expect(page.getByText('AI-powered crisis recovery Q&A with explainability')).toBeVisible();
  });

  test('displays question input form with proper accessibility', async ({ page }) => {
    // Check label is present and associated with input
    const label = page.getByText('Ask a question about crisis recovery:');
    await expect(label).toBeVisible();
    
    // Check textarea is properly labeled
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await expect(questionInput).toBeVisible();
    await expect(questionInput).toHaveAttribute('id', 'question-input');
    
    // Check placeholder text
    await expect(questionInput).toHaveAttribute('placeholder', 'e.g., Which neighborhoods are facing cleanup delays?');
    
    // Check help text is present and associated
    await expect(page.getByText('Ask about recovery status, bottlenecks')).toBeVisible();
    
    // Check submit button
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    await expect(submitButton).toBeVisible();
    await expect(submitButton).toBeDisabled(); // Should be disabled when input is empty
  });

  test('enables submit button when question is entered', async ({ page }) => {
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    
    // Initially disabled
    await expect(submitButton).toBeDisabled();
    
    // Type question
    await questionInput.fill('Which roads are blocked?');
    
    // Should be enabled now
    await expect(submitButton).toBeEnabled();
    
    // Clear input
    await questionInput.clear();
    
    // Should be disabled again
    await expect(submitButton).toBeDisabled();
  });

  test('shows validation error for empty question', async ({ page }) => {
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    
    // Add and remove text to enable button, then clear
    await questionInput.fill(' '); // Space character
    await questionInput.clear();
    
    // Try to submit
    await questionInput.press('Enter');
    
    // Should show validation error
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('Please enter a question');
  });

  test('shows loading state when submitting question', async ({ page }) => {
    // Mock API to delay response
    await page.route('**/ask', async route => {
      await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Test answer',
          explanation_bullets: ['Test explanation'],
          sources: ['Test source']
        })
      });
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    
    await questionInput.fill('Which roads are blocked?');
    await submitButton.click();
    
    // Should show loading state
    await expect(page.getByText('Processing...')).toBeVisible();
    await expect(submitButton).toBeDisabled();
    await expect(questionInput).toBeDisabled();
    
    // Wait for response
    await expect(page.getByText('Test answer')).toBeVisible();
  });

  test('displays successful API response with proper structure', async ({ page }) => {
    // Mock successful API response
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Highway 520 remains blocked while Redmond Way is partially cleared.',
          explanation_bullets: [
            'Highway 520 has significant debris from storm damage',
            'Redmond Way cleanup is 60% complete as of today'
          ],
          sources: [
            'Traffic Report C: Highway 520 Status Update from DOT',
            'City Update D: Redmond Infrastructure Recovery Progress'
          ]
        })
      });
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    const submitButton = page.getByRole('button', { name: 'Ask Question' });
    
    await questionInput.fill('Which roads are still blocked near Redmond?');
    await submitButton.click();
    
    // Check Answer section
    await expect(page.getByRole('heading', { name: 'Answer', level: 2 })).toBeVisible();
    await expect(page.getByText('Highway 520 remains blocked while Redmond Way')).toBeVisible();
    
    // Check Why section
    await expect(page.getByRole('heading', { name: 'Why', level: 2 })).toBeVisible();
    const explanationList = page.getByRole('list', { name: 'Explanation steps' });
    await expect(explanationList).toBeVisible();
    await expect(explanationList.getByText('Highway 520 has significant debris')).toBeVisible();
    await expect(explanationList.getByText('Redmond Way cleanup is 60% complete')).toBeVisible();
    
    // Check Sources section
    await expect(page.getByRole('heading', { name: 'Sources', level: 2 })).toBeVisible();
    const sourcesRegion = page.getByRole('region', { name: 'Source documents' });
    await expect(sourcesRegion).toBeVisible();
    await expect(sourcesRegion.getByText('Traffic Report C')).toBeVisible();
    await expect(sourcesRegion.getByText('City Update D')).toBeVisible();
  });

  test('handles source text truncation and expansion', async ({ page }) => {
    // Mock API with long source text
    const longSourceText = 'This is a very long source text that should be truncated when initially displayed. It contains lots of information about the current status of recovery efforts and detailed information about various aspects of the cleanup process.';
    
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: 'Test answer',
          explanation_bullets: ['Test explanation'],
          sources: [longSourceText]
        })
      });
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await questionInput.fill('Test question?');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Should initially show truncated text
    await expect(page.getByText('This is a very long source text that should be truncated when initially displayed. It con...')).toBeVisible();
    
    // Should have "Show more" button
    const showMoreButton = page.getByRole('button', { name: 'Expand source 1' });
    await expect(showMoreButton).toBeVisible();
    await expect(showMoreButton).toHaveText('Show more');
    
    // Click to expand
    await showMoreButton.click();
    
    // Should show full text
    await expect(page.getByText(longSourceText)).toBeVisible();
    
    // Button should change to "Show less"
    await expect(showMoreButton).toHaveText('Show less');
    await expect(showMoreButton).toHaveAttribute('aria-expanded', 'true');
    
    // Click to collapse
    await showMoreButton.click();
    
    // Should show truncated text again
    await expect(page.getByText('This is a very long source text that should be truncated when initially displayed. It con...')).toBeVisible();
    await expect(showMoreButton).toHaveAttribute('aria-expanded', 'false');
  });

  test('handles network error gracefully', async ({ page }) => {
    // Mock network error
    await page.route('**/ask', async route => {
      await route.abort('failed');
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await questionInput.fill('Test question?');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Should show network error
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('Unable to connect to the service');
    await expect(errorAlert.getByText('Error')).toBeVisible();
  });

  test('handles server error gracefully', async ({ page }) => {
    // Mock server error
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' })
      });
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await questionInput.fill('Test question?');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Should show server error
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
    await expect(errorAlert).toContainText('An error occurred while processing');
  });

  test('supports keyboard navigation', async ({ page }) => {
    // Tab through interface
    await page.keyboard.press('Tab'); // Should focus question input
    await expect(page.getByRole('textbox', { name: /ask a question about crisis recovery/i })).toBeFocused();
    
    // Type question
    await page.keyboard.type('Which areas need priority attention?');
    
    // Tab to submit button
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Ask Question' })).toBeFocused();
    
    // Should be able to submit with Enter
    await expect(page.getByRole('button', { name: 'Ask Question' })).toBeEnabled();
  });

  test('has proper ARIA live regions for dynamic content', async ({ page }) => {
    // Check error region has aria-live
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await questionInput.fill(' ');
    await questionInput.clear();
    await page.keyboard.press('Enter');
    
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toHaveAttribute('aria-live', 'polite');
  });

}); // End describe block

// Negative test cases in separate describe block
test.describe('Resilience-X Error Handling', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('handles malformed API response', async ({ page }) => {
    // Mock malformed API response
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: 'invalid json response'
      });
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await questionInput.fill('Test question?');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Should handle gracefully
    const errorAlert = page.getByRole('alert');
    await expect(errorAlert).toBeVisible();
  });

  test('handles empty API response fields', async ({ page }) => {
    // Mock API response with empty fields
    await page.route('**/ask', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          answer: '',
          explanation_bullets: [],
          sources: []
        })
      });
    });
    
    const questionInput = page.getByRole('textbox', { name: /ask a question about crisis recovery/i });
    await questionInput.fill('Test question?');
    await page.getByRole('button', { name: 'Ask Question' }).click();
    
    // Should display response sections but handle empty content gracefully
    await expect(page.getByRole('heading', { name: 'Answer', level: 2 })).toBeVisible();
    
    // Why section should not appear if explanation_bullets is empty
    await expect(page.getByRole('heading', { name: 'Why', level: 2 })).not.toBeVisible();
    
    // Sources section should not appear if sources is empty  
    await expect(page.getByRole('heading', { name: 'Sources', level: 2 })).not.toBeVisible();
  });

});