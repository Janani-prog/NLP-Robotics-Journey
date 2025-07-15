import json
import random
from flask import Flask, render_template, request, jsonify
from nlp_model import DisasterNLP

app = Flask(__name__)

# --- Initialization ---
# Instantiate the NLP model when the server starts.
# This is efficient as it's done only once.
print("--- Server starting up ---")
nlp_processor = DisasterNLP()
print("--- NLP model initialization complete. Server is ready. ---")

# --- Routes ---
@app.route('/')
def index():
    """Renders the main user interface."""
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    """
    Receives a text command, processes it using the NLP model,
    and returns the structured data as JSON.
    """
    try:
        data = request.get_json()
        command_text = data.get('text', '')

        if not command_text:
            return jsonify({'error': 'No text provided'}), 400

        # Use the NLP model to predict the corresponding command
        prediction = nlp_processor.predict(command_text)

        if prediction is None:
            return jsonify({'error': 'Could not process empty command'}), 400
            
        print(f"Received: '{command_text}' -> Predicted Intent: {prediction['intent']}")
        
        # Return the full structured data object
        return jsonify(prediction)

    except Exception as e:
        print(f"ERROR in process_command: {e}")
        # In a real app, you might log the stack trace here.
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/get_examples', methods=['GET'])
def get_examples():
    """Provides a few random example commands to the frontend."""
    try:
        # Get all English commands from the loaded data
        all_english_commands = [item['english'] for item in nlp_processor.data]
        
        # Define how many examples to return
        num_examples = min(5, len(all_english_commands))
        
        # Randomly sample the commands
        examples = random.sample(all_english_commands, num_examples)
        
        return jsonify(examples)
    except Exception as e:
        print(f"ERROR in get_examples: {e}")
        return jsonify({'error': 'Could not retrieve examples'}), 500

if __name__ == '__main__':
    # Setting debug=True is fine for development.
    # It enables auto-reloading when you change the code.
    app.run(debug=True, port=5000)