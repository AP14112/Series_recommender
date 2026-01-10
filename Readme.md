# Explainable Series Recommender System

This is an end-to-end hybrid recommendation engine that suggests TV series by combining semantic content similarity with user interaction behavior. It features an Explainable AI (XAI) layer that uses a Large Language Model to provide human-readable justifications for every suggestion.

## Key Features

- Hybrid Recommendation Logic: Blends content-based filtering (semantic embeddings) with behavioral weighting (user interactions).
- Explainable AI (XAI): Converts internal algorithmic signals into natural language explanations using an LLM.
- Architectural Efficiency: Strictly separates heavy offline preprocessing from lightweight online inference.
- High-Performance Search: Utilizes FAISS for fast similarity retrieval within the vector space.
- Interactive UI: A clean, modular Streamlit dashboard for real-time interaction.

---

## System Architecture

The project is designed to transition smoothly from raw data to explained recommendations:

1. Ingestion: Raw metadata and interactions are cleaned and sanitized.
2. Indexing: Metadata is converted into embeddings and stored in a FAISS vector index.
3. Hybrid Scoring: The system ranks items by combining vector similarity with user affinity.
4. Explanation Layer: Ranking signals are processed by an LLM (Groq) to generate a narrative explanation.
5. Output: Results are served through a Streamlit frontend.

```
Raw Data
   ↓
Offline Preprocessing (data_loader.py)
   ↓
Processed CSVs + FAISS Vector Store (build_pipeline.py)
   ↓
Hybrid Recommender (hybrid_model.py)
   ↓
LLM Explainer (recommender.py)
   ↓
Streamlit UI (app.py)
```

---

## Project Structure

```
SERIES_RECOMMENDER/
├── src/
│   ├── data_loader.py
│   ├── vector_score.py
│   ├── hybrid_model.py
│   └── recommender.py
├── pipeline/
│   ├── build_pipeline.py
│   └── pipeline.py
├── app/
│   └── app.py
├── data/
├── faiss_db/
└── utils/
```

---

## Offline vs Online Pipeline

### Offline (Run Once)

```bash
python pipeline/build_pipeline.py
```

Generates:
- processed_user_interactions.csv
- processed_series_metadata.csv
- FAISS index (faiss_db/)

### Online (Run Anytime)

```bash
streamlit run app/app.py
```

The application only reads pre-built artifacts and performs no heavy computation at runtime.

---

## Recommendation Logic (Simplified)

1. Identify strongest user interaction
2. Retrieve similar series using FAISS
3. Combine content similarity and interaction strength
4. Rank results using weighted scoring
5. Generate explanations using an LLM

---

## Explainable AI (XAI)

Each recommendation is accompanied by a natural-language explanation derived from:
- Content similarity scores
- User interaction signals
- Seed series influence

---

## Tech Stack

- Python
- Pandas, NumPy
- FAISS
- Sentence Transformers
- Streamlit
- Groq LLM

---

## Deployment (Docker + Kubernetes)

The application is containerized and deployed using Docker and Google Kubernetes Engine (GKE Autopilot).

### Docker

```bash
docker build -t series-recommender .
```

### Container Registry (GCP Artifact Registry)

```bash
docker tag series-recommender:latest us-central1-docker.pkg.dev/<PROJECT_ID>/series-repo/series-recommender:latest
docker push us-central1-docker.pkg.dev/<PROJECT_ID>/series-repo/series-recommender:latest
```

### Kubernetes (GKE Autopilot)

- Images pulled from Artifact Registry
- Secrets injected via Kubernetes Secrets
- Service exposed using a LoadBalancer

```bash
kubectl apply -f series-k8s.yaml
kubectl get svc
```

Access the app at:

```
http://<EXTERNAL-IP>:8501
```

---

## Notes

- Heavy preprocessing is done at image build time
- Runtime inference remains lightweight
- Environment variables are injected via Kubernetes Secrets in production
