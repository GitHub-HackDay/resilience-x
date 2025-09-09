from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Resilience-X API")

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    explanation_bullets: List[str]
    sources: List[str]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/ask")
async def ask_question(question: Question):
    return Answer(
        answer="Cleanup is delayed in King County due to crew shortages and equipment delays.",
        explanation_bullets=[
            "Debris removal crews are short-staffed due to illness (Crisis Report #001)",
            "Heavy equipment delayed due to supply chain issues (Crisis Report #001)"
        ],
        sources=["crisis_report_001.txt", "crisis_report_002.txt"]
    )
