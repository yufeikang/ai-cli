import logging
import os
from typing import Generator, Union

import google.generativeai as genai
from google.generativeai import GenerativeModel

from ai_cli.bot import Bot
from ai_cli.setting import Setting

logger = logging.getLogger(__name__)


class GeminiBot(Bot):
    def __init__(self, setting: Setting, args, **kwargs):
        super().__init__(setting, args, **kwargs)
        logger.info(f"Init GeminiBot with setting: {setting}")
        api_key = setting.google_api_key.get_value() or os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = args.model or setting.model.get_value() or "gemini-1.5-pro-latest"
        if self.model not in self.available_models:
            raise ValueError(f"Model {self.model} is not supported. Supported models: {self.available_models}")
        self.bot: GenerativeModel = genai.GenerativeModel(model_name=self.model)

    @property
    def available_models(self):
        return ["gemini-1.5-pro-latest", "gemini-1.0-pro", "gemini-pro"]

    def get_messages(self):
        prompt_added = False
        for m in self.history:
            parts = []
            if prompt_added is False and self.prompt:
                parts.append(self.prompt)
                prompt_added = True
            parts.append(m.question)
            yield {"role": "user", "parts": parts}
            if m.answer is not None:
                yield {"role": "model", "parts": [m.answer]}

    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        messages = self.get_messages()
        logger.debug(f"Ask: {self.model} with stream: {stream}")
        try:
            response = self.bot.generate_content(
                messages,
                stream=stream,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=self.setting.max_tokens.get_value() or 2048,
                    temperature=self.setting.temperature.get_value() or 0.7,
                ),
            )
            if not stream:
                yield response.text
            else:
                for chunk in response:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Ask failed: {e}")
            raise e
