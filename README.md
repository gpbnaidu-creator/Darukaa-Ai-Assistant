Darukaa Ai Assistant

An AI-powered biodiversity intelligence chatbot that analyzes environmental conditions and provides science-based biodiversity recommendations.

 ## Overview

Darukaa Ai Assistant combines **RAG (Retrieval-Augmented Generation)**, **FAISS vector search**, and **Google Gemini** to analyze environmental information such as soil, rainfall, temperature, land use, pollution, and deforestation.

The system provides:
- Environmental analysis
- Biodiversity recommendations
- Scientific reasoning
- Impacted environmental metrics
- Evidence source
- Confidence level
- Conversational follow-up support

##  Architecture

```text
User
 ↓
Streamlit UI
 ↓
Environmental Profile + User Question
 ↓
Query Construction
 ↓
Gemini Embedding
 ↓
FAISS Vector Search
 ↓
Scientific Knowledge Chunks
 ↓
Gemini
 ↓
Recommendation + Reasoning + Evidence

