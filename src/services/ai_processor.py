from src.utils.gpt_client import GPTClient
from src.utils.embedding_client import EmbeddingClient
from src.utils.agent_client import AgentClient

class AIProcessor:
    """
    Facade class that provides a unified interface for completions,
    embeddings, and agent/agent group operations.
    """
    def __init__(self, base_url, api_key, client):
        self.gpt = GPTClient(base_url, api_key, client)
        self.embedder = EmbeddingClient(base_url, api_key, client)
        self.agent = AgentClient(base_url, api_key, client)

    # GPT completions
    def generate_completion(self, system_prompt, user_prompt, *args, **kwargs):
        return self.gpt.generate_response(system_prompt, user_prompt, *args, **kwargs)

    # Embeddings
    def generate_embeddings(self, input_text, *args, **kwargs):
        return self.embedder.get_embeddings(input_text, *args, **kwargs)

    # Agent methods
    def list_agents(self):
        return self.agent.list_agents()
    
    def create_agent(self, agent_name, description, instructions, agent_kind, prompt_template, *args, **kwargs):
        return self.agent.create_agent(agent_name, description, instructions, agent_kind, prompt_template, *args, **kwargs)
    
    def delete_agent(self, agent_name, agent_kind, *args, **kwargs):
        return self.agent.delete_agent(agent_name, agent_kind, *args, **kwargs)
    
    def list_agent_groups(self):
        return self.agent.list_agent_groups()
    
    def create_agent_group(self, agent_group_name, orchestrator_instruction, selection_instruction, result_quality_control_instruction, agents, *args, **kwargs):
        return self.agent.create_agent_group(agent_group_name, orchestrator_instruction, selection_instruction, result_quality_control_instruction, agents, *args, **kwargs)
    
    def delete_agent_group(self, agent_group_name, *args, **kwargs):
        return self.agent.delete_agent_group(agent_group_name, *args, **kwargs)
    
    def execute_agent(self, agent_name, user_message, agent_kind, *args, **kwargs):
        return self.agent.execute_agent(agent_name, user_message, agent_kind, *args, **kwargs)