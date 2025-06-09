import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

"""
TF-IDF stands for Term Frequency – Inverse Document Frequency, 
used to convert text into numeric vectors based on word importance.
"""
async def generate_embedding(text: str):
    await asyncio.sleep(0.1)  # simulate async call

    vocab_path = "vocabulary/tfidf_vocab.pkl"

    if os.path.exists(vocab_path):
        # Load the existing vocab
        try:
            with open(vocab_path, "rb") as f:
                vocab = pickle.load(f)
            vectorizer = TfidfVectorizer(vocabulary=vocab)
            vector = vectorizer.fit_transform([text])
        except (EOFError, pickle.UnpicklingError) as e:
            raise RuntimeError("Vocabulary file is corrupted or empty") from e
    else:
        # First document: train new vectorizer and save vocab
        vectorizer = TfidfVectorizer()
        """
        Applies the TF-IDF transformation to the single text input (passed as a list with one item).
        Returns a sparse matrix of shape (1, number_of_features).
        """
        vector = vectorizer.transform([text])
        """
        Converts the sparse matrix to a dense array.
        Extracts the first (and only) vector.
        Converts it to a regular Python list and returns it.
        """

        os.makedirs("vocabulary", exist_ok=True)
        with open(vocab_path, "wb") as f:
            pickle.dump(vectorizer.vocabulary_, f)

    return vector.toarray()[0].tolist()

    """
    🧠 Real Use Case
    In a real-world RAG or NLP system, this would be replaced with:
    OpenAIEmbeddings from Langchain
    sentence-transformers from Hugging Face
    Or any LLM-generated vector
    """