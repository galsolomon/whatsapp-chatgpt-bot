from flask import Flask, request
import os
import openai

app = Flask(__name__)

# לקוח לפי הגרסה החדשה של openai>=1.0
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/whatsapp", methods=["POST"])
def reply():
    msg = request.values.get("Body", "")
    if not msg:
        return "OK"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "ענה בצורה ברורה, קצרה, וללא אימוג'ים."},
                {"role": "user", "content": msg}
            ]
        )

        reply_text = response.choices[0].message.content

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}

    except Exception as e:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>שגיאה: {str(e)}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}

# 🟢 חשוב: זה מה שמוודא ש-Render יודע לאיזה פורט להתחבר
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
