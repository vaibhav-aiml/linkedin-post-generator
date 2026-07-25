# LinkedIn Post Generator 🚀

A production-grade, full-stack application built to generate engaging LinkedIn posts and messages, perform real-time post quality analysis, track analytics, and export content—powered by **FastAPI**, **PostgreSQL/SQLAlchemy**, **Pluggable LLM Engine (Groq / OpenAI)**, and modern security practices.

---

## 🎯 Architectural Overview

```
+---------------------------------------------------------------------------------------+
|                                  CLIENT BROWSER                                       |
|  - HTML5 / CSS3 / ES6 JavaScript & Chart.js                                           |
|  - Generator UI, Quality Metrics Engine, Analytics Visualizations                    |
|  - httpOnly Cookie Token Auth Handling (XSS Vulnerability Safeguard)                  |
+------------------------------------------+--------------------------------------------+
                                           |
                              REST API / JSON / Cookies
                                           v
+---------------------------------------------------------------------------------------+
|                               FASTAPI BACKEND (Python 3.11+)                           |
|  - Routers: /api/v1/auth, /api/v1/posts, /api/v1/analyzer, /api/v1/export             |
|  - Security: httpOnly JWT Cookies, CORS Restriction, Slowapi Rate Limiting             |
|  - Services: LLM Engine (Groq / OpenAI / Mock), Quality Scoring, ReportLab PDF         |
|  - Background Tasks: Native FastAPI BackgroundTasks for exports                       |
+-------------------+------------------------------------+------------------------------+
                    |                                    |
                    v                                    v
   +---------------------------------+  +----------------------------------+
   |  PostgreSQL / SQLite Database   |  |      Pluggable LLM Providers     |
   | - SQLAlchemy ORM Models         |  | - Groq Llama 3.3 70B / 3.1 8B    |
   | - Idempotent JSON Data Migration|  | - Token Budget Enforcer          |
   +---------------------------------+  +----------------------------------+
```

---

## ✨ Features & Highlights

- 🤖 **LLM Post Generator**: Real-time generation powered by LLMs (Groq Llama 3.3 70B & 3.1 8B) with customizable tone, length, and auto-hashtags. Includes token cost control enforcement.
- 💬 **Professional Message Generator**: Write tailored networking, collaboration, and follow-up messages.
- 🔍 **Post Quality Analyzer**: Comprehensive scoring (0-100), word count assessment, hashtag optimization, line break checks, and AI improvement suggestions.
- 🗄️ **Relational Database Storage**: Migrated from legacy `post_history.json` to SQLAlchemy ORM (PostgreSQL/SQLite) with idempotent data migration.
- 🔒 **Security & Authentication**: User registration and login powered by bcrypt password hashing and **`httpOnly` JWT cookies** (protecting against XSS token theft).
- 📊 **Analytics Dashboard**: Interactive Chart.js visualizers for post counts, popular topics, and timeline trends.
- 📄 **Export Utilities**: High-quality PDF export (ReportLab) and direct LinkedIn sharing links.
- 🐳 **Docker Parity**: Multi-stage `Dockerfile` and `docker-compose.yml` for unified local dev and production deployment.
- 🧪 **Automated Testing & CI**: Pytest suite covering endpoints, auth, and logic, integrated into GitHub Actions CI (`.github/workflows/ci.yml`).
- 📖 **OpenAPI Documentation**: Automatic Swagger UI documentation available at `/docs`.

---

## 💻 Quick Start & Installation

### Option A: Local Python Environment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vaibhav-aiml/linkedin-post-generator.git
   cd linkedin-post-generator
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to supply your `GROQ_API_KEY` (or use `LLM_PROVIDER=mock` for offline testing).*

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Idempotent Data Migration**:
   ```bash
   python scripts/migrate_json_to_db.py
   ```

5. **Start FastAPI Backend**:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

6. **Open the Frontend**:
   Open `frontend/index.html` in your browser or run Live Server.

---

### Option B: Docker Compose (Production Parity)

```bash
cp .env.example .env
docker-compose up --build
```

The application will be live with PostgreSQL database at `http://localhost:8000`.

---

## 🧪 Running Automated Tests

Run the full Pytest test suite:

```bash
python -m pytest -v
```

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Service health diagnostic status |
| POST | `/api/v1/auth/register` | Register new user account |
| POST | `/api/v1/auth/login` | Login user & set httpOnly access token cookie |
| POST | `/api/v1/auth/logout` | Logout user & clear cookie |
| POST | `/api/v1/generate-post` | Generate LinkedIn post with LLM |
| POST | `/api/v1/generate-message` | Generate professional message |
| POST | `/api/v1/analyze-text` | Analyze post quality & score |
| GET | `/api/v1/get-history` | Retrieve user post history |
| POST | `/api/v1/export-pdf` | Download post as PDF document |

Full interactive API documentation is available at `/docs`.

---

## 📄 License

This project is open source and available under the **MIT License**.
