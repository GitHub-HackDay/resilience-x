# Resilience-X Frontend

AI-powered Q&A interface for post-disaster recovery planning.

## Features

- **Single Page Application**: Clean, focused UI with input box and results panel
- **Accessibility First**: Proper ARIA labels, keyboard navigation, and screen reader support
- **Results Display**: Shows Answer, Why (explanations), and Sources with expand/collapse functionality
- **TypeScript**: Strict typing throughout the application
- **Responsive Design**: Works on desktop and mobile devices

## Components

- `QuestionInput`: Form component for submitting questions
- `ResultsPanel`: Displays AI responses with proper formatting and accessibility
- Main page: Integrates all components with loading states and error handling

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   npm start
   ```

## API Integration

The frontend is designed to integrate with the FastAPI `/ask` endpoint. Currently uses mock data for demonstration.

Expected API response format:
```typescript
interface QueryResult {
  answer: string;
  explanation_bullets: string[];
  sources: string[];
}
```

## Accessibility Features

- Semantic HTML with proper headings and landmarks
- ARIA labels and roles for screen readers
- Keyboard navigation support
- Focus management during loading states
- Color-blind friendly design (no color-only indicators)
- Text truncation with "Show more/less" controls
