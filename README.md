# Job Application AI Agent 🚀

An AI-powered job application automation tool that scrapes job listings, extracts skills and requirements using **NVIDIA NIM LLMs** (or local NLP), and automatically tailors your CV template (`.docx`) to match job descriptions.

---

## 🌟 Key Features

- **🔍 LinkedIn Job Scraper**: Automatically search for job postings by keyword and location, extracting job details and full descriptions.
- **🧠 NVIDIA NIM AI Skill Extractor**: Powered by **`nvidia/llama-3.1-nemotron-70b-instruct`** to extract technical skills, soft skills, and core requirements from job postings.
- **🔄 Local NLP Fallback**: Includes spaCy and regex-based NLP matching if no AI API key is configured.
- **📄 Automatic CV Tailoring**: Modifies your `.docx` CV template to highlight the specific skills and qualifications required for each job post.
- **🌐 Modern Web Interface**: Clean Flask-based UI for effortless file uploading, job searching, skill matching, and tailored CV generation.
- **📊 Batch Export**: Automatically exports job listings to Excel and supports bulk CV generation for multiple roles.

---

## 🏗️ Architecture & Workflow

```
 ┌──────────────────────┐      ┌──────────────────────┐
 │  LinkedIn Job Search │ ---> │ Job Description Text │
 └──────────────────────┘      └──────────┬───────────┘
                                          │
                                          ▼
┌──────────────────────┐       ┌──────────────────────┐
│  CV Template (.docx) │  ---> │  AI Skill Extraction │ (NVIDIA NIM / spaCy)
└──────────────────────┘       └──────────┬───────────┘
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │ Tailored CV (.docx)  │
                               └──────────────────────┘
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+**
- **Google Chrome** (for Selenium job scraping)

---

### 1. Installation

#### **Automated Setup (Recommended)**
Run the setup script to create a virtual environment, install python dependencies, download spaCy models, and set up the package:

```bash
bash install.sh
```

#### **Manual Setup**
```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Download spaCy English model
python -m spacy download en_core_web_sm

# 4. Install package in editable mode
pip install -e .
```

---

### 2. Configure NVIDIA AI Models (Optional but Recommended)

Get a free NVIDIA API key from [build.nvidia.com](https://build.nvidia.com) to enable high-accuracy LLM skill extraction:

```bash
export NVIDIA_API_KEY="nvapi-your-actual-api-key"
```

> **Note**: If `NVIDIA_API_KEY` is not provided, the application will automatically fall back to rule-based spaCy NLP processing.

---

### 3. Running the Application

#### **Option A: Web Interface (Flask App)**

Activate your environment and run:

```bash
python -m ui.app
```
or via the CLI entrypoint:
```bash
job-apply-ai web
```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

#### **Option B: Batch Command Line Mode**

To process job listings from an Excel file directly:

```bash
python -m cv_modifier.cv_analyzer
```

---

## 📂 Project Structure

```
job_apply_ai/
├── install.sh                # Automated setup bash script
├── requirements.txt          # Python package requirements
├── setup.py                  # Setuptools package configuration
├── cv_modifier/
│   ├── __init__.py
│   └── cv_analyzer.py        # Skill extraction & DOCX CV modifier
├── scraper/
│   ├── __init__.py
│   └── linkedin.py           # Selenium-based LinkedIn job scraper
├── ui/
│   ├── __init__.py
│   ├── app.py                # Flask Web UI server
│   └── templates/            # HTML Jinja templates (index, job list, etc.)
└── utils/
    ├── __init__.py
    ├── helpers.py            # Utility helpers (formatting, IO)
    └── nvidia_client.py      # NVIDIA NIM API Client (OpenAI standard)
```

---

## ⚙️ Configuration & Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NVIDIA_API_KEY` | NVIDIA NIM AI API key (`nvapi-...`) | `None` (uses spaCy fallback) |
| `SECRET_KEY` | Secret key for Flask sessions | `dev_key_for_testing` |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
