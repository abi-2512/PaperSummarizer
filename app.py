from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import nltk
import os
import torch
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Ensure nltk resources are available
nltk_data_path = os.path.expanduser('~/nltk_data')
nltk.data.path.append(nltk_data_path)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_path)

app = Flask(__name__)
CORS(app)  # Enable CORS on your app

# Initialize models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
st_model = SentenceTransformer('all-MiniLM-L6-v2')

def summarize_paper(text, max_length=150, min_length=80):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def rank_sentences_by_similarity(sentences, query, top_n=5):
    if not sentences:
        return []

    query_embedding = st_model.encode(query, convert_to_tensor=True)
    sentence_embeddings = st_model.encode(sentences, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, sentence_embeddings)[0]

    sorted_indices = torch.argsort(cosine_scores, descending=True)[:top_n]
    return [{"sentence": sentences[i], "score": cosine_scores[i].item()} for i in sorted_indices]

def detect_bias(sentence, threshold=0.6):
    candidate_labels = ["biased", "inconsistent", "sound"]
    result = classifier(sentence, candidate_labels)
    
    best_label = result['labels'][0]
    score = result['scores'][0]

    return (best_label if score >= threshold else "uncertain"), score

@app.route('/summarize', methods=['POST'])
def summarize_endpoint():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({"error": "No text provided."}), 400

    summary = summarize_paper(text)
    sentences = sent_tokenize(summary)

    query = "ethical issues, bias, and methodological inconsistencies"
    ranked = rank_sentences_by_similarity(sentences, query)

    bias_analysis = [{"sentence": sent, "label": detect_bias(sent)[0], "score": detect_bias(sent)[1]} for sent in sentences]

    return jsonify({
        "summary": summary,
        "analysis": {
            "ranked_sentences": ranked,
            "bias_detection": bias_analysis,
            "metadata": {
                "word_count": len(text.split()),
                "summary_length": len(summary.split())
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
