from src.utils.gpt_client import GPTClient
from src.utils.embedding_client import EmbeddingClient

class AIProcessor:
    """
    Facade class that provides a unified interface for both
    GPT completions and embedding generation.
    """
    def __init__(self, base_url, api_key, client):
        self.gpt = GPTClient(base_url, api_key, client)
        self.embedder = EmbeddingClient(base_url, api_key, client)

    def generate_completion(self, *args, **kwargs):
        return self.gpt.generate_response(*args, **kwargs)

    def generate_embeddings(self, *args, **kwargs):
        return self.embedder.get_embeddings(*args, **kwargs)

