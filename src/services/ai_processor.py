from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


class AIprocessor:
    def __init__(self, base_url: str, api_key: str, deployment_name: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.model = model

    def gpt_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0,
        max_tokens: int | None = None,
        pydantic_schema: type | None = None
    ):
        if not system_prompt.strip():
            raise ValueError("system_prompt cannot be empty.")
        if not user_prompt.strip():
            raise ValueError("user_prompt cannot be empty.")

        try:
            llm = self._get_llm_client(temperature, max_tokens)
        except Exception as e:
            raise RuntimeError(f"LLM client initialization failed: {e}") from e

        prompt = self._build_prompt(pydantic_schema)

        try:
            if pydantic_schema:
                parser = PydanticOutputParser(pydantic_object=pydantic_schema)
                chain = prompt | llm | parser
            else:
                chain = prompt | llm

            response = chain.invoke({"system_prompt": system_prompt, "user_input": user_prompt})

            if pydantic_schema:
                return response.dict()
            else:
                return response

        except Exception as e:
            # Catch API/network/parsing errors
            raise RuntimeError(f"Model invocation failed: {e}") from e

    def _build_prompt(self, pydantic_schema: type | None) -> ChatPromptTemplate:
        try:
            if pydantic_schema:
                parser = PydanticOutputParser(pydantic_object=pydantic_schema)
                return ChatPromptTemplate.from_messages(
                    [
                        ("system", "{system_prompt}\n{format_instructions}"),
                        ("human", "{user_input}"),
                    ]
                ).partial(format_instructions=parser.get_format_instructions())
            else:
                return ChatPromptTemplate.from_messages(
                    [
                        ("system", "{system_prompt}"),
                        ("human", "{user_input}"),
                    ]
                )
        except Exception as e:
            raise RuntimeError(f"Failed to build prompt template: {e}") from e

    def _get_llm_client(self, temperature: float, max_tokens: int | None):
        try:
            return AzureChatOpenAI(
                azure_deployment=self.deployment_name,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=None,
                max_retries=2,
                azure_endpoint=self.base_url,
                api_key=self.api_key,
                openai_api_version="1",
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AzureChatOpenAI client: {e}") from e
