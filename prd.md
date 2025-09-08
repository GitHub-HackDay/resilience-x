# PRD: Resilience-X

## Overview
Resilience-X is a lightweight demo app that helps answer *“where are the bottlenecks and why?”* in post-disaster recovery scenarios.  
It combines semantic search, graph reasoning, and natural language Q&A into a single experience that can be demoed in under 2 minutes.

The project is built as part of the GitHub + Microsoft Research Builders Hack Day, showcasing how AI-native tools (Copilot, GraphRAG, NLWeb, Weaviate) accelerate startup-style product building.

---

## Goals
- Build a **demoable end-to-end app in 1 day**.
- Show how AI can turn small sets of messy crisis documents into **actionable, explainable answers**.
- Use all 4 required technologies: GitHub Copilot, GraphRAG, NLWeb, Weaviate.
- Keep the scope narrow: **one clean use case** + **one slick demo flow**.

---

## User Story
- **As an emergency operations planner**,  
  I want to ask plain-English questions like *“Which roads are still blocked near Redmond, and why is cleanup delayed?”*  
  So that I can get an answer plus a simple explanation and sources, without sifting through multiple reports.

---

## Demo Script (90 sec)
1. Show the NLWeb interface with one input box.  
2. Ask: “Which neighborhoods are facing cleanup delays?”  
3. App queries Weaviate (semantic match) + GraphRAG (multi-hop explanation).  
4. Output includes:  
   - **Answer:** “Cleanup is delayed in King County.”  
   - **Why:** “Crew shortages (Report A), debris overflow (Report B).”  
   - **Sources:** clickable links to the docs.  
5. End with: “Built in one day with Copilot, GraphRAG, NLWeb, and Weaviate.”

---

## Core Features (MVP)
- **Natural Language Query Interface** (NLWeb frontend).  
- **Semantic Search** (Weaviate vector DB for embeddings).  
- **Multi-hop Reasoning + Explanation** (GraphRAG project).  
- **Single Endpoint API** (`/ask`) with FastAPI.  
- **Copilot-assisted scaffolding + docs** (tracked in repo).  

---

## Nice-to-Have (Stretch if time permits)
- Multiple canned demo questions with polished outputs.  
- Simple visualization of graph hops (2–3 nodes shown in UI).  
- Dark mode + minimal design polish.  
- Scripted Docker setup (`demo.sh`) for one-click run.

---

## Out of Scope
- Large datasets (keep under ~20 short docs).  
- Full production-grade infra (auth, monitoring, scaling).  
- Complex UI/UX (stick to one page, one flow).  
- Non-demo use cases (focus purely on post-disaster recovery Q&A).

---

## Repo Structure
