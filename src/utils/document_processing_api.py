import requests

class DocumentAPIClient:
    def __init__(self, base_url: str, client: str, api_key: str):
        """
        Initialize the DocumentOperations instance.

        Args:
            base_url (str): Base URL of the API service.
            client (str): Client identifier.
            api_key (str): API key for authentication.
        """
        self.base_url = base_url
        self.client = client
        self.api_key = api_key
        self.headers = {
            "Platform-Api-Version": "2025-02-01",
            "Accept": "application/json",
            "x-api-key": self.api_key,
            }

    def upload_document(self, file_path: str, document_id: str = "", document_part: str = "0", ttl: int = 900) -> str | None:
        """
        Upload a document file to the document management API.

        Args:
            file_path (str): Path to the file to upload.
            document_id (str, optional): Document ID if updating an existing document. Defaults to empty string.
            document_part (str, optional): Document part identifier. Defaults to "0".
            ttl (int, optional): Time to live (in seconds) for the uploaded document. Defaults to 900.

        Returns:
            str | None: The document ID returned by the API if upload is successful; None otherwise.

        Raises:
            FileNotFoundError: If the specified file_path does not exist.
            requests.HTTPError: If the API call fails with a non-success status code.
            requests.ConnectionError: If the network connection fails.
            requests.Timeout: If the request times out.
            ValueError: If the response content is not valid JSON.
        """
        url = f"{self.base_url}/document-management/api/{self.client}/documents"
        data = {
            "documentId": document_id,
            "documentPart": document_part,
            "ttl": str(ttl),
        }

        try:
            with open(file_path, "rb") as file_obj:
                files = {
                    "file1": (file_path.split("/")[-1], file_obj, "application/pdf"),
                }
                response = requests.post(url, headers=self.headers, data=data, files=files)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except requests.ConnectionError as e:
            raise requests.ConnectionError("Connection error while uploading document") from e
        except requests.Timeout as e:
            raise requests.Timeout("Request timed out while uploading document") from e

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error during upload: {e.response.status_code} - {e.response.text}") from e

        try:
            resp_json = response.json()
            return resp_json.get("documentId")
        except ValueError as e:
            raise ValueError("Response content is not valid JSON") from e
        

    def get_document(self, document_id: str) -> bytes:
        """
        Retrieve a document from the document management API.

        Args:
            document_id (str): The ID of the document to retrieve.

        Returns:
            bytes: The raw content of the document.

        Raises:
            requests.HTTPError: If the API call fails with a non-success status code.
            requests.ConnectionError: If the network connection fails.
            requests.Timeout: If the request times out.
            RuntimeError: If the response content cannot be accessed.
        """
        url = f"{self.base_url}/document-management/api/{self.client}/documents/{document_id}"

        try:
            response = requests.get(url, headers=self.headers)
        except requests.ConnectionError as e:
            raise requests.ConnectionError(f"Connection error while retrieving document: {e}") from e
        except requests.Timeout as e:
            raise requests.Timeout(f"Request timed out while retrieving document: {e}") from e

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error during retrieval: {e.response.status_code} - {e.response.text}") from e

        try:
            return response.content
        except Exception as e:
            raise RuntimeError(f"Failed to access response content: {e}") from e
        

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
        threshold: float = 0.3,
        skip: int = 0,
        take: int = 5
    ) -> dict:
        """
        Perform a semantic search on specified documents using vector embeddings.

        Args:
            search_index_name (str): Name of the search index.
            search_index_version (str): Version of the search index.
            embedding_deployment_name (str): Name of the embedding deployment.
            embedding_model (str): Name of the embedding model.
            vector_dimensions (int): Dimension of the embedding vectors.
            query (str): Search query.
            document_ids (list[str]): List of document IDs to search within.
            k_nearest_neighbors (int, optional): Number of nearest neighbors to return. Defaults to 3.
            threshold (float, optional): Similarity threshold. Defaults to 0.3.
            skip (int, optional): Number of results to skip. Defaults to 0.
            take (int, optional): Number of results to return. Defaults to 5.

        Returns:
            dict: Parsed JSON response from the semantic search API.

        Raises:
            requests.HTTPError: If the API call fails with a non-success status code.
            requests.ConnectionError: If the network connection fails.
            requests.Timeout: If the request times out.
            ValueError: If the response content is not valid JSON.
        """
        url = f"{self.base_url}/semantic-search/api/{self.client}/indexes/{search_index_name}/search?indexVersion={search_index_version}"

        headers = {
            **self.headers,
            "Content-Type": "application/json",
        }

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
                    "exhaustive": True,
                    "threshold": threshold,
                },
            },
            "skip": skip,
            "take": take,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
        except requests.ConnectionError as e:
            raise requests.ConnectionError("Connection error during semantic search") from e
        except requests.Timeout as e:
            raise requests.Timeout("Request timed out during semantic search") from e

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(f"HTTP error during semantic search: {e.response.status_code} - {e.response.text}") from e

        try:
            return response.json()
        except ValueError as e:
            raise ValueError("Response content is not valid JSON") from e