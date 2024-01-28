import asyncio
import json
import logging
from typing import Generator, Union

from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

from ai_cli.bot import Bot
from ai_cli.setting import Setting

logger = logging.getLogger(__name__)

with open(Setting.bing_cookie.get_value(), "r") as f:
    bing_cookies = json.load(f)


class BingBot(Bot):
    def __init__(self, setting: Setting, *args, **kwargs):
        super().__init__(setting)
        self.style = ConversationStyle.creative
        self.history.answer_append = False
        self.bot = Chatbot(cookies=bing_cookies)
        logger.info(f"BingBot init, cookie path: {setting.bing_cookie.get_value()}")
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
        self.bot = Chatbot(cookies=bing_cookies)
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
