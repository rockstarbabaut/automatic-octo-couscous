import os
import io
import openai
from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Load API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return "Astro-Baba API is running! Use POST /generate-report"

def generate_pdf_report(name, dob, place, gender, report_text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Logo and Title
    c.drawImage("logo.png", 50, height - 100, width=100, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(160, height - 70, "Astro-Baba Personalized Report")

    # User Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 130, f"Name: {name}")
    c.drawString(50, height - 150, f"Date of Birth: {dob}")
    c.drawString(50, height - 170, f"Place: {place}")
    c.drawString(50, height - 190, f"Gender: {gender}")

    # Report Text
    text_obj = c.beginText(50, height - 230)
    text_obj.setFont("Helvetica", 11)
    for line in report_text.split('\n'):
        text_obj.textLine(line)
    c.drawText(text_obj)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.json
    name = data.get("name")
    dob = data.get("dob")
    place = data.get("place")
    gender = data.get("gender")
    report_type = data.get("report_type", "Full Report")

    prompt = f"""
You are an expert astrologer and numerologist. Generate a personalized report for:
- Name: {name}
- Date of Birth: {dob}
- Place of Birth: {place}
- Gender: {gender}
- Report Type: {report_type}

Structure:
- Brief personality insight based on zodiac
- Numerology meaning and influence of birth number
- A paragraph combining both energies
- ⚠️ Caution for the Future: Mention likely challenge period or emotional/financial caution between 2 months. Keep it short and practical.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8,
        )

        report_text = response.choices[0].message.content.strip()
        pdf = generate_pdf_report(name, dob, place, gender, report_text)

        return send_file(pdf, download_name=f"{name}_astro_report.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
