# Flask Blogging Platform — 8-Week Internship Project

A full-stack, production-ready blogging platform built with **Python 3**, **Flask**, **SQLite**, and modern web standards. Designed and engineered over an 8-week structured development cycle as a portfolio demonstration project.

---

## 🌟 Key Features

1. **User Authentication & Security (Week 2)**
   * User registration with unique username and email constraints.
   * Secure password hashing with Werkzeug (`scrypt`).
   * Session management via Flask-Login (`current_user`, `@login_required`).
   * CSRF protection on all forms via Flask-WTF.

2. **Blog Post CRUD (Week 3)**
   * Create, Read, Update, and Delete articles.
   * Categorization (*Technology, Programming, Lifestyle, Education, Career, General*).
   * Comma-separated tag support.
   * Author permission enforcement (only authors can edit/delete their own posts).

3. **Modern Responsive UI (Week 4)**
   * Clean typography with Plus Jakarta Sans and modern card shadows.
   * Mobile-responsive collapsible navigation menu with vanilla JavaScript.
   * Dynamic reading time estimation (`{{ post.content | reading_time }}`).
   * Scroll-linked reading progress bar.
   * Auto-dismissing flash notifications.

4. **Community Discussion & Commenting (Week 5)**
   * Real-time discussion thread beneath every article.
   * Author and post-owner comment moderation.
   * Live comment count badges across the application.

5. **Search Engine & Tag Filtering (Week 6)**
   * Full-text search across article titles, body content, and tags using SQLAlchemy `or_`.
   * Interactive `#tag` filtering and category chip selector.
   * Active filter badges bar with one-click filter removal.

6. **Quality Assurance & Production Readiness (Week 7)**
   * Automated unit and integration test suite (`tests/test_blog.py`).
   * Branded custom error pages (`403 Forbidden`, `404 Not Found`, `500 Server Error`).
   * Environment variable configuration (`python-dotenv`, `.env.example`).
   * WSGI deployment ready with `gunicorn` and `Procfile`.

---

## 🛠️ Technology Stack

* **Backend:** Python 3, Flask
* **Database ORM:** SQLite, Flask-SQLAlchemy
* **Authentication:** Flask-Login, Werkzeug Security
* **Form Handling:** Flask-WTF, WTForms, Email-Validator
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Jinja2
* **Testing:** Python `unittest`
* **Production Server:** Gunicorn, Python-Dotenv

---

## 🚀 Quick Start Guide

### 1. Clone or Open the Repository
```bash
git clone https://github.com/YOUR_USERNAME/blogging-platform-flask.git
cd blogging-platform-flask
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Development Server
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Running Automated Tests

To execute the automated unit and integration tests:
```bash
python -m unittest discover tests
```

---

## 📁 Project Architecture

```text
blogging platform/
│
├── instance/
│   └── site.db               # SQLite database file
├── static/
│   ├── css/
│   │   └── style.css         # Modern responsive stylesheet
│   └── js/
│       └── main.js           # JavaScript interactions & navigation
├── templates/
│   ├── base.html             # Master layout template
│   ├── index.html            # Homepage with hero, search & feed
│   ├── about.html            # Project roadmap & tech stack
│   ├── create_post.html      # Create & edit post editor
│   ├── post_detail.html      # Article view & comment thread
│   ├── dashboard.html        # User profile & post management table
│   ├── register.html         # User registration form
│   ├── login.html            # User login form
│   └── errors/
│       ├── 403.html          # Forbidden error
│       ├── 404.html          # Not found error
│       └── 500.html          # Server error
├── tests/
│   ├── __init__.py
│   └── test_blog.py          # Automated test suite
├── .env.example              # Environment variables template
├── .gitignore                # Git exclusions (venv, db, caches)
├── app.py                    # Main Flask application & routes
├── forms.py                  # WTForms form definitions
├── models.py                 # SQLAlchemy database models
├── Procfile                  # Production cloud deployment runner
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```
