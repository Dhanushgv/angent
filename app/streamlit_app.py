import streamlit as st
import pandas as pd, os, tempfile
from backend.parser import parse_resume_file, extract_meta
from backend.embeddings import embed_texts, init_model
from backend.ranker import rank_resumes
from backend.analysis import compute_skill_gap, resume_quality_score
from backend.ai_tools import generate_summary, generate_interview_questions, hr_recommendation, export_candidate_pdf

# ---------- UI Setup ----------
st.set_page_config(page_title="AI Resume Studio — Futuristic", layout="wide")

# ---- Helper: convert 0–1 into percentage ----
def to_percent(x):
    return int(x * 100)

# ---- HEADER ----
st.title("AI Resume Studio — Futuristic Version")
st.caption("Now showing all scores & thresholds in 0–100% format")

# ---------- Sidebar Controls ----------
st.sidebar.header("Controls")

# Threshold 0–100 UI (converted internally to 0–1)
threshold = st.sidebar.slider("Score Threshold (%)", 0, 100, 65) / 100

use_samples = st.sidebar.checkbox("Use Sample Resumes", value=True)
top_k = st.sidebar.slider("Max Candidates", 1, 20, 6)

# ---------- Inputs ----------
jd = st.text_area("Paste Job Description (JD)", height=150)
uploads = st.file_uploader("Upload resumes (PDF/TXT)", accept_multiple_files=True)

# ---------- Run Button ----------
if st.button("Run Screening"):

    if not jd or len(jd.strip()) < 5:
        st.error("Please provide a valid Job Description.")
        st.stop()

    # ---------- Load resumes ----------
    texts, names = [], []

    if uploads and not use_samples:
        for f in uploads:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f.name)[1])
            tmp.write(f.read())
            tmp.close()

            texts.append(parse_resume_file(tmp.name))
            names.append(f.name)
            os.unlink(tmp.name)

    else:
        base = os.path.join(os.path.dirname(__file__), "..", "data", "samples")
        for fn in sorted(os.listdir(base)):
            if fn.endswith(".txt"):
                texts.append(parse_resume_file(os.path.join(base, fn)))
                names.append(fn)

    # ---------- Embeddings ----------
    init_model()
    jd_emb = embed_texts([jd])[0]
    resume_embs = embed_texts(texts)

    # ---------- Metadata Extraction ----------
    metas = []
    for i, t in enumerate(texts):
        m = extract_meta(t)
        m["filename"] = names[i]
        m["skill_gap"] = compute_skill_gap(jd, t)
        m["quality"] = resume_quality_score(t)
        metas.append(m)

    # ---------- Ranking ----------
    ranked = rank_resumes(jd_emb, resume_embs, metas)

    # ---------- Chart ----------
    st.subheader("Score Comparison (0–100%)")
    df = pd.DataFrame([
        {"name": r["meta"]["filename"], "score": to_percent(r["score"])}
        for r in ranked
    ]).sort_values("score", ascending=False)
    st.bar_chart(df.set_index("name")["score"])

    # ---------- Candidate Cards ----------
    st.subheader("Candidates")
    shown = 0

    for r in ranked:
        if r["score"] < threshold:
            continue
        if shown >= top_k:
            break

        shown += 1
        meta = r["meta"]

        score_pct = to_percent(r["score"])
        coverage_pct = to_percent(meta["skill_gap"]["coverage"])
        quality_pct = to_percent(meta["quality"]["overall_score"])

        st.markdown(f"""
        ### {meta['filename']} — **{score_pct}%**
        **Skill Coverage:** {coverage_pct}%  
        **Resume Quality:** {quality_pct}%
        """)

        # Summary
        summary = generate_summary(meta["filename"], meta.get("skills", []), meta.get("years_exp"), meta["quality"]["overall_score"])
        st.write("**Summary:**", summary)

        # Interview Qs
        qs = generate_interview_questions(jd, meta.get("skills", []), meta["skill_gap"]["missing"])
        st.write("**Sample Interview Questions:**")
        for q in qs:
            st.write("- ", q)

        # Recommendation (Hire / Consider / Reject)
        rec = hr_recommendation(r["score"])
        st.write("**HR Recommendation:**", rec)

        # PDF Export
        pdf = export_candidate_pdf(meta, r["score"], jd)
        st.download_button("Download Report PDF", pdf, file_name=meta["filename"].replace(" ", "_") + "_report.pdf")

    st.success(f"Displayed {shown} candidates above threshold.")
