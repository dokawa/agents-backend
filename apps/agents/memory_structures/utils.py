import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

from apps.agents.constants import EMBEDDING_MODEL, MAX_TOKENS


def get_embedding(
    text,
    model=EMBEDDING_MODEL,
    max_tokens=MAX_TOKENS,
    average=True,
):
    chunk_embeddings = []
    tokenizer = get_tokenizer()
    chunks, chunk_lens = create_chunks(text, max_tokens, tokenizer)

    for chunk in chunks:
        chunk_embeddings.append(embed(tokenizer.decode(chunk), model=model))

    if average:
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        chunk_embeddings = chunk_embeddings / np.linalg.norm(
            chunk_embeddings
        )  # normalizes length to 1
        chunk_embeddings = chunk_embeddings.tolist()
        print(f"hucnk {len(chunk_embeddings)} ")
    return chunk_embeddings


def embed(sentence, model=EMBEDDING_MODEL):
    model = SentenceTransformer(f"sentence-transformers/{model}")

    embeddings = model.encode(sentence)
    return embeddings


def create_chunks(text, n, tokenizer):
    tokens = tokenizer.encode(text)
    i = 0
    chunks, chunk_lens = [], []
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and n tokens
        j = min(i + n, len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + n:
            j = min(i + n, len(tokens))

        tokens_sub = tokens[i:j]
        chunks.append(tokens_sub)
        chunk_lens.append(len(tokens_sub))
        i = j

    return chunks, chunk_lens


def get_tokenizer(model=EMBEDDING_MODEL):
    tokenizer = AutoTokenizer.from_pretrained(f"sentence-transformers/{model}")
    return tokenizer
