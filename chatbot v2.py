from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS
import logging

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Configure the Generative AI client
def configure_genai():
    """Configure the Google Generative AI client using an API key."""
    api_key = "AIzaSyBNMCGdvPBYdJU-pf6Ak5MV8LThIvs7CX8"  
    genai.configure(api_key=api_key)

# Create and configure the Generative AI model
def create_chat_model():
    """Create and configure the Generative AI model."""
    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1000,
        "response_mime_type": "text/plain",
    }
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

# Initialize the chat model
chat_model = None

# Log user interactions to a text file
def log_interaction(user_message, bot_response):
    """Log the user message and bot response to a file."""
    with open("chat_history.txt", "a") as history_file:
        history_file.write(f"User: {user_message}\n")
        history_file.write(f"Bot: {bot_response}\n\n")

# Load chat history from file
def load_chat_history():
    """Load the chat history from the log file."""
    history = []
    try:
        with open("chat_history.txt", "r") as history_file:
            lines = history_file.readlines()
            for i in range(0, len(lines), 2):
                user_line = lines[i].strip().replace("User: ", "")
                bot_line = lines[i + 1].strip().replace("Bot: ", "")
                if user_line and bot_line:  
                    history.append({"role": "user", "parts": user_line})
                    history.append({"role": "model", "parts": bot_line})
    except FileNotFoundError:
        pass  # No history file found; return an empty history
    return history

@app.route("/")
def home():
    """Render the main HTML page."""
    return render_template("webpage.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat requests."""
    user_input = request.json.get("message", "")
    logging.debug(f"Received message: {user_input}")
    
    if not user_input.strip():  # Check if the message is empty or just whitespace
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        # Load chat history
        chat_history = load_chat_history()
        logging.debug(f"Chat history: {chat_history}")

        # Start a chat session with history
        chat_session = chat_model.start_chat(history=chat_history)
        response = chat_session.send_message(user_input)
        bot_response = response.text
        logging.debug(f"Model response: {bot_response}")

        # Log interaction
        log_interaction(user_input, bot_response)

        return jsonify({"response": bot_response})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

# Main function to start the Flask app
if __name__ == "__main__":
    try:
        configure_genai()
        chat_model = create_chat_model()
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Initialization error: {e}")

