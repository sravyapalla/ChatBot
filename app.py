from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-1.5-flash")

# Store chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Append user message to history
        chat_history.append({"role": "user", "parts": [{"text": user_message}]})

        # Start chat session with history
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_message)
        bot_response = response.text

        # Append bot response to history
        chat_history.append({"role": "model", "parts": [{"text": bot_response}]})

        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))