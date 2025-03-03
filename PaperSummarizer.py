import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# ------------------------------------------------------------
# 1. Summarization Function using Hugging Face Transformers
# ------------------------------------------------------------
def summarize_paper(text, max_length=150, min_length=80):
    """
    Summarizes the given research paper text using a pre-trained summarization model.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # The summarizer expects the text to be shorter than the model's maximum length.
    # For long documents, consider splitting the text into chunks.
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']


# ------------------------------------------------------------
# 2. Semantic Similarity Ranking using Sentence Transformers
# ------------------------------------------------------------
def rank_sentences_by_similarity(sentences, query, st_model):
    """
    Ranks sentences based on semantic similarity with the provided query.
    """
    query_embedding = st_model.encode(query, convert_to_tensor=True)
    sentence_embeddings = st_model.encode(sentences, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, sentence_embeddings)[0]
    
    # Get indices of sentences sorted by similarity score (highest first)
    sorted_indices = torch.argsort(cosine_scores, descending=True)
    ranked = [(sentences[i], cosine_scores[i].item()) for i in sorted_indices]
    return ranked


# ------------------------------------------------------------
# 3. Bias / Inconsistency Detection via Zero-Shot Classification
# ------------------------------------------------------------
def detect_bias(sentence, classifier):
    """
    Uses zero-shot classification to detect if a sentence might be biased or methodologically inconsistent.
    Candidate labels can be refined or extended as needed.
    """
    candidate_labels = ["biased", "inconsistent", "sound"]
    result = classifier(sentence, candidate_labels)
    best_label = result['labels'][0]
    score = result['scores'][0]
    return best_label, score


# ------------------------------------------------------------
# 4. Main Pipeline
# ------------------------------------------------------------
if __name__ == "__main__":
    # ----- Load the research paper text -----
    # For this demo, ensure you have a text file (e.g., "research_paper.txt")
    try:
        with open("research_paper.txt", "r", encoding="utf-8") as f:
            paper_text = f.read()
    except FileNotFoundError:
        print("Error: 'research_paper.txt' not found. Please provide a research paper text file.")
        exit()

    # ----- Summarize the research paper -----
    print("Summarizing the research paper...")
    summary_text = summarize_paper(paper_text)
    print("\n--- Summary ---")
    print(summary_text)

    # ----- Tokenize the summary into sentences -----
    sentences = sent_tokenize(summary_text)

    # ----- Semantic Similarity Ranking -----
    # Define a query that focuses on ethical issues, biases, and methodological inconsistencies.
    query = "ethical issues, bias, and methodological inconsistencies"
    st_model = SentenceTransformer('all-MiniLM-L6-v2')
    ranked_sentences = rank_sentences_by_similarity(sentences, query, st_model)

    print("\n--- Ranked Sentences by Semantic Similarity ---")
    for sent, score in ranked_sentences:
        print(f"Score: {score:.4f} - {sent}")

    # ----- Fact-Checking / Bias Detection -----
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("\n--- Bias and Consistency Analysis ---")
    for sent in sentences:
        label, score = detect_bias(sent, classifier)
        print(f"Sentence: {sent}\n-> Detected as: {label} (confidence: {score:.4f})\n")
