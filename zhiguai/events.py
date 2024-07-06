from typing import Tuple

from .models import ChatMessage, ChatModel, CriticModel


class NPC(object):

    def __init__(
        self,
        role: str,
        name: str,
        appearance: str,
        voice: str,
        backstory: str,
        relationships: str,
        response: str,
        memory: list,
        action: str,
        action_space: list,
        chat_model: ChatModel,
        chat_prompt: str,
        critic_model: CriticModel,
        critic_prompt: str,
        observation: str,
    ) -> None:
        # TODO: Implement memory
        if memory:
            raise NotImplementedError
        self.role = role
        self.name = name
        self.appearance = appearance
        self.voice = voice
        self.backstory = backstory
        self.relationships = relationships
        self.chat_model = chat_model
        self.chat_prompt = chat_prompt
        self.critic_model = critic_model
        self.critic_prompt = critic_prompt
        self.observation = observation
        self.response = response
        self.action = action
        self.action_space = action_space
        self.memory = memory

    def responde(
        self,
        query: str = "",
        history: list = [],
        retry: int = 3,
    ) -> Tuple[str, list]:
        # TODO: Implement retry
        if self.memory:
            message = ChatMessage(
                role="user",
                content=query,
            )
        else:
            message = ChatMessage(
                role="user",
                content=self.chat_prompt.format(
                    role=self.role,
                    name=self.name,
                    appearance=self.appearance,
                    backstory=self.backstory,
                    # TODO: Implement relationships
                    # relationships=self.relationships,
                    observation=self.observation,
                ),
            )
            query = "【咚咚咚】"
        self.memory.append(message)
        self.response = self.chat_model.generate(self.memory)
        history.append((query, self.response))
        message = ChatMessage(
            role="assistant",
            content=self.response,
        )
        self.memory.append(message)
        return self.response, history

    def react(self, retry: int = 3) -> str:
        count = 0
        # TODO: Improve retry
        while self.action not in self.action_space:
            if count > retry:
                raise RuntimeError("action not found")
            self.action = self.critic_model.generate(
                self.critic_prompt.format(message=self.response),
            )
            count += 1
        return self.action

    def refresh(self):
        self.memory = []


class Event(object):

    def __init__(self, npc: NPC, state: str) -> None:
        self.npc = npc
        self.state = state

    def end(self) -> None:
        return
