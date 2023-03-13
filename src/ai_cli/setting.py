import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
setting_file = Path.home() / ".ai_cli.json"


class Setting:
    api_key = None
    endpoint = "https://api.openai.com/v1"
    model = "gpt-3.5-turbo"
    no_stream = False
    raw = False
    log_level = "INFO"
    debug = False
    proxy = None
    multi_line_input = False
    review_prompt = "Please review the above code diff, looking for bugs and potential improvements."
    commit_prompt = "Please generate git commit message for the above code diff."

    def __iter__(self):
        for k in self.__dir__():
            if k.startswith("_"):
                continue
            v = getattr(self, k)
            if callable(v):
                continue
            yield k, getattr(self, k)

    def __dict__(self):
        return {k: v for k, v in self.__iter__()}

    def set(self, k, v):
        if not hasattr(self, k):
            return
        if v is None:
            return
        setattr(self, k, v)

    @classmethod
    def from_dict(cls, d):
        obj = cls()
        for k, v in d.items():
            if not hasattr(obj, k):
                continue
            setattr(obj, k, v)
        return obj


def read_setting() -> Setting:
    if setting_file.exists():
        with setting_file.open() as f:
            return Setting.from_dict(json.load(f))
    return Setting()


setting: Setting = Setting()


if not setting_file.exists():
    setting_file.touch()
    json.dump(dict(setting), setting_file.open("w"))
else:
    setting = read_setting()


def view_setting():
    setting = read_setting()
    if not setting:
        console.print("No setting found")
        return
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="dim")
    table.add_column("Value")

    for k, v in setting:
        table.add_row(k, str(v))
    console.print(table)


def save_setting(setting: Setting):
    with setting_file.open("w") as f:
        json.dump(setting.__dict__(), f)


def set_setting(k, v):
    global setting
    if not hasattr(setting, k):
        console.print(f"Setting {k} not found")
        return
    if isinstance(setting.__dict__()[k], bool) and isinstance(v, str):
        v = v.lower() in ("yes", "true", "t", "1")
    setting.set(k, v)
    save_setting(setting)
