Short Description

AI Resume Screening Agent that analyzes resumes, performs skill-gap evaluation, computes resume quality scores, ranks candidates using semantic similarity, generates summaries and interview questions, exports PDF reports, and provides a futuristic Streamlit UI for recruiters.


Overview

The AI Resume Screening Agent automates the initial stage of recruitment by analyzing resumes against a given Job Description (JD).

The agent extracts metadata, identifies skills, computes structured scoring, generates insights, and prepares recruiter-ready output files — enabling efficient and objective shortlisting.

This system is optimized for:
Speed
Interpretability
HR workflow compatibility
Demonstration-ready agent behavior

Features

Resume Parsing & Metadata Extraction
Skill Gap Analysis
Resume Quality Scoring
Quality score
PDF Report Generation
Auto-Shortlisting
Futuristic UI



Tools, Models & Frameworks Used

 Libraries & Frameworks

Streamlit – UI

SentenceTransformers (MiniLM) – Embeddings

PDFPlumber – PDF parsing

spaCy – Text preprocessing

Matplotlib / Plotly – Visualization

FPDF / ReportLab – PDF generation


Internal Tools Implemented

Resume parser

Skill extractor

Quality evaluator

Ranking engine

PDF report generator

Shortlist manager

Demo email-sender



Project Structure

resume_agent/
├─ app/
│  └─ streamlit_app.py
├─ backend/
│  ├─ parser.py
│  ├─ embeddings.py
│  ├─ ranker.py
│  ├─ analysis.py
│  ├─ ai_tools.py
│  └─ tools.py
├─ data/
│  └─ samples/
├─ .streamlit/
│  └─ config.toml
├─ requirements.txt
└─ README.md


Setup Instructions

1. Clone the repository

git clone <repo-url>
cd resume_agent

2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate

3. Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

4. Install spaCy Model (optional)

python -m spacy download en_core_web_sm

5. Run the Application

streamlit run app/streamlit_app.py


Future Improvements

Add real SMTP email-sending

Add LLM-powered agent command system

Resume improvement suggestions

Multi-candidate comparison dashboard

Database integration (Supabase/Firebase)

DOCX resume support
