
import pdfplumber, re
def parse_resume_file(path):
    if path.lower().endswith('.pdf'):
        text=''
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                text += (p.extract_text() or '') + '\n'
        return text
    else:
        return open(path,'r',errors='ignore').read()

def extract_meta(text):
    candidates = ['python','java','aws','docker','react','node','sql','nlp','pandas','tensorflow','excel','scikit-learn']
    found=[c for c in candidates if c in text.lower()]
    years=None
    m=re.search(r'(\d+)\s+years', text.lower())
    if m: years=int(m.group(1))
    return {'skills':found, 'years_exp': years}
