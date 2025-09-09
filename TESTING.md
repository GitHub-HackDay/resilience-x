# Testing Documentation - Resilience-X

This document describes the comprehensive testing strategy and infrastructure for the Resilience-X project.

## Test Architecture

The testing infrastructure follows a multi-layered approach:

1. **Unit Tests** - Individual component and function testing
2. **Integration Tests** - Service interaction testing with mocking
3. **End-to-End Tests** - Complete user journey testing
4. **Accessibility Tests** - WCAG compliance and keyboard navigation
5. **Performance Tests** - Load and reliability testing

## Test Structure

```
tests/
├── api/                     # Backend API tests (pytest)
│   ├── test_main.py        # Core API endpoint tests
│   └── test_integration.py # External service integration tests
├── web/                    # Frontend tests (Playwright)
│   ├── main-page.spec.ts   # Main page functionality tests
│   └── accessibility.spec.ts # Accessibility compliance tests
└── integration/            # End-to-end integration tests
    └── test_e2e.py         # Complete system integration tests
```

## Backend Testing (Python/FastAPI)

### Technologies Used
- **pytest** - Test framework
- **pytest-asyncio** - Async test support
- **pytest-mock** - Mocking utilities
- **httpx** - HTTP client for testing
- **TestClient** - FastAPI test client

### Test Categories

#### Unit Tests (`tests/api/test_main.py`)
- Health endpoint validation
- `/ask` endpoint functionality
- Request/response model validation
- CORS configuration testing
- Error handling scenarios

#### Integration Tests (`tests/api/test_integration.py`)
- Mocked Weaviate client integration
- Mocked GraphRAG client integration
- Complete pipeline flow testing
- Configuration and logging validation
- Timeout and error handling

### Running API Tests
```bash
# From project root
cd services/api
python -m pytest ../../tests/api/ -v

# With coverage
python -m pytest ../../tests/api/ -v --cov=. --cov-report=term-missing

# Specific test file
python -m pytest ../../tests/api/test_main.py -v
```

## Frontend Testing (Next.js/Playwright)

### Technologies Used
- **Playwright** - End-to-end testing framework
- **TypeScript** - Type-safe test development
- **Multiple Browsers** - Chrome, Firefox, Safari support

### Test Categories

#### Main Page Tests (`tests/web/main-page.spec.ts`)
- Page title and heading validation
- Form functionality and validation
- API integration with various response scenarios
- Loading states and error handling
- Source text truncation and expansion
- Keyboard navigation support

#### Accessibility Tests (`tests/web/accessibility.spec.ts`)
- Semantic HTML structure validation
- ARIA attributes and roles
- Keyboard navigation compliance
- Screen reader compatibility
- WCAG 2.1 compliance checks
- Focus management and visual indicators

### Running Web Tests
```bash
# From project root
cd apps/web
npm run test

# With UI mode
npm run test:ui

# In headed mode (visible browser)
npm run test:headed

# Specific test file
npx playwright test tests/web/main-page.spec.ts
```

## Integration Testing

### End-to-End Tests (`tests/integration/test_e2e.py`)
- Complete system integration validation
- Data flow and transformation testing
- Service integration patterns
- Performance and reliability testing
- Input validation robustness

### Service Integration Patterns
The integration tests define expected patterns for:
- **Weaviate Integration**: Vector search with metadata
- **GraphRAG Integration**: Multi-hop reasoning with explanation
- **Error Handling**: Graceful degradation and fallbacks

## Test Configuration

### Pytest Configuration (`services/api/pyproject.toml`)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"] 
python_functions = ["test_*"]
addopts = "-v --tb=short --cov=services/api --cov-report=term-missing"
asyncio_mode = "auto"
```

### Playwright Configuration (`apps/web/playwright.config.ts`)
- Multi-browser testing (Chromium, Firefox, WebKit)
- Automatic server startup for testing
- Trace collection on test failures
- Parallel test execution

## Running All Tests

### Quick Start
```bash
# Setup development environment
./scripts/setup-dev.sh

# Run all tests
./scripts/test.sh

# Run specific test suites
./scripts/test.sh --api-only    # Only API tests
./scripts/test.sh --web-only    # Only web tests
./scripts/test.sh --no-lint     # Skip linting
```

### Manual Testing
```bash
# API tests only
cd services/api && python -m pytest ../../tests/api/ ../../tests/integration/ -v

# Web tests only  
cd apps/web && npm run test

# Linting
cd services/api && python -m black --check . && python -m flake8 .
cd apps/web && npm run lint
```

## Test Guidelines

### Writing Tests
1. **Independent Tests** - No cross-test state dependencies
2. **Clear Naming** - Descriptive test function names
3. **Arrange-Act-Assert** - Clear test structure
4. **Mock External Services** - No real API calls in tests
5. **Both Positive and Negative Cases** - Happy path and error scenarios

### API Test Patterns
```python
def test_endpoint_happy_path():
    """Test successful request processing"""
    client = TestClient(app)
    response = client.post("/ask", json={"question": "Test?"})
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["explanation_bullets"], list)
```

### Web Test Patterns
```typescript
test('has accessible form controls', async ({ page }) => {
  await page.goto('/');
  
  const input = page.getByRole('textbox', { name: /ask a question/i });
  await expect(input).toBeVisible();
  
  const button = page.getByRole('button', { name: 'Ask Question' });
  await expect(button).toBeVisible();
});
```

## Coverage Targets

- **API Coverage**: >90% line coverage
- **Web Coverage**: Complete user journey coverage  
- **Integration Coverage**: All service integration points
- **Accessibility Coverage**: WCAG 2.1 AA compliance
- **Error Coverage**: All error scenarios handled

## Continuous Integration

Tests are designed to run in CI environments with:
- Parallel execution for speed
- Deterministic results (no flaky tests)
- Comprehensive error reporting
- Coverage reporting
- Multiple browser testing

## Troubleshooting

### Common Issues

1. **Playwright Browser Not Found**
   ```bash
   cd apps/web && npx playwright install
   ```

2. **Python Module Import Errors**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/services/api"
   ```

3. **CORS Issues in Tests**
   - Ensure TestClient includes proper Origin headers
   - Verify CORS middleware configuration

4. **Async Test Issues**
   - Use `pytest-asyncio` for async functions
   - Mark tests with `@pytest.mark.asyncio`

### Debug Mode

Enable debug logging and verbose output:
```bash
# API tests with debug
python -m pytest ../../tests/api/ -v -s --log-cli-level=DEBUG

# Web tests with debug  
DEBUG=pw:api npm run test
```

## Future Enhancements

Planned testing improvements:
- Visual regression testing
- Load testing with realistic scenarios
- Security testing (OWASP compliance)
- Mobile responsiveness testing
- Performance benchmarking
- Contract testing between frontend and API