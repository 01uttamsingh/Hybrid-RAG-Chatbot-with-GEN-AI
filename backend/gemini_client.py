import google.generativeai as genai
from config import GEMINI_API_KEY
from prompts import DOC_PROMPT, GENERAL_PROMPT

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Best free-tier safe model
# model = genai.GenerativeModel("models/gemini-flash-lite-latest")
# model = genai.GenerativeModel("gemini-1.5-flash")
# model = genai.GenerativeModel("models/gemini-2.0-flash")
model = genai.GenerativeModel("models/gemini-flash-latest")

def ask_gemini_doc(question, context):
    prompt = f"""
{DOC_PROMPT}

Context:
{context}

Question:
{question}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini DOC error] {type(e).__name__}: {str(e)}"


def ask_gemini_general(question):
    prompt = f"""
{GENERAL_PROMPT}

Question:
{question}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini GENERAL error] {type(e).__name__}: {str(e)}"
