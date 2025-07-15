# Aura: AI-Powered Disaster Response System

Aura is a full-stack prototype application that demonstrates the use of Natural Language Processing (NLP) for interpreting and visualizing disaster management commands. An operator can issue commands in plain English, and the system parses the intent, extracts critical parameters, and simulates the action on an interactive map.

 <!-- It's a great idea to add a real screenshot here! -->

## Features

-   **Intent Recognition:** Classifies the user's command into a predefined set of actions (e.g., `search_survivors`, `deploy_supplies`).
-   **Entity Extraction:** Pulls out key parameters from the command, such as locations, coordinates, quantities, and technology types.
-   **Interactive Map Visualization:** Uses Leaflet.js to provide a real-time visual representation of commands on a map, including search radii, supply drops, and hazard zones.
-   **Safety Confirmation:** Implements a confirmation dialog for actions flagged as `safety_critical`, mimicking a real-world command and control system.
-   **Full-Stack Architecture:** Built with a Python/Flask backend for NLP processing and a modern HTML/CSS/JavaScript frontend for the user interface.

## Tech Stack

-   **Backend:**
    -   Python 3
    -   Flask (Web Framework)
    -   Scikit-learn (Machine Learning for Intent Classification)
    -   spaCy (NLP for Entity Extraction)
    -   Pandas (Data Handling)

-   **Frontend:**
    -   HTML5
    -   CSS3 (with a modern, dark-theme UI)
    -   JavaScript (ES6+)
    -   Leaflet.js (Interactive Mapping Library)

## NLP Model Approach

Given the small dataset of 50 examples, a deep learning model would be inappropriate and prone to overfitting. The project takes a more practical and robust approach:

1.  **Intent Classification:** A `scikit-learn` pipeline combining a **TF-IDF Vectorizer** and a **Support Vector Machine (SVM)** classifier is used. This classic ML stack is highly effective and reliable for text classification on smaller datasets.
2.  **Entity Extraction:** A hybrid strategy is employed:
    -   **spaCy's NER:** Used to identify general entities like locations (`GPE`) and numbers (`CARDINAL`).
    -   **Rule-Based Matching:** Regular expressions and keyword lists are used to extract domain-specific entities (e.g., coordinates, radii, sensor types) that a general-purpose model would miss.

This pragmatic approach demonstrates an understanding of choosing the right tool for the job based on data constraints.

## Bilingual Tamil-English Command Mapping (Robust)

- **Direct Mapping:** Every Tamil command in the dataset is mapped directly (using normalization) to its corresponding English command and simulation. This guarantees perfect simulation for all dataset Tamil commands.
- **Fuzzy Matching:** If the input Tamil command is close (even with minor changes or typos) to a dataset command, it will still map to the correct English command using fuzzy matching (via rapidfuzz).
- **Semantic Search:** If the input is not Tamil or not in the dataset, the system falls back to semantic search (using a multilingual model) for English or unknown input.

### How It Works
- At startup, the system builds a normalized dictionary of all Tamil commands in the dataset.
- On user input, it first checks for an exact normalized match, then uses fuzzy matching, and only then falls back to semantic search.
- This ensures that every Tamil command in the dataset (even with minor changes) always triggers the correct English simulation.

### Adding New Commands
- To add new Tamil/English commands, simply add them to `data/nlp_disaster.json` with both `english` and `tamil` fields.
- Restart the server after editing the dataset to rebuild the mapping.

### Testing
- Enter any Tamil command from the dataset (even with minor changes or typos) in the input box. The correct English mapping and simulation will be shown.
- You can also enter English commands as before.

### Troubleshooting
- If a Tamil command does not map correctly:
  - Make sure it exists in the dataset and is spelled correctly.
  - Check for invisible Unicode or whitespace issues.
  - Restart the Flask server after any code or dataset changes.
  - Ensure `rapidfuzz` is installed and the model is set to `paraphrase-multilingual-MiniLM-L12-v2`.
- For debugging, the system prints the normalized dataset and user input to the console.

### Requirements
- `rapidfuzz` for fuzzy matching
- `sentence-transformers` with the `paraphrase-multilingual-MiniLM-L12-v2` model for semantic search

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd aura_disaster_response_ai
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the spaCy language model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  **Open your browser** and navigate to `http://127.0.0.1:5000`. The Aura interface should now be visible and ready for commands. 