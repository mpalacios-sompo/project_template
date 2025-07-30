from typing import Optional
from langchain_openai import AzureOpenAIEmbeddings

class EmbeddingClient:
    def __init__(self, base_url, api_key, client):
        """
        Initializes the EmbeddingClient with Azure OpenAI service details.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.client = client

    def get_embeddings(
        self,
        input_text: str,
        model: str = "text-embedding-3-small",
        dimensions: int = 3072,
        ) -> list[float]:
        """Generates an embedding vector from input text using Azure OpenAI.

        Args:
            input_text (str): Text input to be embedded.
            model (str, optional): Model name to use. Defaults to "text-embedding-3-large".
            dimensions (int, optional): Expected embedding vector length. Defaults to 3072.

        Returns:
            list[float]: The embedding vector.

        Raises:
            ValueError: If input is invalid or output shape/type mismatches.
            RuntimeError: If embedding client initialization or API call fails.
        """
        if not input_text.strip():
            raise ValueError("Input text for embedding cannot be empty.")

        embedding_client = self._get_embedding_client()

        try:
            response = embedding_client.client.create(
                input=input_text,
                model=model,
                dimensions=dimensions,
            )

            embedding = response.data[0].embedding

            if not isinstance(embedding, list) or len(embedding) != dimensions:
                raise ValueError(
                    f"Unexpected embedding format or dimensions: expected {dimensions}, "
                    f"got {len(embedding) if isinstance(embedding, list) else 'invalid type'}"
                )

            if not all(isinstance(x, float) for x in embedding):
                raise ValueError("Embedding vector contains non-float values.")

            return embedding

        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings: {e}") from e
    
    def _get_embedding_client(self) -> AzureOpenAIEmbeddings:
        """Initializes the Azure OpenAI Embeddings client.

        Returns:
            AzureOpenAIEmbeddings: Configured embeddings client.

        Raises:
            RuntimeError: If the client cannot be initialized.
        """
        try:
            return AzureOpenAIEmbeddings(
                azure_endpoint=f"{self.base_url}/embedding-model-orchestrator/api/{self.client}",
                api_key=self.api_key,
                openai_api_version="2025-02-01",
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Azure OpenAI Embedding client: {e}") from e

