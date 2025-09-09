# Contributing to Resilience-X

Thank you for your interest in contributing to Resilience-X! This guide will help you get started with development and contributions.

## 🚀 Quick Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+ with npm
- Git

### Development Environment Setup

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR-USERNAME/resilience-x.git
cd resilience-x
```

2. **Start dependencies:**
```bash
docker compose up -d weaviate
```

3. **Install dependencies:**
```bash
# Backend
uv sync

# Frontend  
npm ci --prefix apps/web
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🧪 Testing

### Running Tests
```bash
# All tests
uv run pytest -q && npm run test --prefix apps/web

# Backend only
uv run pytest services/api/tests/ -v

# Frontend only
npm run test --prefix apps/web

# With coverage
uv run pytest --cov=services/api services/api/tests/
```

### Writing Tests
- **Backend:** Use pytest with type hints and fixtures
- **Frontend:** Use Playwright for e2e tests, prefer `getByRole`
- **Integration:** Test the `/ask` endpoint with realistic scenarios
- Always include at least one negative test per module

Example backend test:
```python
def test_ask_endpoint_success(client):
    response = client.post("/ask", json={"question": "test question"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "explanation_bullets" in data
    assert "sources" in data
```

Example frontend test:
```typescript
test('should display results after asking question', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('textbox', { name: 'question' }).fill('test question');
  await page.getByRole('button', { name: 'Ask' }).click();
  await expect(page.getByRole('heading', { name: 'Answer' })).toBeVisible();
});
```

## 🎨 Code Style

### Python (Backend)
- Use type hints for all functions and variables
- Follow PEP 8 with line length of 100 characters
- Use docstrings for public functions
- Prefer `pydantic` models for data validation

```python
from typing import List
from pydantic import BaseModel

class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str

async def ask_question(request: AskRequest) -> Dict[str, Any]:
    """Process a question and return structured answer with explainability."""
    # Implementation here
    pass
```

### TypeScript (Frontend)
- Use strict TypeScript mode
- Prefer functional components with hooks
- Use semantic HTML and ARIA attributes for accessibility
- No `any` types - use proper type definitions

```typescript
interface QuestionFormProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
}

export function QuestionForm({ onSubmit, isLoading }: QuestionFormProps) {
  // Implementation here
}
```

### Documentation
- Keep README.md updated with new features
- Include code examples in documentation
- Use clear, concise language
- Add inline comments for complex logic only

## 🏗️ Architecture Guidelines

### Backend Design
- Keep the `/ask` endpoint lightweight and focused
- Use dependency injection for clients (Weaviate, GraphRAG)
- Implement proper error handling and logging
- Return structured JSON with explainability

### Frontend Design
- Single-page application focused on Q&A flow
- Accessible design with keyboard navigation
- Clear visual hierarchy: Question → Answer → Why → Sources
- Progressive enhancement and graceful degradation

### Data Flow
```
User Input → Frontend → /ask API → Weaviate (retrieval) + GraphRAG (reasoning) → Structured Response → Frontend Display
```

## 🔧 Development Workflow

### Making Changes

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make incremental changes:**
- Write tests first (TDD approach recommended)
- Implement the minimal change needed
- Test frequently during development

3. **Validate your changes:**
```bash
# Lint and format
uv run black services/
uv run isort services/
npm run lint --prefix apps/web

# Type checking
uv run mypy services/
npm run type-check --prefix apps/web

# Tests
uv run pytest -q
npm run test --prefix apps/web
```

4. **Commit with clear messages:**
```bash
git add .
git commit -m "feat: add explanation bullet points to GraphRAG integration"
```

### Pull Request Process

1. **Update documentation** if you've made user-facing changes
2. **Add tests** for new functionality
3. **Ensure all tests pass** and code is properly formatted
4. **Create PR with descriptive title and body**
5. **Include demo steps** if applicable

**PR Template:**
```markdown
## Changes Made
- Brief description of changes

## Why
- Reason for the change
- Link to issue if applicable

## Demo Steps (if applicable)
1. Start the application
2. Navigate to...
3. Expected behavior...

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
```

## 🚫 What to Avoid

- **Breaking changes** without discussion
- **Large refactoring** without prior approval
- **Secrets or credentials** in code
- **Dependencies** without security scanning
- **Complex features** that don't align with MVP goals

## 📚 Resources

### Key Technologies
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [GraphRAG Documentation](https://github.com/microsoft/graphrag)

### AI Tools
- Use **GitHub Copilot** for code generation and completion
- Leverage **NLWeb** patterns for natural language interfaces
- Follow **GraphRAG** best practices for explainability

### Getting Help
- Check existing issues and discussions
- Ask questions in PR comments
- Reference the detailed PRD and technical specifications
- Use the built-in Copilot instructions in `.github/`

## 🎯 Contribution Ideas

### High Priority
- Improve error handling and user feedback
- Add more comprehensive tests
- Enhance accessibility features
- Optimize GraphRAG query performance

### Nice to Have
- Visual representation of reasoning paths
- Additional crisis management domains
- Performance monitoring and metrics
- Dark mode support

### Documentation
- Video tutorials and demos
- API usage examples
- Deployment guides
- Architecture deep dives

---

**Thank you for contributing to Resilience-X!** 🚀

Every contribution helps demonstrate the power of AI-native development and makes crisis recovery tools more accessible and effective.