from typing import Optional, Type, Union
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureOpenAIEmbeddings

class GPTClient:
    def __init__(self, base_url, api_key, client):
        """
        Initializes the GPTClient with Azure OpenAI service details.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.client = client

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        deployment_name: str = "gpt-4o-dev-default",
        model: str = "gpt-4",
        temperature: float = 0,
        max_tokens: Optional[int] = None,
        pydantic_schema: Optional[Type] = None,
    ) -> Union[dict, str]:
        """
        Generate a completion from the GPT model with optional structured output parsing.

        Args:
            system_prompt (str): The system-level prompt context.
            user_prompt (str): The user input prompt.
            deployment_name (str, optional): Azure deployment name. Defaults to "gpt-4o-dev-default".
            model (str, optional): Model name. Defaults to "gpt-4".
            temperature (float, optional): Sampling temperature. Defaults to 0.
            max_tokens (int | None, optional): Max tokens for response. Defaults to None.
            pydantic_schema (Type | None, optional): Pydantic model class for structured output parsing. Defaults to None.

        Returns:
            dict or str: Parsed output as dict if pydantic_schema provided, else raw string response.

        Raises:
            ValueError: If system_prompt or user_prompt is empty.
            RuntimeError: For client initialization or model invocation failures.
        """
        if not system_prompt.strip():
            raise ValueError("system_prompt cannot be empty.")
        if not user_prompt.strip():
            raise ValueError("user_prompt cannot be empty.")

        llm = self._get_llm_client(deployment_name, model, temperature, max_tokens)
        prompt = self._build_prompt(pydantic_schema)

        try:
            if pydantic_schema:
                parser = PydanticOutputParser(pydantic_object=pydantic_schema)
                chain = prompt | llm | parser
            else:
                chain = prompt | llm

            response = chain.invoke({"system_prompt": system_prompt, "user_input": user_prompt})

            return response.dict() if pydantic_schema else response

        except Exception as e:
            raise RuntimeError(f"Model invocation failed: {e}") from e
        

    def _build_prompt(self, pydantic_schema: Optional[Type]) -> ChatPromptTemplate:
        """
        Build the chat prompt template, optionally including Pydantic output format instructions.

        Args:
            pydantic_schema (Type | None): Pydantic schema class for output parsing.

        Returns:
            ChatPromptTemplate: The prompt template configured accordingly.

        Raises:
            RuntimeError: If prompt template creation fails.
        """
        try:
            if pydantic_schema:
                parser = PydanticOutputParser(pydantic_object=pydantic_schema)
                return ChatPromptTemplate.from_messages(
                    [
                        ("system", "{system_prompt}\n{format_instructions}"),
                        ("human", "{user_input}"),
                    ]
                ).partial(format_instructions=parser.get_format_instructions())

            return ChatPromptTemplate.from_messages(
                [
                    ("system", "{system_prompt}"),
                    ("human", "{user_input}"),
                ]
            )

        except Exception as e:
            raise RuntimeError(f"Failed to build prompt template: {e}") from e

    def _get_llm_client(
        self,
        deployment_name: str,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
    ) -> AzureChatOpenAI:
        """
        Initialize the AzureChatOpenAI client with specified parameters.

        Args:
            deployment_name (str): The Azure deployment name.
            model (str): The model name.
            temperature (float): Sampling temperature.
            max_tokens (int | None): Maximum tokens for the response.

        Returns:
            AzureChatOpenAI: Initialized LLM client.

        Raises:
            RuntimeError: If client initialization fails.
        """
        try:
            return AzureChatOpenAI(
                azure_deployment=deployment_name,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=None,
                max_retries=2,
                azure_endpoint=f"{self.base_url}/model-orchestrator/api/{self.client}",
                api_key=self.api_key,
                openai_api_version="1",
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AzureChatOpenAI client: {e}") from e
