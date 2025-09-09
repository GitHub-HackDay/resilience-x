/**
 * Type definitions for polished explanation bullets and source tracing
 */

export interface ExplanationBullet {
  step: number;
  reasoning: string;
  source_references: number[];
  confidence?: number;
}

export interface Source {
  id: number;
  title: string;
  content: string;
  metadata: Record<string, any>;
  url?: string;
}

export interface AskResponse {
  answer: string;
  explanation_bullets: ExplanationBullet[];
  sources: Source[];
}

export interface AskRequest {
  question: string;
}