import os
import pickle
import pytest
import shutil
from unittest.mock import patch, mock_open
from app.services.embedding import generate_embedding

@pytest.mark.asyncio
async def test_generate_embedding_new_vocab(tmp_path):
    # Point to a clean, temporary vocab directory
    vocab_dir = tmp_path / "vocabulary"
    os.makedirs(vocab_dir)

    vocab_path = vocab_dir / "tfidf_vocab.pkl"

    # Monkeypatch the vocab path in the actual function
    original_vocab_path = "vocabulary/tfidf_vocab.pkl"
    try:
        # Replace the path in the source code dynamically
        import app.services.embedding as embedding_module
        embedding_module.vocab_path = str(vocab_path)

        # Run the actual embedding generator
        vector = await embedding_module.generate_embedding("The quick brown fox jumps over the lazy dog")

        assert isinstance(vector, list)
        assert len(vector) > 0
    finally:
        # Reset path override if necessary
        embedding_module.vocab_path = original_vocab_path


@pytest.mark.asyncio
async def test_generate_embedding_with_existing_vocab(tmp_path):
    # Create fake vocab file
    vocab = {"the": 0, "quick": 1, "brown": 2}
    vocab_path = tmp_path / "vocabulary" / "tfidf_vocab.pkl"
    os.makedirs(vocab_path.parent)
    with open(vocab_path, "wb") as f:
        pickle.dump(vocab, f)

    with patch("app.services.embedding.os.path.exists", return_value=True), \
         patch("app.services.embedding.open", create=True, new_callable=mock_open) as m:
        m.return_value.__enter__.return_value = open(vocab_path, "rb")
        vector = await generate_embedding("the quick brown")
        assert isinstance(vector, list)
        assert len(vector) > 0


@pytest.mark.asyncio
async def test_generate_embedding_with_corrupt_vocab(tmp_path):
    vocab_path = tmp_path / "vocabulary" / "tfidf_vocab.pkl"
    os.makedirs(vocab_path.parent)
    with open(vocab_path, "wb") as f:
        f.write(b"corrupted content")

    def fake_exists(path):
        return True

    with patch("app.services.embedding.os.path.exists", fake_exists), \
         patch("app.services.embedding.open", create=True, new_callable=mock_open) as m:
        m.return_value.__enter__.return_value = open(vocab_path, "rb")
        with pytest.raises(RuntimeError, match="Vocabulary file is corrupted or empty"):
            await generate_embedding("bad vocab")

