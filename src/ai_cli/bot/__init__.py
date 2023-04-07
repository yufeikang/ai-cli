# abc bot interface
import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Generator, Union
from uuid import uuid4

import openai
from EdgeGPT import Chatbot, ConversationStyle

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

    def __iter__(self):
        return iter(self.history.values())


class Bot(ABC):
    def __init__(self, setting: Setting):
        self.setting = setting
        self.history = ChatHistoryContainer()
        self.stream = not setting.no_stream

    @abstractmethod
    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        pass

    def ask(self, question: str, stream=None) -> Union[str, Generator]:
        stream = self.stream if stream is None else stream
        logger.info(f"Ask: {question} stream: {stream}")
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
    def __init__(self, setting: Setting):
        super().__init__(setting)
        self.model = setting.model

    def get_messages(self):
        for h in self.history:
            yield {"role": "user", "content": h.question}
            if h.answer is not None:
                yield {"role": "assistant", "content": h.answer}

    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        messages = list(self.get_messages())
        try:
            response = openai.ChatCompletion.create(model=self.setting.model, messages=messages, stream=stream)
            if not stream:
                yield response.choices[0].message.content
            else:
                for v in response:
                    if "content" in v.choices[0].delta:
                        yield v.choices[0].delta.content
        except openai.error.RateLimitError:
            logger.warning("[bold red]Rate limit exceeded, sleep for 10 seconds, then retry")
            time.sleep(10)
            return self._ask(question, stream=stream)


class BingBot(Bot):
    def __init__(self, setting: Setting):
        super().__init__(setting)
        self.style = ConversationStyle.creative
        self.history.answer_append = False
        self.bot = Chatbot(cookiePath=setting.bing_cookie)
        logger.info(f"BingBot init, cookie path: {setting.bing_cookie}")

    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        if not stream:
            result = asyncio.run(self.bot.ask(question, conversation_style=self.style))
            logger.debug(f"Answer: {json.dumps(result, ensure_ascii=False)}")
            messages = result.get("item").get("messages")
            yield messages[len(messages) - 1].get("text")
        else:
            gen = self.bot.chat_hub.ask_stream(
                question, conversation_style=self.style, wss_link="wss://sydney.bing.com/sydney/ChatHub"
            )
            for result in self.sync_adapter(gen):
                logger.debug(f"Answer stream: {json.dumps(result, ensure_ascii=False)}")
                if not result[0]:
                    yield result[1]

    def sync_adapter(self, async_generator):
        loop = asyncio.get_event_loop()
        async_gen = async_generator
        try:
            while True:
                next_val = loop.run_until_complete(async_gen.__anext__())
                yield next_val
        except StopAsyncIteration:
            pass


bot = None


def get_bot(setting: Setting, bot_type: str):
    global bot
    if bot is None:
        if bot_type == "BingBot":
            bot = BingBot(setting)
        else:
            bot = GPTBot(setting)
    return bot
