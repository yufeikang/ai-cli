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
        self.stream = not setting.no_stream

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
    def __init__(self, setting: Setting):
        super().__init__(setting)
        self.model = setting.model
        self.max_tokens = setting.max_tokens

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
            return self._ask("", stream=stream)


class BingBot(Bot):
    def __init__(self, setting: Setting):
        super().__init__(setting)
        self.style = ConversationStyle.creative
        self.history.answer_append = False
        self.bot = Chatbot(cookiePath=setting.bing_cookie)
        logger.info(f"BingBot init, cookie path: {setting.bing_cookie}")
        self.max_conversation = None
        self.current_conversation = 0
        self.prefix_prompt = None

    def update_conversation(self, response: dict):
        throttling = response.get("item").get("throttling")
        if throttling:
            self.max_conversation = throttling.get("maxNumUserMessagesInConversation")
            self.current_conversation = throttling.get("numUserMessagesInConversation")

    def should_summarize(self) -> bool:
        if self.max_conversation is None:
            return super().should_summarize()
        if self.current_conversation + 1 >= self.max_conversation:
            logger.info(
                f"Conversation count: {self.current_conversation + 1} >= {self.max_conversation}, should summarize"
            )
            return True
        return super().should_summarize()

    def summarize(self):
        # reset conversation
        summary = list(self._ask("", stream=False))[0]
        logger.info(f"Summarize: {summary}")
        self.bot = Chatbot(cookiePath=self.setting.bing_cookie)
        self.prefix_prompt = summary

    def _get_question(self, question: str) -> str:
        if self.prefix_prompt:
            logger.info("Add prefix prompt")
            question = self.prefix_prompt + "\n" + question
            self.prefix_prompt = None
        return question

    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        question = self._get_question(question)
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
                if not result[0]:
                    logger.debug(f"Answer stream: {json.dumps(result, ensure_ascii=False)}")
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
