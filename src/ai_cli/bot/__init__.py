# abc bot interface
import logging
import os
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Generator, Union
from uuid import uuid4
import httpx

import openai

from ai_cli.bot.token import get_token_count
from ai_cli.setting import Setting

logger = logging.getLogger(__name__)


class ChatHistory:
    def __init__(self, question: str, answer: str, q_id: str, answer_append: bool = True):
        self.question = question
        self._answer = answer
        self.q_id = q_id
        self.question_time = time.time()
        self.answer_time = None
        if answer is not None:
            self.answer_time = time.time()
        self.answer_append = answer_append

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, answer: str):
        if self._answer is None:
            self._answer = answer
        else:
            if self.answer_append:
                self._answer += answer
            else:
                self._answer = answer
        self.answer_time = time.time()

    def time_cost(self):
        return self.answer_time - self.question_time

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self._answer}\nTime cost: {self.time_cost()}"

    def __repr__(self):
        content = self.question
        if self._answer is not None:
            content += "\n"
            content += self._answer
        return content


class ChatHistoryContainer:
    def __init__(self):
        self.history = OrderedDict()
        self.answer_append = True

    def add_question(self, question: str):
        q_id = str(uuid4())
        self.history[q_id] = ChatHistory(question, None, q_id, self.answer_append)
        return q_id

    def add_answer(self, q_id: str, answer: str):
        self.history[q_id].answer = answer
        return self.history[q_id].answer

    def reset(self):
        self.history = OrderedDict()

    def __iter__(self):
        return iter(self.history.values())

    def __str__(self) -> str:
        return "\n".join([repr(h) for h in self.history.values()])


class Bot(ABC):
    def __init__(self, setting: Setting):
        self.setting = setting
        self.history = ChatHistoryContainer()
        self.stream = not setting.no_stream.get_value()

    @abstractmethod
    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        pass

    def should_summarize(self) -> bool:
        return False

    def summarize(self):
        raise NotImplementedError("summarize method not implemented")

    def ask(self, question: str, stream=None) -> Union[str, Generator]:
        stream = self.stream if stream is None else stream
        logger.info(f"Ask: {question} stream: {stream}")
        if self.should_summarize():
            self.summarize()
        question_id = self.history.add_question(question)
        if not stream:
            answer = self._ask(question, stream=stream)
            if isinstance(answer, Generator):
                answer = list(answer)[0]
            logger.info(f"Answer: {answer}")
            self.history.add_answer(question_id, answer)
            return answer
        else:
            return (self.history.add_answer(question_id, a) for a in self._ask(question, stream=stream))


class GPTBot(Bot):
    def __init__(self, setting: Setting, args=None):
        super().__init__(setting)
        self.init_env(setting, args=args)
        self.model = setting.model.get_value()
        self.max_tokens = setting.max_tokens.get_value()
        init_kwargs = {
            "api_key": self.api_key,
            "base_url": self.api_base,
        }
        client_cls = openai.OpenAI
        if self.proxy:
            http_client = httpx.Client(
                proxies=self.proxy,
                transport=httpx.HTTPTransport(local_address="0.0.0.0"),
            )
            init_kwargs["http_client"] = http_client
        if "azure" in self.api_base or "AZURE_OPENAI_ENDPOINT" in os.environ:
            client_cls = openai.AzureOpenAI
            logger.info("using azure api")
            api_version = os.environ.get("AZURE_API_VERSION", "2023-07-01-preview")
            init_kwargs["api_version"] = api_version
            init_kwargs["azure_endpoint"] = os.environ.get("AZURE_OPENAI_ENDPOINT") or self.api_base
            init_kwargs["azure_ad_token"] = os.environ.get("AZURE_OPENAI_AD_TOKEN") or self.api_key
            init_kwargs["azure_deployment"] = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

        self.client = client_cls(**init_kwargs)

    def init_env(self, setting: Setting, args=None):
        self.api_key = None
        if args.api_key:
            self.api_key = args.api_key
        elif setting.api_key.get_value():
            self.api_key = setting.api_key.get_value()
        elif "OPENAI_API_KEY" in os.environ:
            self.api_key = os.environ["OPENAI_API_KEY"]
        self.api_base = "https://api.openai.com"
        if args.endpoint:
            self.api_base = args.endpoint
        elif setting.endpoint.get_value():
            self.api_base = setting.endpoint.get_value()
        elif "OPENAI_API_BASE" in os.environ:
            self.api_base = os.environ["OPENAI_API_BASE"]
        logger.debug("using endpoint: %s", self.api_base)
        self.proxy = None
        if args.proxy:
            self.proxy = args.proxy
        elif setting.proxy.get_value():
            self.proxy = setting.proxy.get_value()
        elif "HTTP_PROXY" in os.environ:
            self.proxy = os.environ["HTTP_PROXY"]
        elif "HTTPS_PROXY" in os.environ:
            self.proxy = os.environ["HTTPS_PROXY"]
        elif "SOCKS_PROXY" in os.environ:
            self.proxy = os.environ["SOCKS_PROXY"]
        elif "ALL_PROXY" in os.environ:
            self.proxy = os.environ["ALL_PROXY"]
        if self.proxy:
            if self.proxy.startswith("socks"):
                logger.debug("using socks proxy: %s", self.proxy)
                try:
                    import socks
                except ImportError:
                    print("Please install pysocks: pip install pysocks")
                    exit(1)

    def get_messages(self):
        for h in self.history:
            yield {"role": "user", "content": h.question}
            if h.answer is not None:
                yield {"role": "assistant", "content": h.answer}

    def should_summarize(self) -> bool:
        content = str(self.history)
        logger.debug(f"All Content: {content}")
        token_count = get_token_count(content, self.model)
        logger.debug(f"Token count: {token_count}")
        if token_count > self.max_tokens / 2:
            logger.info(f"Token count: {token_count} > {self.max_tokens / 2}, should summarize")
            return True
        return super().should_summarize()

    def summarize(self):
        self.history.add_question("TLDR")
        content = list(self._ask("", stream=False))[0]
        logger.info(f"Summarize: {content}")
        self.history.reset()
        q_id = self.history.add_question("TLDR")
        self.history.add_answer(q_id, content)

    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        messages = list(self.get_messages())
        logger.debug(f"Messages: {messages}, model: {self.model}, stream: {stream}")
        try:
            response = self.client.chat.completions.create(model=self.model, messages=messages, stream=stream)
            if not stream:
                yield response.choices[0].message.content
            else:
                for v in response:
                    if v.choices[0].delta.content:
                        yield v.choices[0].delta.content
        except openai.RateLimitError:
            logger.warning("[bold red]Rate limit exceeded, sleep for 10 seconds, then retry")
            time.sleep(10)
            return self._ask("", stream=stream)


bot = None


def get_bot(setting: Setting, bot_type: str, args=None):
    global bot
    if bot is None:
        if bot_type == "BingBot":
            from .bing import BingBot

            bot = BingBot(setting, args)
        elif bot_type == "BardBot":
            from .bard import BardBot

            bot = BardBot(setting, args)
        else:
            bot = GPTBot(setting, args)
    return bot
