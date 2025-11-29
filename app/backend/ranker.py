
import numpy as np
from sklearn.preprocessing import MinMaxScaler
def cosine_sim(a,b): return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-10))
def rank_resumes(jd_emb, resume_embs, metas, weight_skill=0.6, weight_embed=0.4):
    sims=[cosine_sim(jd_emb, r) for r in resume_embs]
    skill_scores=[len(m.get('skills',[])) for m in metas]
    scaler=MinMaxScaler()
    try:
        skill_norm = scaler.fit_transform(np.array(skill_scores).reshape(-1,1)).ravel()
        embed_norm = scaler.fit_transform(np.array(sims).reshape(-1,1)).ravel()
    except:
        skill_norm = [0]*len(sims); embed_norm=[0]*len(sims)
    final = weight_skill*np.array(skill_norm) + weight_embed*np.array(embed_norm)
    idx = np.argsort(final)[::-1]
    out=[]
    for i in idx:
        out.append({'index':int(i),'score':float(final[i]),'embed_score':float(embed_norm[i]),'skill_score':float(skill_norm[i]),'meta':metas[i]})
    return out
