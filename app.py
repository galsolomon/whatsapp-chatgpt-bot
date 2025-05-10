from flask import Flask, request
import os
import openai

app = Flask(__name__)

# הגדרת לקוח OpenAI עם מפתח מהסביבה
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/whatsapp", methods=["POST"])
def reply():
    # קבלת ההודעה שנשלחה לבוט
    msg = request.values.get("Body", "")
    if not msg:
        return "OK"

    try:
        # בקשת תשובה מ־ChatGPT (gpt-4.1-nano)
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "ענה בעברית, בקצרה ולעניין, בלי אימוג׳ים."},
                {"role": "user", "content": msg}
            ]
        )

        reply_text = response.choices[0].message.content.strip()

        # שליחת תשובה ל־Twilio בפורמט XML
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}

    except Exception as e:
        # במקרה של שגיאה – שולח טקסט ידידותי למשתמש
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>שגיאה: {str(e)}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}

# 🟢 חשוב מאוד ל־Render: האזנה לפורט המתאים
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
