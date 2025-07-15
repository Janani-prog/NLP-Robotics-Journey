import json
import torch
from sentence_transformers import SentenceTransformer, util
import re
from rapidfuzz import process, fuzz
import os
import sys

class DisasterNLP:
    def __init__(self):
        """
        Initializes the NLP model using Sentence Transformers.
        This model finds the most semantically similar command from the dataset,
        supporting both English and Tamil.
        """
        print("Initializing Sentence Transformer model (paraphrase-multilingual-MiniLM-L12-v2)...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("Model loaded. Loading and pre-processing disaster data...")
        self.data = self._load_data()

        # Build a normalized Tamil-to-index map for fast exact and fuzzy lookup
        self.tamil_to_index = {}
        for idx, item in enumerate(self.data):
            if 'tamil' in item and item['tamil']:
                norm_tamil = self.normalize_text(item['tamil'])
                self.tamil_to_index[norm_tamil] = idx

        # Build bilingual corpus: both English and Tamil for each command for semantic search
        self.bilingual_corpus = []
        self.bilingual_index_map = []  # Maps each entry in bilingual_corpus to the original self.data index
        for idx, item in enumerate(self.data):
            # Add English sentence
            self.bilingual_corpus.append(item['english'])
            self.bilingual_index_map.append(idx)
            # Add Tamil sentence if it exists
            if 'tamil' in item and item['tamil']:
                self.bilingual_corpus.append(item['tamil'])
                self.bilingual_index_map.append(idx)

        print("Computing embeddings for the bilingual corpus...")
        self.corpus_embeddings = self.model.encode(self.bilingual_corpus, convert_to_tensor=True, show_progress_bar=True)
        print("Corpus embeddings computed. NLP system is ready.")

    def _load_data(self):
        """Loads the consolidated bilingual JSON data from the 'data' directory."""
        # This path is relative to the project root, where app.py is executed.
        data_path = 'data/nlp_disaster.json'
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                print(f"Successfully loaded data from {data_path}")
                return json.load(f)
        except FileNotFoundError:
            print(f"FATAL ERROR: Data file not found at '{data_path}'.")
            print("Please ensure 'nlp_disaster.json' is located inside a 'data' folder in your project root.")
            sys.exit(1) # Exit because the application cannot run without data.
        except json.JSONDecodeError:
            print(f"FATAL ERROR: Could not parse '{data_path}'. Please ensure it is a valid JSON file.")
            sys.exit(1)


    def normalize_text(self, text):
        """Removes spaces, punctuation, and lowercases text for robust matching."""
        return re.sub(r'[\s\W_]+', '', text).casefold()

    def predict(self, query: str):
        """
        Finds the most similar command in the corpus to the user's query.
        It prioritizes exact/fuzzy matches in Tamil before falling back to semantic search.
        """
        if not query or not query.strip():
            return None

        clean_query = self.normalize_text(query)

        # 1. Direct normalized Tamil match (Highest Priority)
        if clean_query in self.tamil_to_index:
            idx = self.tamil_to_index[clean_query]
            best_match_command = self.data[idx].copy()
            best_match_command['original_query'] = query
            print(f"Result: Found direct Tamil match for '{query}' -> ID: {best_match_command['id']}")
            return best_match_command

        # 2. Fuzzy Tamil match using rapidfuzz (Second Priority)
        # We use a high threshold to avoid incorrect matches for short/dissimilar queries.
        choices = list(self.tamil_to_index.keys())
        if choices:
            # The scorer `fuzz.ratio` works well for matching whole sentences.
            match, score, _ = process.extractOne(clean_query, choices, scorer=fuzz.ratio)
            if score > 85: # Using a higher threshold (e.g., 85) is safer for sentence matching
                idx = self.tamil_to_index[match]
                best_match_command = self.data[idx].copy()
                best_match_command['original_query'] = query
                print(f"Result: Found fuzzy Tamil match for '{query}' (score: {score:.2f}) -> ID: {best_match_command['id']}")
                return best_match_command

        # 3. Fallback to bilingual semantic search (Works for English, Tamil, and mixed queries)
        print("No exact/fuzzy Tamil match found. Falling back to bilingual semantic search...")
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        # Compute cosine similarities
        cos_scores = util.cos_sim(query_embedding, self.corpus_embeddings)[0]

        # Find the best match in the bilingual corpus
        best_match_bilingual_idx = torch.argmax(cos_scores).item()
        
        # Map back to the original data index
        best_match_idx = self.bilingual_index_map[best_match_bilingual_idx]
        
        best_match_command = self.data[best_match_idx].copy()
        best_match_command['original_query'] = query
        
        score = cos_scores[best_match_bilingual_idx].item()
        print(f"Result: Found semantic match for '{query}' (score: {score:.2f}) -> ID: {best_match_command['id']}")
        
        return best_match_command