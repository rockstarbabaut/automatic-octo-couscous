import os

import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# Set your OpenAI API key (safer to use environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Astro-Baba API is running! Use POST /generate-report"


@app.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.json
    name = data.get("name")
    dob = data.get("dob")
    place = data.get("place")
    gender = data.get("gender")
    report_type = data.get("report_type", "Full Report")

    # Build prompt for GPT
    prompt = f"""
You are an expert astrologer and numerologist. Generate a personalized report for:
- Name: {name}
- Date of Birth: {dob}
- Place of Birth: {place}
- Gender: {gender}
- Report Type: {report_type}

Keep it simple, clear, insightful, and respectful. Do not start with “Reply from ChatGPT” or similar lines.
    """

    # Request ChatGPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8,
        )

        message = response['choices'][0]['message']['content'].strip()

        return jsonify({"report_text": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
