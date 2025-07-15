import json
from flask import Flask, render_template, request, jsonify
from nlp_model import DisasterNLP

app = Flask(__name__)

# --- Initialization ---
# Instantiate and train the NLP model when the server starts.
# This is efficient as it's done only once.
print("Initializing and training NLP model...")
nlp_processor = DisasterNLP()
print("Model training complete. Server is ready.")

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

        # Use the NLP model to predict intent and entities
        prediction = nlp_processor.predict(command_text)

        if prediction is None:
            return jsonify({'error': 'Could not process empty command'}), 400
            
        print(f"Received: '{command_text}' -> Predicted: {prediction['intent']}")
        
        return jsonify(prediction)

    except Exception as e:
        print(f"Error processing command: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

@app.route('/get_examples', methods=['GET'])
def get_examples():
    """Provides example commands to the frontend."""
    examples = nlp_processor.df['english'].sample(5).tolist()
    return jsonify(examples)

if __name__ == '__main__':
    # Setting debug=False is better for a "production" demo, 
    # but True is fine for development.
    app.run(debug=True, port=5000) 