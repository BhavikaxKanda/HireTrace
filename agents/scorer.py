import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def score_candidate(jd_requirements, masked_resume_text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # LOGIC: Strict Technical Audit with Modest Transferable Rewards
    scoring_prompt = f"""
    Act as a Technical Recruiter for Schneider Electric. 
    Audit this candidate against the Business Analytics Intern JD.
    
    SCORING PROTOCOL:
    1. Skills Match (30%): Strictly look for Tableau, Excel (Pivot/VLOOKUP), and Python/R. 
       - Deduct 1.5 for complete absence of Tableau or Excel metrics[cite: 10, 17].
    2. Experience Relevance (25%): Value real-world data handling (e.g., managing 200+ records)[cite: 22, 106].
    3. Project Complexity (20%): Reward exceptional logic (RAG, Agentic AI, Forensics) even if not analytics-specific[cite: 228, 229].
    
    SCORING BANDS:
    - 8.0+: Direct match with tools and strong project logic.
    - 7.0 - 7.9: Strong logic/potential but missing 1 core software (e.g., Tableau).
    - Below 6.0: Lacks professional experience and core analytical tools.

    REQUIRED JSON OUTPUT:
    {{
      "dimensions": {{
        "Skills Match": {{"score": 0.0, "justification": "text"}},
        "Experience Relevance": {{"score": 0.0, "justification": "text"}},
        "Education & Certs": {{"score": 0.0, "justification": "text"}},
        "Project/Portfolio": {{"score": 0.0, "justification": "text"}},
        "Communication Quality": {{"score": 0.0, "justification": "text"}}
      }},
      "overall_summary": "fact-based technical audit"
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"{scoring_prompt}\n\nJD: {jd_requirements}\n\nResume: {masked_resume_text}"}],
        response_format={"type": "json_object"},
        temperature=0.0  # Zero randomness for stable ranking
    )
    
    return json.loads(response.choices[0].message.content)