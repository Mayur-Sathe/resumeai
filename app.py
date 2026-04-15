import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from pypdf import PdfReader
import io

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max upload

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def analyze_with_gemini(resume_text, job_description):
    prompt = f"""You are an expert resume analyzer. Analyze the resume against the job description and return ONLY a valid JSON object with no extra text, no markdown, no backticks.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:1500]}

Return this exact JSON structure:
{{
  "match_score": <integer 0-100>,
  "summary": "<2 sentence overall assessment>",
  "matching_skills": ["skill1", "skill2", "skill3"],
  "missing_skills": ["skill1", "skill2", "skill3"],
  "suggestions": [
    "<specific actionable suggestion 1>",
    "<specific actionable suggestion 2>",
    "<specific actionable suggestion 3>"
  ],
  "verdict": "<one of: Strong Match, Good Match, Partial Match, Weak Match>"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=30,
    )
    print(f"GEMINI STATUS: {response.status_code}")
    print(f"GEMINI RESPONSE: {response.text[:500]}")
    response.raise_for_status()
    content = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    # Strip markdown fences if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content.strip())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    print(f"API KEY LOADED: {GEMINI_API_KEY[:8]}...")  # add this line
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
    if not GEMINI_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400
    if not resume_file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    try:
        resume_text = extract_text_from_pdf(resume_file.read())
        if not resume_text:
            return jsonify({"error": "Could not extract text from PDF"}), 400
        result = analyze_with_gemini(resume_text, job_description)
        return jsonify(result)
    except json.JSONDecodeError as e:
        print(f"JSON ERROR: {e}")
        return jsonify({"error": "Failed to parse AI response"}), 500
    except requests.RequestException as e:
        print(f"REQUEST ERROR: {e}")
        print(f"RESPONSE: {e.response.text if hasattr(e, 'response') and e.response else 'no response'}")
        return jsonify({"error": "API request failed"}), 500
    except Exception as e:
        print(f"GENERAL ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
