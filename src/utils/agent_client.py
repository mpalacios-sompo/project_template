from src.utils.api_client import APIClient

from typing import List, Optional, Dict, Any


class AgentClient:
    """
    Client for managing AI agents and agent groups via the Agent Management API.
    """

    def __init__(self, base_url: str, api_key: str, client: str):
        """
        Initializes the AgentClient.

        Args:
            base_url (str): Base URL of the API.
            api_key (str): API key for authentication.
            client (str): Client identifier.
        """
        self.client = client
        self.api = APIClient(
            base_url,
            headers={
                "Platform-Api-Version": "2025-02-01",
                "Accept": "application/json",
                "x-api-key": api_key,
            },
        )

    #Agent Methods

    def create_agent(
        self,
        agent_name: str,
        description: str,
        instructions: str,
        agent_kind: str,
        prompt_template: str,
        model_deployment_name: str = "gpt-4o-dev-default",
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> dict:
        """
        Create a new agent.

        Args:
            agent_name (str): Name of the agent.
            description (str): Description of the agent.
            instructions (str): Prompt instructions.
            agent_kind (str): Agent type (e.g., "General").
            model_deployment_name (str): Model deployment to use.
            prompt_template (str): Top-level prompt template.
            temperature (float): Model sampling temperature.
            max_tokens (int): Maximum tokens allowed in response.

        Returns:
            dict: API response.
        """

        instructions = instructions + "The user question to process:\n---\n{{payload.userMessage}}\n"
        
        payload = {
            "agentName": agent_name,
            "description": description,
            "instructions": instructions,
            "agentKind": agent_kind,
            "temperature": temperature,
            "maxTokens": max_tokens,
            "modelDeploymentName": model_deployment_name,
            "promptTemplate": prompt_template,
        }
        path = f"/agents/api/{self.client}/agents"
        return self.api.post(path, json=payload)

    def list_agents(self) -> dict:
        """
        List all agents for the client.

        Returns:
            dict: List of agents.
        """
        path = f"/agents/api/{self.client}/agents"
        return self.api.get(path)

    def update_agent(
        self,
        agent_name: str,
        description: str,
        instructions: str,
        agent_kind: str,
        prompt_template: str,
        model_deployment_name: str = "gpt-4o-dev-default",
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> dict:
        """
        Update an existing agent.

        Args:
            agent_name (str): Name of the agent.
            description (str): Updated description.
            instructions (str): Updated instructions.
            agent_kind (str): Agent kind.
            model_deployment_name (str): Deployment name.
            prompt_template (str): Updated prompt template.
            temperature (float): Sampling temperature.
            max_tokens (int): Max response tokens.

        Returns:
            dict: API response.
        """
        payload = {
            "agentName": agent_name,
            "description": description,
            "instructions": instructions,
            "agentKind": agent_kind,
            "temperature": temperature,
            "maxTokens": max_tokens,
            "modelDeploymentName": model_deployment_name,
            "promptTemplate": prompt_template,
        }
        path = f"/agents/api/{self.client}/agents/{agent_name}/{agent_kind}"
        return self.api.patch(path, json=payload)

    def delete_agent(self, agent_name: str, agent_kind: str) -> dict:
        """
        Delete an agent.

        Args:
            agent_name (str): Name of the agent.
            agent_kind (str): Type of agent.

        Returns:
            dict: API response.
        """
        path = f"/agents/api/{self.client}/agents/{agent_name}/{agent_kind}"
        return self.api.delete(path)

    # Agent Group Methods 

    def create_agent_group(
        self,
        agent_group_name: str,
        orchestrator_instruction: str,
        selection_instruction: str,
        result_quality_control_instruction: str,
        agents: List[Dict[str, str]],
        deployment_name: str = "gpt-4o-dev-default",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        max_iterations: int = 3,
        max_history: int = 50
    ) -> dict:
        """
        Create a new agent group.

        Args:
            agent_group_name (str): Name of the group.
            orchestrator_instruction (str): Instruction for orchestrator.
            selection_instruction (str): Agent selection rules.
            result_quality_control_instruction (str): QC rule set.
            agents (List[Dict[str, str]]): List of agents in the group.
            deployment_name (str): Deployment name.
            temperature (float): Sampling temperature.
            max_tokens (int): Max tokens allowed.
            max_iterations (int): Max dialogue iterations.
            max_history (int): Max chat history size.

        Returns:
            dict: API response.
        """
        payload = {
            "agentGroupName": agent_group_name,
            "orchestratorInstruction": orchestrator_instruction,
            "selectionInstruction": selection_instruction,
            "resultQualityControlInstruction": result_quality_control_instruction,
            "maximumNumberOfIteration": max_iterations,
            "maximumNumberOfHistoryItems": max_history,
            "temperature": temperature,
            "maxTokens": max_tokens,
            "deploymentName": deployment_name,
            "agents": agents
        }
        path = f"/agents/api/{self.client}/agent-groups"
        return self.api.post(path, json=payload)
    

    def list_agent_groups(self) -> dict:
        """
        List all agent groups.

        Returns:
            dict: List of agent groups.
        """
        path = f"/agents/api/{self.client}/agent-groups"
        return self.api.get(path)

    def update_agent_group(
        self,
        agent_group_name: str,
        orchestrator_instruction: str,
        selection_instruction: str,
        result_quality_control_instruction: str,
        agents: List[Dict[str, str]],
        deployment_name: str = "gpt-4o-dev-default",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        max_iterations: int = 3,
        max_history: int = 50
    ) -> dict:
        """
        Update an existing agent group.

        Args:
            agent_group_name (str): Name of the group.
            orchestrator_instruction (str): New orchestrator instructions.
            selection_instruction (str): New selection instructions.
            result_quality_control_instruction (str): New QC instructions.
            agents (List[Dict[str, str]]): Updated agent list.
            deployment_name (str): Deployment name.
            temperature (float): Sampling temperature.
            max_tokens (int): Max tokens allowed.
            max_iterations (int): Max dialogue iterations.
            max_history (int): Max chat history size.

        Returns:
            dict: API response.
        """
        payload = {
            "agentGroupName": agent_group_name,
            "orchestratorInstruction": orchestrator_instruction,
            "selectionInstruction": selection_instruction,
            "resultQualityControlInstruction": result_quality_control_instruction,
            "maximumNumberOfIteration": max_iterations,
            "maximumNumberOfHistoryItems": max_history,
            "temperature": temperature,
            "maxTokens": max_tokens,
            "deploymentName": deployment_name,
            "agents": agents
        }
        path = f"/agents/api/{self.client}/agent-groups/{agent_group_name}"
        return self.api.patch(path, json=payload)

    def delete_agent_group(self, agent_group_name: str) -> dict:
        """
        Delete an agent group.

        Args:
            agent_group_name (str): Name of the group to delete.

        Returns:
            dict: API response.
        """
        path = f"/agents/api/{self.client}/agent-groups/{agent_group_name}"
        return self.api.delete(path)

    # Execution

    def execute_agent(
        self,
        handler_name: str,
        user_message: str,
        agent_kind: str,
        user_id: str = "not-authorized"
    ) -> dict:
        """
        Execute a single agent or agent group.

        Args:
            handler_name (str): Name of the handler (agent or group).
            user_id (str): User identifier.
            user_message (str): user request.
            agent_kind (str): Kind of agent

        Returns:
            dict: API response.
        """
        query_payload = {'userMessage': user_message}

        payload = {
            "handlerName": handler_name,
            "userId": user_id,
            "agentKind": agent_kind,
            "QueryPayload": str(query_payload)
        }
        path = f"/agents/api/{self.client}/realtime/execute-agents"
        return self.api.post(path, json=payload)
    