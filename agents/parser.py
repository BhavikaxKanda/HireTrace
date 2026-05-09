import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def extract_jd_requirements(jd_text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # System prompt to ensure structured extraction
    system_prompt = """
    You are an expert HR Recruitment Agent. Your task is to extract requirements from a Job Description.
    Return ONLY a JSON object with the following keys:
    - "skills": A list of required technical skills.
    - "experience": Minimum years of experience required (integer).
    - "education": Minimum degree required.
    - "seniority": Seniority level (e.g., Junior, Mid, Senior).
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": jd_text}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)