# LinkedIn Post Generator 🚀

A production-grade, full-stack application built to generate engaging LinkedIn posts and messages, perform real-time AI quality analysis, track analytics, and export content—powered by **FastAPI**, **PostgreSQL/SQLAlchemy**, **Pluggable LLM Engine (Groq / OpenAI / Anthropic)**, and modern security practices.

---

## 🎯 Architectural Overview

```
+---------------------------------------------------------------------------------------+
|                                  CLIENT BROWSER                                       |
|  - HTML5 / CSS3 / ES6 JavaScript & Chart.js                                           |
|  - Auth UI Modal (Login / Register / Profile Badge)                                   |
|  - httpOnly Cookie Token Auth Handling (XSS Vulnerability Safeguard)                  |
+------------------------------------------+--------------------------------------------+
                                           |
                              REST API / JSON / Cookies
                                           v
+---------------------------------------------------------------------------------------+
|                               FASTAPI BACKEND (Python 3.11+)                           |
|  - Procfile / Gunicorn: gunicorn backend.app.main:app -k uvicorn.workers.UvicornWorker|
|  - Routers: /api/v1/auth, /api/v1/posts, /api/v1/analyzer, /api/v1/export             |
|  - Security: IDOR Ownership Checks, httpOnly JWT Cookies, Slowapi Rate Limiting       |
|  - Services: Multi-Provider LLM Engine, Dynamic Quality Scoring, ReportLab PDF         |
+-------------------+------------------------------------+------------------------------+
                    |                                    |
                    v                                    v
   +---------------------------------+  +----------------------------------+
   |  PostgreSQL / SQLite Database   |  |      Pluggable LLM Providers     |
   | - SQLAlchemy ORM Models         |  | - Groq (Llama 3.3 70B / 3.1 8B) |
   | - User-Scoped Data Protection   |  | - OpenAI (GPT-3.5-Turbo / GPT-4o)|
   | - Idempotent Data Migration     |  | - Anthropic (Claude 3.5 Sonnet)  |
   |                                 |  | - Token Budget Enforcer          |
   +---------------------------------+  +----------------------------------+
```

---

## ✨ Features & Highlights

- 🤖 **Multi-Provider LLM Engine**: Native support for **Groq**, **OpenAI**, and **Anthropic** with automatic fallback to mock engine for offline development. Enforces `max_tokens` (1000 limit) and input length validation to control billing.
- 🔐 **JWT Auth & Ownership Protection**: User registration and login powered by bcrypt password hashing and **`httpOnly` JWT cookies**. Enforces user ownership checks to eliminate IDOR and global wiping vulnerabilities.
- 🔍 **AI-Assisted Quality Analyzer**: Analyzes length, line spacing, questions, emojis, and hashtags, providing dynamic AI-rewritten post versions.
- 🗄️ **Relational Database Storage**: Migrated from legacy `post_history.json` to SQLAlchemy ORM (PostgreSQL/SQLite) with idempotent deduplicated data migration.
- 💻 **Frontend Auth Integration**: Interactive Login/Register modal, automatic user session detection, and dynamic API base URL routing.
- 📊 **Analytics Dashboard**: Interactive Chart.js visualizers for post counts, popular topics, and timeline trends.
- 📄 **Export Utilities**: High-quality PDF export (ReportLab) and direct LinkedIn sharing links.
- 🐳 **Docker Parity**: Multi-stage `Dockerfile` and `docker-compose.yml` for unified local dev and production deployment.
- 🧪 **Automated Testing & CI**: Pytest suite covering endpoints, auth, IDOR checks, and logic, integrated into GitHub Actions CI (`.github/workflows/ci.yml`).
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
   *Edit `.env` to supply your `GROQ_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY` (or set `LLM_PROVIDER=mock` for offline testing).*

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
| GET | `/api/v1/auth/me` | Retrieve authenticated user profile |
| POST | `/api/v1/generate-post` | Generate LinkedIn post with LLM |
| POST | `/api/v1/generate-message` | Generate professional message |
| POST | `/api/v1/analyze-text` | Analyze post quality & score with AI rewrite |
| GET | `/api/v1/get-history` | Retrieve user post history |
| DELETE | `/api/v1/delete-history` | Delete history for authenticated user |
| POST | `/api/v1/export-pdf` | Download post as PDF document |

Full interactive API documentation is available at `/docs`.

---

## 📄 License

This project is open source and available under the **MIT License**.
