import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Temporarily hardcode the API key to bypass the environment variable issue
api_key = "AIzaSyBN5fdiiFcLFGWIKiU7cFPF_62kb5xwibs"  # Replace with your actual key

genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

# Serve the HTML file for the chatbot
@app.route('/')
def index():
    return render_template('chatbot.html')

# Define the chat route for handling POST requests from the web page
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({'response': 'Please type a message.'})

    # Start the chat session and send the user's message
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)

    # Send the bot's response back to the front-end
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
