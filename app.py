from flask import Flask, request
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]

@app.route("/whatsapp", methods=["POST"])
def reply():
    msg = request.values.get("Body", "")
    if not msg:
        return "OK"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "ענה בצורה ברורה, קצרה, וללא אימוג'ים."},
            {"role": "user", "content": msg}
        ]
    )

    reply_text = response.choices[0].message["content"]

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply_text}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}
