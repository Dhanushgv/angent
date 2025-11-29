
import re
DEFAULT_SKILLS = ['python','java','aws','docker','react','node','sql','nlp','pandas','tensorflow']
def compute_skill_gap(jd_text, resume_text):
    jd_sk = [s for s in DEFAULT_SKILLS if s in jd_text.lower()]
    res_sk = [s for s in jd_sk if s in resume_text.lower()]
    missing = [s for s in jd_sk if s not in res_sk]
    coverage = (len(res_sk)/len(jd_sk)) if jd_sk else 0.0
    return {'jd_skills':jd_sk,'resume_skills':res_sk,'matched':res_sk,'missing':missing,'coverage':coverage}

def resume_quality_score(text):
    t=(text or '')
    words = len(re.findall(r'\w+', t))
    tokens = ['email','phone','experience','education','skills','projects']
    presence = sum(1 for tok in tokens if tok in t.lower())
    presence_score = min(1.0, presence/len(tokens))
    length_score = min(1.0, words/400)
    keyword_score = min(1.0, len([k for k in ['python','java','sql','aws','docker'] if k in t.lower()])/5)
    overall = 0.3*presence_score + 0.4*length_score + 0.3*keyword_score
    return {'overall_score':overall,'presence_score':presence_score,'length_score':length_score,'keyword_score':keyword_score}
