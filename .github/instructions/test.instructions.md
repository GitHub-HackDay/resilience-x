---
applyTo: "**/tests/**/*.{ts,tsx,py}"
---

# Test Writing Rules (Resilience-X)
- Keep tests **independent**; no cross-test state.
- Web (Playwright): prefer `getByRole` + accessible names; avoid brittle selectors.
- API (pytest): test `/ask` happy path + 1 edge case; mock external calls if needed.
- Include at least one **negative** test per module.
- Name patterns: `*.spec.ts(x)` for web; `test_*.py` for Python.
