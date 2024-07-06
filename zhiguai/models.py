from sparkai.core.messages import ChatMessage
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler


class Config(object):

    def __init__(
        self,
        app_id: str,
        api_secret: str,
        api_key: str,
        api_url: str = "wss://spark-api.xf-yun.com/v3.5/",
        llm_domain: str = "generalv3.5",
    ) -> None:
        self.app_id = app_id
        self.api_secret = api_secret
        self.api_key = api_key
        self.api_url = api_url
        self.llm_domain = llm_domain


class ChatModel(object):

    def __init__(
        self,
        config: Config,
        stream: bool = False,
        timeout: int = 30,
        temperature: float = 0.5,
        top_k: int = 4,
        max_tokens: int = 4096,
    ) -> None:
        # TODO: Implement streaming
        if stream:
            raise NotImplementedError
        self.llm = ChatSparkLLM(
            spark_app_id=config.app_id,
            spark_api_secret=config.api_secret,
            spark_api_key=config.api_key,
            spark_api_url=config.api_url,
            spark_llm_domain=config.llm_domain,
            streaming=stream,
            request_timeout=timeout,
            temperature=temperature,
            top_k=top_k,
            max_tokens=max_tokens,
        )

    # TODO: Handle timeout
    def generate(self, messages: list) -> str:
        handler = ChunkPrintHandler()
        r = self.llm.generate([messages], callbacks=[handler])
        return r.generations[0][0].text


class CriticModel(object):

    def __init__(
        self,
        config: Config,
        stream: bool = False,
        timeout: int = 30,
        temperature: float = 0.5,
        top_k: int = 4,
        max_tokens: int = 4096,
    ) -> None:
        # TODO: Implement streaming
        if stream:
            raise NotImplementedError
        self.llm = ChatSparkLLM(
            spark_app_id=config.app_id,
            spark_api_secret=config.api_secret,
            spark_api_key=config.api_key,
            spark_api_url=config.api_url,
            spark_llm_domain=config.llm_domain,
            streaming=stream,
            request_timeout=timeout,
            temperature=temperature,
            top_k=top_k,
            max_tokens=max_tokens,
        )

    # TODO: Handle timeout
    def generate(self, prompt: str) -> str:
        messages = [
            ChatMessage(
                role="user",
                content=prompt,
            )
        ]
        handler = ChunkPrintHandler()
        r = self.llm.generate([messages], callbacks=[handler])
        return r.generations[0][0].text
