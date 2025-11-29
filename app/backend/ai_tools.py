from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_summary(name, skills, years, quality):
    yrs = f"{years} yrs" if years else "N/A"
    skills_text = ", ".join(skills) if skills else "No skills detected"
    return f"{name}: {skills_text}. Experience: {yrs}. Resume Quality Score: {quality:.2f}"

def generate_interview_questions(jd_text, skills, missing):
    qs = []
    for s in skills[:4]:
        qs.append(f"Explain a project where you used {s} and the impact it created.")
    for m in missing[:2]:
        qs.append(f"How comfortable are you with {m}? Describe any exposure you have.")
    if not qs:
        qs = ["Tell me about the most relevant project you worked on for this role."]
    return qs

def hr_recommendation(score, coverage=None, quality=None):
    """Recommendation based ONLY on final score."""
    if score >= 0.75: return "Hire"
    elif score >= 0.55: return "Consider"
    else: return "Reject"

def export_candidate_pdf(meta, score, jd):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 750, f"Candidate Report: {meta.get('filename','')}")

    c.setFont("Helvetica", 11)
    c.drawString(40, 720, f"Final Score: {int(score*100)}%")
    c.drawString(40, 700, f"Skills: {', '.join(meta.get('skills', []))}")
    c.drawString(40, 680, f"Skill Coverage: {int(meta.get('skill_gap',{}).get('coverage',0)*100)}%")
    c.drawString(40, 660, f"Resume Quality: {int(meta.get('quality',{}).get('overall_score',0)*100)}%")

    c.drawString(40, 640, "Job Description:")
    t = c.beginText(40, 620)
    t.setFont("Helvetica", 9)
    t.textLines(jd[:900])
    c.drawText(t)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
