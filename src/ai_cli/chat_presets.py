from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatPreset:
    # Custom prompts to start a chat with
    instruction: str
    name: str
    role: str

    model: Optional[str] = None  # use setting default
    stream: bool = True
    no_markdown: bool = False
    temperature: float = 1

    def to_json(self) -> dict:
        return {"role": self.role, "content": self.instruction}

    def format_response(self, inputstr) -> str:
        return inputstr


@dataclass
class Presets:
    """
    TODO: check out https://www.jailbreakchat.com/

    """

    models = {
        "unix": ChatPreset(
            name="unix",
            role="system",
            stream=False,
            no_markdown=True,
            temperature=0.15,
            instruction=f"""
            I want you to act as an experienced devops engineer, software engineer, and unix expert. You are an expert in devops, systems design, unix, linux, vim, shell scripts, python, and more.
            I will ask you to write unix commands and code snippets for me.
            I want you to only reply with the terminal command or code, and nothing else. Do not use markdown. Do not write explanations. Your response should be executable verbatim.
            """,
        ),
    }

    def get_preset(self, preset: str) -> Optional[ChatPreset]:
        return self.models.get(preset)
