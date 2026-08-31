# LinkedIn Post Generator 🚀

A production-grade, full-stack application built to generate engaging LinkedIn posts and messages, extract factual context from uploaded certificates & documents (PDF), perform real-time AI quality analysis, track analytics, and export content—powered by **FastAPI**, **PostgreSQL/SQLAlchemy**, **Pluggable LLM Engine (Groq / OpenAI / Anthropic)**, and modern security practices.

## 🌐 Live Demo

- **Frontend**: [https://tubular-bonbon-644eda.netlify.app](https://tubular-bonbon-644eda.netlify.app)
- **Backend API**: [https://linkedin-post-generator-pd4j.onrender.com](https://linkedin-post-generator-pd4j.onrender.com) (Swagger docs at [`/docs`](https://linkedin-post-generator-pd4j.onrender.com/docs))

---

## 🎯 Architectural Overview

```
+---------------------------------------------------------------------------------------+
|                                  CLIENT BROWSER                                       |
|  - HTML5 / CSS3 / ES6 JavaScript & Chart.js                                           |
|  - Document Upload Dropzone & Extracted Context Editor (PDF)                          |
|  - Auth UI Modal (Login / Register / Profile Badge)                                   |
|  - httpOnly Cookie Token Auth Handling (XSS Vulnerability Safeguard)                  |
|  - Multi-Format Export: PDF (ReportLab) & PNG Image (html2canvas)                     |
+------------------------------------------+--------------------------------------------+
                                           |
                              REST API / JSON / Cookies
                                           v
+---------------------------------------------------------------------------------------+
|                               FASTAPI BACKEND (Python 3.11+)                           |
|  - Procfile / Gunicorn: gunicorn backend.app.main:app -k uvicorn.workers.UvicornWorker|
|  - Routers: /api/v1/auth, /api/v1/posts, /api/v1/analyzer, /api/v1/export,            |
|             /api/v1/upload-document                                                   |
|  - Security: IDOR Ownership Checks, httpOnly JWT Cookies, Slowapi Rate Limiting       |
|  - Services: Multi-Provider LLM Engine, Document Parsing (pypdf), ReportLab PDF       |
+-------------------+------------------------------------+------------------------------+
                    |                                    |
                    v                                    v
   +---------------------------------+  +----------------------------------+
   |  PostgreSQL / SQLite Database   |  |      Pluggable LLM Providers     |
   | - SQLAlchemy ORM Models         |  | - Groq (Llama 3.3 70B / GPT OSS) |
   | - User-Scoped Data Protection   |  | - OpenAI (GPT-3.5-Turbo / GPT-4o)|
   | - Document Context Persistence  |  | - Anthropic (Claude 3.5 Sonnet)  |
   | - Idempotent Data Migration     |  | - Token Budget & Injection Shield|
   +---------------------------------+  +----------------------------------+
```

---

## ✨ Features & Highlights

- 📄 **Document Upload & Grounded Generation**: Upload PDF certificates or reports to automatically extract verified achievements, dates, and credentials, grounding generated LinkedIn posts in real facts with prompt-injection defenses.
- 🤖 **Multi-Provider LLM Engine**: Native support for **Groq**, **OpenAI**, and **Anthropic** with automatic fallback to mock engine for offline development. Enforces `max_tokens` (1000 limit) and input length validation to control billing.
- 🔐 **JWT Auth & Ownership Protection**: User registration and login powered by bcrypt password hashing and **`httpOnly` JWT cookies**. Enforces user ownership checks to eliminate IDOR and global wiping vulnerabilities.
- ⏱️ **Active Rate Limiting**: Slowapi middleware enforces 10 req/min limits on LLM and parsing routes while keeping uptime monitoring (`/health`) unthrottled.
- 🔍 **AI-Assisted Quality Analyzer**: Analyzes length, line spacing, questions, emojis, and hashtags, providing dynamic AI-rewritten post versions that preserve the user's original message.
- 🗄️ **Relational Database Storage**: Migrated from legacy `post_history.json` to SQLAlchemy ORM (PostgreSQL/SQLite) with idempotent deduplicated data migration.
- 💻 **Frontend Auth Integration**: Interactive Login/Register modal, automatic user session detection, and dynamic API base URL routing.
- 📊 **Analytics Dashboard**: Interactive Chart.js visualizers for post counts, popular topics, and timeline trends.
- 📄 **Multi-Format Export Utilities**: High-quality PDF export (ReportLab with XML entity sanitization), PNG image export (`html2canvas`), and direct LinkedIn sharing links.
- 🐳 **Multi-Stage Docker Parity**: True multi-stage `Dockerfile` (stripping `build-essential` from runtime) and `docker-compose.yml` for unified local dev and production deployment.
- 🧪 **Automated Testing & CI**: Pytest suite covering endpoints, auth, document extraction, rate limiting, and IDOR checks.
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
   pip install -r backend/requirements.txt
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
pytest tests/ -v
```

---

## 📡 Key API Endpoints

| Method | Endpoint | Rate Limit | Description |
|--------|----------|------------|-------------|
| GET | `/api/health` | Exempt | Service health diagnostic status |
| POST | `/api/v1/auth/register` | Default | Register new user account |
| POST | `/api/v1/auth/login` | Default | Login user & set httpOnly access token cookie |
| POST | `/api/v1/auth/logout` | Default | Logout user & clear cookie |
| GET | `/api/v1/auth/me` | Default | Retrieve authenticated user profile |
| POST | `/api/v1/upload-document` | 10/min | Parse PDF and extract grounding achievement context |
| POST | `/api/v1/generate-post` | 10/min | Generate LinkedIn post with LLM (optional document context) |
| POST | `/api/v1/generate-message` | 10/min | Generate professional networking message |
| POST | `/api/v1/analyze-text` | 10/min | Analyze post quality & score with AI rewrite |
| GET | `/api/v1/get-history` | Default | Retrieve user post history |
| GET | `/api/v1/get-post/{post_id}` | Default | Retrieve post details (with ownership check) |
| DELETE | `/api/v1/delete-history` | Default | Delete history for authenticated user |
| POST | `/api/v1/export-pdf` | 10/min | Download post as PDF document (with XML sanitization) |

Full interactive API documentation is available at `/docs`.

---

## 📄 License

This project is open source and available under the **MIT License**.

