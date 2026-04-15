# ResumeAI — Smart Resume Analyzer

An AI-powered resume analyzer that matches your resume against any job description and gives instant feedback.

## Features
- Upload resume as PDF
- Paste any job description
- Get a match score (0–100)
- See matching and missing skills
- Get actionable improvement suggestions
- Powered by Claude AI (Anthropic)

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Claude API (Anthropic)
- **PDF Parsing:** pypdf

## Local Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Anthropic API key:
   ```bash
   # Windows
   set ANTHROPIC_API_KEY=your_api_key_here
   # Mac/Linux
   export ANTHROPIC_API_KEY=your_api_key_here
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open http://localhost:5000

## Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repo
4. Set environment variable: `ANTHROPIC_API_KEY = your_key`
5. Deploy!

## Author
Mayur Sathe — [sathemayur29@gmail.com](mailto:sathemayur29@gmail.com)
