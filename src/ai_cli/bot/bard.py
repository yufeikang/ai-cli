from bardapi import Bard

import os, sys
import logging


from ai_cli.bot import Bot
from ai_cli.setting import Setting

from typing import Generator, Union

logger = logging.getLogger(__name__)


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class BardBot(Bot):
    def __init__(self, setting: Setting, *args, **kwargs):
        super().__init__(setting)

        # bard-api will print the cookies to stdout and it can't be disabled otherwise
        with HiddenPrints():
            self.bard = Bard(token_from_browser=True)

    def _ask(self, question: str, stream=None) -> Union[str, Generator]:
        answer = self.bard.get_answer(question)
        yield answer["content"]
