from typing import Optional
from src.utils.api_client import APIClient  

class DocumentAPIClient:
    """
    Client for document management and semantic search API operations.
    """

    def __init__(self, base_url: str, client: str, api_key: str):
        """
        Initialize the DocumentAPIClient.

        Args:
            base_url (str): Base URL of the API.
            client (str): Client identifier.
            api_key (str): API key for authentication.
        """
        self.client = client
        headers = {
            "Platform-Api-Version": "2025-02-01",
            "Accept": "application/json",
            "x-api-key": api_key,
        }
        self.api = APIClient(base_url, headers)

    def upload_document(self, file_path: str, document_id: str = "", document_part: str = "0", ttl: int = 900) -> Optional[str]:
        """
        Upload a PDF document.

        Args:
            file_path (str): Path to the file.
            document_id (str): Optional document ID.
            document_part (str): Part identifier.
            ttl (int): Time-to-live in seconds.

        Returns:
            Optional[str]: Document ID if successful.
        """
        path = f"/document-management/api/{self.client}/documents"
        data = {
            "documentId": document_id,
            "documentPart": document_part,
            "ttl": str(ttl),
        }

        try:
            with open(file_path, "rb") as f:
                files = {"file1": (file_path.split("/")[-1], f, "application/pdf")}
                response = self.api.post(path, data=data, files=files)
                return response.get("documentId")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def get_document(self, document_id: str) -> bytes:
        """
        Retrieve a document by ID.

        Args:
            document_id (str): The document ID.

        Returns:
            bytes: Binary content of the document.
        """
        path = f"/document-management/api/{self.client}/documents/{document_id}"
        return self.api.get(path)

    def semantic_search(
        self,
        query: str,
        document_ids: list[str],
        search_index_name: str = "default_semantic_search_index",
        search_index_version: int = 3,
        embedding_deployment_name: str = "text-embedding-3-large-dev-shared",
        embedding_model: str = "text-embedding-3-large",
        vector_dimensions: int = 3072,
        k_nearest_neighbors: int = 3,
        exhaustive: bool = True,
        threshold: float = 0.3,
        skip: int = 0,
        take: int = 5
    ) -> dict:
        """
        Perform semantic search on a list of documents using vector similarity.

        Args:
            query (str): The query string.
            document_ids (list[str]): List of document IDs to search within.
            search_index_name (str, optional): Name of the search index. Defaults to 'default_semantic_search_index'.
            search_index_version (int, optional): Version of the search index. Defaults to 3.
            embedding_deployment_name (str, optional): Embedding deployment name. Defaults to 'text-embedding-3-large-dev-shared'.
            embedding_model (str, optional): Embedding model name. Defaults to 'text-embedding-3-large'.
            vector_dimensions (int, optional): Number of embedding dimensions. Defaults to 3072.
            k_nearest_neighbors (int, optional): Number of nearest neighbors to return. Defaults to 3.
            exhaustive (bool, optional): Whether to use exhaustive search. Defaults to True.
            threshold (float, optional): Minimum similarity threshold. Defaults to 0.3.
            skip (int, optional): Number of results to skip. Defaults to 0.
            take (int, optional): Number of results to return. Defaults to 5.

        Returns:
            dict: Parsed response from the semantic search API.
        """
        path = (
            f"/semantic-search/api/{self.client}/indexes/{search_index_name}/search"
            f"?indexVersion={search_index_version}"
        )

        payload = {
            "documentIds": document_ids,
            "query": query,
            "embeddingDeploymentName": embedding_deployment_name,
            "embeddingModel": embedding_model,
            "vectorDimensions": vector_dimensions,
            "searchParams": {
                "type": "RegularSearchParameters",
                "contentVectorSearchParams": {
                    "kNearestNeighborsCount": k_nearest_neighbors,
                    "exhaustive": exhaustive,
                    "threshold": threshold,
                },
            },
            "skip": skip,
            "take": take,
        }

        return self.api.post(path, json=payload)
