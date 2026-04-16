
# LinkedIn Post Generator 🚀

A full-stack web application that helps professionals create engaging LinkedIn posts, generate professional messages, analyze content quality, and track analytics - all in one place.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Future Improvements](#future-improvements)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## 🎯 Overview

The **LinkedIn Post Generator** is designed to solve writer's block for professionals who want to maintain an active LinkedIn presence. It provides AI-powered templates, real-time post analysis, and comprehensive analytics to help users create high-quality content that drives engagement.

**Live Demo:** *(Add your Render deployment link here)*

**GitHub Repository:** https://github.com/vaibhav-aiml/linkedin-post-generator

## ✨ Features

### 📝 Post Generation
- **7 Professional Templates:** Professional Insight, Networking, Achievement, Technology, Marketing, Leadership, Career Advice
- **Character Counter** with visual progress bar (max 100 characters)
- **Key Points Integration** - Add custom bullet points to your posts
- **Auto-generated Hashtags** based on your topic

### 💬 Message Generator
- Personalized professional messages for networking
- Collaboration requests
- Job inquiry templates

### 🔍 Post Analyzer
- **Quality Score** (0-100) based on multiple factors
- Word count, sentence count, and hashtag analysis
- **Actionable suggestions** for improvement
- Engagement potential evaluation

### 📚 Post History
- Auto-saves every generated post
- View, load, and reuse previous posts
- Clear history option
- Persistent storage using JSON file

### 📊 Analytics Dashboard
- **Total posts counter**
- **Most used topic** tracking
- **Popular post type** analysis
- **Average post length** calculation
- **Pie Chart** - Posts by type visualization
- **Line Chart** - Posting timeline

### ⭐ Favorite Templates
- Save unlimited favorite templates
- Quick load saved templates
- Persistent storage using LocalStorage
- Maximum 10 favorites (auto-managed)

### 🎨 User Experience
- **Dark Mode Toggle** with persistent preference
- **Responsive Design** - Works on desktop and mobile
- **Loading Animations** for better UX
- **Toast Notifications** for user actions

### 📄 Export & Share
- **Export as PDF** - Download posts as professional PDF documents
- **Export as Image** - Save posts as PNG images
- **Share to LinkedIn** - Direct sharing to your LinkedIn feed
- **Copy to Clipboard** - One-click copy functionality

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **Flask** | Web framework for REST API |
| **Flask-CORS** | Cross-origin resource sharing |
| **ReportLab** | PDF generation |
| **JSON** | File-based storage for post history |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure and layout |
| **CSS3** | Styling and animations |
| **JavaScript (ES6+)** | Core functionality |
| **Chart.js** | Analytics visualizations |
| **html2canvas** | Image export functionality |
| **Font Awesome** | Icons and visual elements |

### Development Tools
- **Git** - Version control
- **GitHub** - Code hosting
- **VS Code** - Development environment

## 📁 Project Structure

```
linkedin-post-generator/
│
├── backend/
│   ├── app.py                 # Flask application with all API endpoints
│   ├── requirements.txt       # Python dependencies
│   ├── post_history.json      # Auto-generated post storage
│   └── Procfile               # Deployment configuration for Render
│
├── frontend/
│   ├── index.html             # Main application UI
│   ├── style.css              # Styling with dark mode support
│   └── script.js              # Frontend logic and API integration
│
├── start.bat                  # One-click launcher for Windows
└── README.md                  # Project documentation
```

## 💻 Installation

### Prerequisites
- Python 3.9 or higher installed
- Git (optional, for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/vaibhav-aiml/linkedin-post-generator.git
cd linkedin-post-generator
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run the Backend Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Step 4: Open the Frontend

- **Option A:** Double-click `frontend/index.html`
- **Option B:** Use Live Server in VS Code
- **Option C:** Run `cd frontend && start index.html`

### Quick Start (Windows)
Double-click `start.bat` in the main folder - it will automatically start both backend and frontend!

## 🚀 Usage

### Generating a Post
1. Enter a topic (e.g., "Artificial Intelligence in Healthcare")
2. Select a post type from 7 available templates
3. Click "Generate Post"
4. Copy, save, or share the generated content

### Saving Favorite Templates
1. Generate a post with your desired topic and type
2. Click "Save as Favorite"
3. Access saved templates from the Favorites section

### Analyzing a Post
1. Paste any LinkedIn post in the analyzer section
2. Click "Analyze Post"
3. Review the quality score and improvement suggestions

### Viewing Analytics
- Check **Post History** for all generated content
- View **Analytics Dashboard** for charts and statistics
- Track your posting patterns over time

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check backend status |
| POST | `/api/generate-post` | Generate a LinkedIn post |
| POST | `/api/generate-message` | Generate a professional message |
| POST | `/api/analyze-text` | Analyze post quality |
| GET | `/api/get-history` | Retrieve all saved posts |
| GET | `/api/get-post/<id>` | Retrieve a specific post |
| DELETE | `/api/delete-history` | Clear all post history |
| POST | `/api/share-to-linkedin` | Generate LinkedIn share URL |
| POST | `/api/export-pdf` | Export post as PDF |

## 🔧 Future Improvements

- [ ] **User Authentication** - Login system with personalized history
- [ ] **Database Integration** - Migrate from JSON to PostgreSQL
- [ ] **AI-Powered Suggestions** - GPT integration for smarter content
- [ ] **Social Media Analytics** - Track actual post performance
- [ ] **Browser Extension** - Use directly on LinkedIn website
- [ ] **Mobile App** - React Native version
- [ ] **Schedule Posts** - Plan and schedule future posts
- [ ] **Multiple Language Support** - Generate posts in different languages

## 🙏 Acknowledgments

- **Xebia** - For their invaluable guidance, mentorship, and providing this amazing learning opportunity
- **HOD & Dean** - For their constant support and encouragement
- **Project Guide** - For technical guidance and feedback
- **All Teachers** - For sharing their knowledge and expertise

## 📞 Contact

- **GitHub:** [vaibhav-aiml](https://github.com/vaibhav-aiml)
- **Project Repository:** [linkedin-post-generator](https://github.com/vaibhav-aiml/linkedin-post-generator)

## 📄 License

This project is open source and available under the **MIT License**.

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---


