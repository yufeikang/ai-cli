import json
import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from ai_cli import CONFIG_DIR

logger = logging.getLogger("ai_cli")

console = Console()

setting_file = CONFIG_DIR / "setting.json"

# migrate old setting file
old_setting_file = Path.home() / ".ai_cli.json"
if old_setting_file.exists() and not setting_file.exists():
    setting_file.parent.mkdir(parents=True, exist_ok=True)
    old_setting_file.rename(setting_file)


class SettingField:
    def __init__(self, name, required=False, default=None, type=str, value=None, description=None):
        self.name = name
        self.required = required
        self.default = default
        self.type = type
        self.value = value
        self.description = description

    def get_value(self):
        return self.value or self.default

    def set_value(self, value):
        if value is not None:
            if self.type is not None:
                value = self.type(value)
        self.value = value


class Setting:
    api_key = SettingField(
        "OpenAI API Key", description="You can get it from https://platform.openai.com/account/api-keys"
    )
    endpoint = SettingField("OpenAI API Endpoint", description="default is https://api.openai.com")
    model = SettingField("OpenAI API Model", default="gpt-3.5-turbo")
    no_stream = SettingField("Disable stream mode", default=False, type=bool)
    bot = SettingField("Bot Type", default="GPTBot", description="Supported: GPTBot, BingBot, BardBot")
    raw = SettingField("Raw mode", default=False, type=bool, description="no render content by rich")
    log_level = SettingField("Log level", default="INFO")
    debug = SettingField("Debug mode", default=False, type=bool)
    proxy = SettingField("Proxy", default=None)
    multi_line_input = SettingField("Multi line input", default=False, type=bool)
    bing_cookie = SettingField("Bing cookie", default=None)
    max_tokens = SettingField("Max tokens", default=4096, type=int)
    review_prompt = SettingField(
        "Review prompt", default="Please review the above code diff, looking for bugs and potential improvements."
    )
    commit_prompt = SettingField(
        "Commit prompt",
        default="Please generate git commit message for the above code diff from user. The commit message should be in the following format: <type>(<scope>): <subject>",
    )

    def __call__(self):
        return self.__dict__()

    def __iter__(self):
        for k in self.__dir__():
            if k.startswith("_"):
                continue
            v = getattr(self, k)
            if callable(v):
                continue
            yield k, getattr(self, k)

    def __dict__(self):
        return {k: v.get_value() for k, v in self.__iter__()}

    def set(self, k, v):
        if not hasattr(self, k):
            return
        if v in ["None", "none"]:
            v = None
        getattr(self, k).set_value(v)

    @classmethod
    def from_dict(cls, d):
        obj = cls()
        for k, v in d.items():
            if not hasattr(obj, k):
                continue
            getattr(obj, k).set_value(v)
        return obj


def read_setting() -> Setting:
    if setting_file.exists():
        with setting_file.open() as f:
            return Setting.from_dict(json.load(f))
    return Setting()


def save_setting(setting: Setting):
    with setting_file.open("w") as f:
        json.dump(setting.__dict__(), f, ensure_ascii=False, indent=2)


setting: Setting = Setting()


if not setting_file.exists():
    setting_file.touch()
    # save default setting
    logger.info("Save default setting, to %s", setting_file)
    save_setting(setting)
else:
    setting = read_setting()


def view_setting():
    setting = read_setting()
    if not setting:
        console.print("No setting found")
        return
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("key", style="dim")
    table.add_column("name")
    table.add_column("Value")
    table.add_column("Description")

    for k, v in setting:
        table.add_row(k, v.name, str(v.get_value()), v.description)
    console.print(table)


def set_setting(k, v):
    global setting
    if not hasattr(setting, k):
        console.print(f"Setting {k} not found")
        return
    if isinstance(setting.__dict__()[k], bool) and isinstance(v, str):
        v = v.lower() in ("yes", "true", "t", "1")
    setting.set(k, v)
    save_setting(setting)
