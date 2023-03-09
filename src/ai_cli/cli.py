#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time
from typing import Optional

from ai_cli import git
from ai_cli.setting import set_setting, setting, view_setting
from ai_cli.chat_presets import Presets, ChatPreset

try:
    import openai
except ImportError:
    print("Please install openai: pip install openai")
    exit(1)
try:
    from rich.console import Console
    from rich.live import Live
    from rich.markdown import Markdown
    from rich.prompt import Prompt
except ImportError:
    print("Please install rich: pip install rich")
    exit(1)


def get_os_language():
    if "LANG" in os.environ:
        return os.environ["LANG"].split("_")[0]
    return "en"


console = Console()

parser = argparse.ArgumentParser(description="chatGPT cli. ")

parser.add_argument(
    "--api-key",
    dest="api_key",
    type=str,
    nargs="?",
    help="the API key to use, defaults to OPENAI_API_KEY env var, or asks you to enter it",
)
parser.add_argument(
    "--no-stream",
    "-ns",
    dest="no_stream",
    action="store_true",
    default=False,
    help="non stream the response, default is to live stream the response",
)
parser.add_argument(
    "--raw",
    "--no-markdown",
    dest="raw",
    action="store_true",
    default=False,
    help="default the content will be rendered as markdown, this will disable that",
)
parser.add_argument(
    "--model",
    "-m",
    dest="model",
    type=str,
    nargs="?",
    default="gpt-3.5-turbo",
    help="the model to use",
)
parser.add_argument(
    "--log-level",
    "-l",
    dest="log_level",
    type=str,
    nargs="?",
    default="INFO",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    help="the log level to use, defaults to INFO",
)
parser.add_argument(
    "--debug",
    "-d",
    dest="debug",
    action="store_true",
    default=False,
    help="enable debug mode, this will print the request and response to the console",
)
parser.add_argument(
    "--multi-line",
    "-ml",
    dest="multi_line_input",
    action="store_true",
    default=False,
    help="enable multi line mode, this will enable multi line input, when enabled, you can end the input with Ctrl+D",
)

parser.add_argument(
    "--endpoint",
    "-e",
    dest="endpoint",
    type=str,
    nargs="?",
    help="the endpoint to use, default is https://api.openai.com/v1. You can use this to"
    " resolve the issue of the api endpoint is blocked in your country. OPENAI_API_BASE"
    " env var will also work.",
)

parser.add_argument(
    "--proxy",
    "-z",
    dest="proxy",
    type=str,
    nargs="?",
    help="the proxy to use, if env var HTTP_PROXY/HTTPS+PROXY/SOCKS_PROXY/ALL_PROXY is set,"
    " this will default to that. When use socks proxy. you need install pysocks first. pip install pysocks",
)


command_parser = parser.add_subparsers(dest="command", help="command to run")

ask_parser = command_parser.add_parser("ask", help="ask a question")
ask_parser.add_argument("question", type=str, nargs="*", help="the question to ask")
ask_parser.add_argument(
    "--preset",
    "-p",
    help="Your custom Chat preset name to use",
)


unix_parser = command_parser.add_parser("unix", help="generate a script or command")
unix_parser.add_argument("question", type=str, nargs="*", help="the question to ask")

chat_parser = command_parser.add_parser("chat", help="chat with the assistant")
chat_parser.add_argument(
    "--preset",
    "-p",
    help="Your custom Chat preset name to use",
)

translate_parser = command_parser.add_parser("translate", help="translate a text")
translate_parser.add_argument("text", type=str, nargs="*", help="the text to translate")
translate_parser.add_argument(
    "--source",
    "-s",
    dest="source",
    type=str,
    nargs="?",
    help="the source language, defaults to auto detect",
)
translate_parser.add_argument(
    "--target",
    "-t",
    dest="target",
    type=str,
    nargs="?",
    default=get_os_language(),
    help="the target language, defaults to your OS language",
)
translate_parser.add_argument(
    "--clipboard",
    "-c",
    dest="clipboard",
    action="store_true",
    default=False,
    help="get the text to translate from clipboard",
)
translate_parser.add_argument(
    "--file",
    "-f",
    dest="file",
    type=str,
    nargs="?",
    help="get the text to translate from a file",
)

setting_parser = command_parser.add_parser(
    "setting", help="view/edit the setting, the setting will be saved in ~/.ai_cli.json"
)
setting_parser.add_argument(
    "--edit",
    "-e",
    dest="edit",
    type=str,
    nargs="*",
    help="edit the setting, example: --edit api_key=xxx proxy=xxx",
)
review_parser = command_parser.add_parser("review", help="let the assistant review your code")
review_parser.add_argument(
    "--target",
    "-t",
    dest="target",
    type=str,
    nargs="?",
    default="HEAD",
    help="the target branch/version to compare with, example: master, develop, v1.0.0, a2c3d4e, HEAD",
)


args = parser.parse_args()

logger = logging.getLogger("cli")

if args.debug or setting.debug:
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel("DEBUG")
    logger.debug("debug mode enabled")
else:
    logging.basicConfig()
    logger.setLevel(args.log_level)

if args.api_key:
    openai.api_key = args.api_key
elif setting.api_key:
    openai.api_key = setting.api_key
elif "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]

proxy = None
if args.proxy:
    proxy = args.proxy
elif setting.proxy:
    proxy = setting.proxy
elif "HTTP_PROXY" in os.environ:
    proxy = os.environ["HTTP_PROXY"]
elif "HTTPS_PROXY" in os.environ:
    proxy = os.environ["HTTPS_PROXY"]
elif "SOCKS_PROXY" in os.environ:
    proxy = os.environ["SOCKS_PROXY"]
elif "ALL_PROXY" in os.environ:
    proxy = os.environ["ALL_PROXY"]


if proxy:
    openai.proxy = proxy
    if proxy.startswith("socks"):
        logger.debug("using socks proxy: %s", proxy)
        try:
            import socks
        except ImportError:
            print("Please install pysocks: pip install pysocks")
            exit(1)

if args.endpoint:
    openai.api_base = args.endpoint
elif setting.endpoint:
    openai.api_base = setting.endpoint
elif "OPENAI_API_BASE" in os.environ:
    openai.api_base = os.environ["OPENAI_API_BASE"]

logger.debug("using endpoint: %s", openai.api_base)


def _print(text, render):
    preset = args.preset
    if preset and Presets().get_preset(preset).no_markdown:
        text = text.replace("`", "")

    content = text
    if args.raw or setting.raw:
        render(content)
        return
    markdown = Markdown(
        content,
        inline_code_lexer="auto",
        inline_code_theme="monokai",
    )
    render(markdown)


def _ask(question, preset: Optional[ChatPreset] = None):
    if not openai.api_key:
        openai.api_key = Prompt.ask("OpenAI API Key", password=True)
        setting.api_key = openai.api_key
        set_setting("api_key", openai.api_key)
    messages = []
    if isinstance(question, list):
        messages = question
    else:
        messages = [{"role": "user", "content": question}]
    try:
        return openai.ChatCompletion.create(
            model=(preset and preset.model) or setting.model or args.model,
            messages=messages,
            stream=(preset and preset.stream) or True,
            temperature=(preset and preset.temperature) or 1,
        )
    except openai.error.RateLimitError:
        logger.warn("rate limit exceeded, sleep for 5 seconds, then retry")
        time.sleep(5)
        return _ask(question, preset)


def ask(question, preset: Optional[ChatPreset] = None):
    content = ""
    stream: bool = preset and preset.stream or True
    if stream:
        with Live("[bold green]Asking...", refresh_per_second=3) as live:
            logger.debug("asking question: %s", question)
            response = _ask(question, preset)
            for v in response:
                if v.choices and "content" in v.choices[0].delta and v.choices[0].delta.content:
                    content += v.choices[0].delta.content
                    _print(content, live.update)
    else:
        with console.status("[bold green]Asking...", spinner="point") as status:
            response = _ask(question, preset)
            logger.info("!")
            logger.info(response)
            content = response.choices[0].message.content
            _print(content, console.print)
            status.update("[bold green]Done!")
    return content


def chat():
    preset = args.preset
    preset_model = None
    if preset:
        preset_model = Presets().get_preset(preset)
        console.print(f"\nStarting with preset [bold blue]'{preset}'[/bold blue]:")
        messages = [Presets().get_preset(preset).to_json()]

    else:
        messages = []
    while True:
        question = get_user_input("You")
        if not question:
            break
        messages.append({"role": "user", "content": question})
        console.print("\n[bold green]Assistant[/bold green]:")
        answer = ask(messages, preset_model)
        console.print("\n")
        messages.append({"role": "assistant", "content": answer})


def _get_text_from_clipboard():
    try:
        import pyperclip

        return pyperclip.paste()
    except ImportError:
        logger.error("pyperclip is not installed, please install it use: pip install pyperclip")
        exit(0)
    except Exception as e:
        logger.error("error getting text from clipboard: %s", e)
        return None


def _get_text_from_file():
    try:
        with open(args.file, "r") as f:
            return f.read()
    except Exception as e:
        logger.error("error getting text from file: %s", e)
        return None


def get_user_input(prompt="Please enter a question"):
    logger.debug("reading question from stdin")
    multi_line_input = setting.multi_line_input or args.multi_line_input
    if sys.stdin.isatty():
        if multi_line_input:
            console.print(f"[bold blue]{prompt}:, Ctrl+D end input[/bold blue]")
        else:
            console.print(f"[bold blue]{prompt}:[/bold blue]")
    return "\n".join(sys.stdin.readlines()) if multi_line_input else sys.stdin.readline()


def translate():
    text = args.text
    if args.file:
        text = _get_text_from_file()
    elif args.clipboard:
        text = _get_text_from_clipboard()
    if not text:
        text = get_user_input("Please enter a text to translate")
    if isinstance(text, list):
        text = " ".join(text)
    logger.debug("translating text: %s", text)
    if args.source:
        question = f"{text} \n\n Please translate the above content from {args.source} to {args.target}"
    else:
        question = f"{text} \n\n Please translate the above content into {args.target}"

    ask(question)


def ask_cmd():
    preset = args.preset
    messages = []
    preset_model = None
    if preset:
        preset_model = Presets().get_preset(preset)
        messages = [preset_model.to_json()]
        args.no_stream = preset_model.stream
        args.raw = preset_model.no_markdown

    if not args.question:
        args.question = get_user_input()
    logger.debug("asking question: %s", args.question)
    if isinstance(args.question, list):
        args.question = " ".join(args.question)
    messages.append({"role": "user", "content": args.question})

    ask(messages, preset_model)


def review_cmd():
    if not git.is_exist_git_repo(os.getcwd()):
        console.print("[bold red]Not a git repository, please run this command in a git repository")
        exit(0)
    diff_files = git.get_change_files(args.target)
    if not diff_files or len(diff_files) == 0:
        console.print("[bold red]No diff files found")
        exit(0)
    for f in diff_files:
        console.print(f"[bold blue]Reviewing file: {f}[/bold blue]")
        diff_context = git.get_file_diff(f, args.target)
        if not diff_context:
            console.print(f"[bold red]No diff found for file: {f}")
            continue
        text = f"{diff_context} \n\n {setting.review_prompt}"
        ask(text)
        Prompt.ask("[bold blue]Press enter to continue[/bold blue]")
    console.print("[bold green]Done![/bold green]")


def set_all_setting():
    for k, v in setting:
        logger.debug(f"setting: {k}={v}")
        default_value = v
        if k in args:
            default_value = default_value or getattr(args, k)
        value = Prompt.ask(f"Please enter a value for {k}", default=default_value)
        set_setting(k, value)


def setting_cmd():
    if args.edit is not None:
        if len(args.edit) == 0:
            set_all_setting()
        else:
            for s in args.edit:
                split = s.split("=")
                if len(split) != 2:
                    console.print(f"[bold red]Invalid setting: {s}, please use key=value format")
                    exit(0)
                set_setting(split[0], split[1])
                console.print("[bold green]Setting saved!")
    view_setting()


CMD = {
    "ask": ask_cmd,
    "chat": chat,
    "translate": translate,
    "review": review_cmd,
    "setting": setting_cmd,
    "help": parser.print_help,
}


def main():
    command = args.command
    logger.debug(f"command: {command}")
    if command in CMD:
        CMD[command]()
    else:
        parser.print_help()


def cli():
    try:
        logger.debug(f"args: {args}")
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
        exit(0)


if __name__ == "__main__":
    cli()
