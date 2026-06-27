# RecruitIQ 🧠 — INDIA RUNS 2026 (Track 1)
**Beyond Keywords. Intelligent Hiring.**

RecruitIQ is a production-ready, local-first AI recruitment platform designed to solve the problem of keyword-based resume screening. Instead of relying on exact word matches, RecruitIQ maps Job Descriptions and Candidate Profiles into a high-dimensional vector space to evaluate **semantic meaning and contextual fit**.

## 🚀 The AI Pipeline (100% Offline & Open Source)
To guarantee data privacy and zero API costs, RecruitIQ runs entirely locally.

1. **Embedding Generation:** Uses `BAAI/bge-small-en-v1.5` via `sentence-transformers` to generate dense vector representations of both jobs and candidates.
2. **Vector Indexing:** Utilizes `FAISS` (Facebook AI Similarity Search) for instantaneous memory-based Cosine Similarity retrieval.
3. **Cross-Encoder Reranking:** The top candidates are passed through `ms-marco-MiniLM-L-6-v2` to evaluate the highly specific contextual relationship between the candidate's exact phrasing and the job's requirements.
4. **Explainable AI (XAI):** A custom natural language generation engine parses vector overlap to output human-readable reasoning (Matched Skills, Missing Skills, Transferable Skills).

## 💻 Tech Stack
* **Frontend:** Next.js 15 (App Router), React Query, Tailwind CSS, Framer Motion, shadcn/ui.
* **Backend:** FastAPI (Python), SQLAlchemy, aiosqlite, JWT Authentication.
* **Database:** SQLite (Easily portable for hackathon evaluation; PostgreSQL ready).
* **AI/ML:** PyTorch, SentenceTransformers, FAISS, Pandas.

## 🛠️ Installation & Setup (Local Environment)

### 1. Backend Setup
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
\`\`\`
*(Note: On the first run, the AI models (~200MB) will download to your local huggingface cache. Subsequent runs are 100% offline).*

### 2. Frontend Setup
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
The application will be running at `http://localhost:3000`.

## 📖 How to Test
1. Register/Login on the dashboard.
2. Navigate to **Data Ingestion**.
3. Create a **Job Blueprint** (e.g., "Senior Python Backend Developer").
4. Upload a dataset of candidates via the **CSV Uploader**.
5. Click **Run Semantic Search** and view the locally generated XAI match reports.

## 👥 Team
* Shivani Rao
* Sanika Jadhav
* Vishal Patil
* Bhakti Desale
