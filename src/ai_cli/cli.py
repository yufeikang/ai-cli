#!/usr/bin/env python3
import argparse
import logging
import os
import subprocess
import sys
import tempfile

from ai_cli import compress_diff_content, git, init_logging
from ai_cli.bot import Bot, get_bot
from ai_cli.setting import set_setting, setting, view_setting

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
    "--bot",
    "-b",
    dest="bot",
    type=str,
    nargs="?",
    choices=["GPTBot", "BingBot", "BardBot"],
    help="the bot to use, defaults to GPTBot, if you want to use Azure openai, you need to set AZURE_OPENAI_ENDPOINT env var",
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
    "-p",
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
    "--prompt",
    "-p",
    dest="prompt",
    type=str,
    nargs="?",
    help="if you want to add a prompt in front of the question."
    " this is useful when you want to ask a question in a specific ."
    " example: curl https://example.com | ai ask --prompt 'please get all the links from '",
)

chat_parser = command_parser.add_parser("chat", help="chat with the assistant")

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

commit_parser = command_parser.add_parser("commit", help="let the assistant help you write a commit message")
commit_parser.add_argument(
    "--message",
    "-m",
    dest="message",
    type=str,
    nargs="?",
    help="the extra message to add to the commit message",
)
commit_parser.add_argument(
    "--user-prompt",
    "-up",
    dest="user_prompt",
    type=str,
    nargs="?",
    help="enable user prompt mode, this will let you input the commit message",
)

args = parser.parse_args()

init_logging(setting.log_level.get_value() if not args.debug else "DEBUG")

logger = logging.getLogger(__name__)


def _print(text, render):
    content = text
    if args.raw or setting.raw.get_value():
        render(content)
        return
    markdown = Markdown(
        content,
        inline_code_lexer="auto",
        inline_code_theme="monokai",
    )
    render(markdown)


def _ask(question, stream=False):
    bot_type = args.bot or setting.bot.get_value()
    bot: Bot = get_bot(setting=setting, bot_type=bot_type, args=args)
    return bot.ask(question, stream=stream)


def ask(question, stream=False):
    content = ""
    if stream:
        with Live("[bold green]Asking...", refresh_per_second=3) as live:
            logger.debug("asking question: %s", question)
            response = _ask(question, stream=stream)
            for content in response:
                _print(content, live.update)
    else:
        with console.status("[bold green]Asking...", spinner="point") as status:
            content = _ask(question, stream=stream)
            _print(content, console.print)
            status.update("[bold green]Done!")
    return content


def chat():
    stream = not args.no_stream
    while True:
        question = get_user_input("You")
        if not question:
            break
        console.print("\n[bold green]Assistant[/bold green]:")
        ask(question, stream)
        console.print("\n")


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
    multi_line_input = setting.multi_line_input.get_value() or args.multi_line_input
    if sys.stdin.isatty():
        if multi_line_input:
            console.print(f"[bold blue]{prompt}:, Ctrl+D end input[/bold blue]")
        else:
            console.print(f"[bold blue]{prompt}:[/bold blue]")
    return "\n".join(sys.stdin.readlines()) if multi_line_input else sys.stdin.readline()


def translate():
    stream = not args.no_stream
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
        text = f"{text} \n\n Please translate the above content from {args.source} to {args.target}"
    else:
        text = f"{text} \n\n Please translate the above content into {args.target}"
    ask(text, stream=stream)


def ask_cmd():
    stream = not args.no_stream
    if not args.question:
        args.question = get_user_input()
    logger.debug("asking question: %s", args.question)
    if isinstance(args.question, list):
        args.question = " ".join(args.question)
    if args.prompt:
        args.question = f"{args.prompt} \n\n {args.question}"
    ask(args.question, stream=stream)


def review_cmd():
    stream = not args.no_stream
    if not git.is_exist_git_repo():
        console.print("[bold red]Not a git repository, please run this command in a git repository")
        exit(0)
    diff_files = git.get_change_files(args.target)
    if not diff_files or len(diff_files) == 0:
        console.print("[bold red]No diff files found")
        exit(0)
    for f in diff_files:
        diff_context = git.get_file_diff(f, args.target)
        diff_context = compress_diff_content(diff_context)
        console.print(f"[bold blue]Reviewing file: {f} :[{len(diff_context)}w][/bold blue]")
        if not diff_context:
            console.print(f"[bold red]No diff found for file: {f}")
            continue
        action = Prompt.ask(
            "[bold blue]Press enter to start, press n to skip[/bold blue]",
            choices=["y", "n"],
            default="y",
            show_choices=False,
        )
        if action == "n":
            continue
        text = f"{diff_context} \n\n {setting.review_prompt.get_value()}"
        ask(text, stream=stream)
    console.print("[bold green]Done![/bold green]")


def set_all_setting():
    for k, v in setting:
        logger.debug(f"setting: {k}={v}")
        default_value = v
        if k in args:
            default_value = default_value or getattr(args, k)
        value = Prompt.ask(f"Please enter a value for {k}", default=default_value)
        set_setting(k, value)


def commit_cmd():
    if not git.is_exist_git_repo():
        console.print("[bold red]Not a git repository, please run this command in a git repository")
        exit(0)
    diff_files = git.get_change_files("HEAD")
    if not diff_files or len(diff_files) == 0:
        console.print("[bold red]No diff files found")
        exit(0)
    console.print(f"[bold blue]Found {len(diff_files)} files changed[/bold blue]")
    diff = git.get_file_diff(diff_files, "HEAD")
    prompt = setting.commit_prompt.get_value()
    if args.user_prompt:
        prompt = f"{prompt} \n\n user ask:{args.user_prompt} \n\n"
    message = f"{prompt} \n\n {diff}"
    result = ask(message, stream=False).strip()
    if args.message:
        result = result + "\n\n" + args.message
    action = Prompt.ask(
        "[bold blue]Do you want to commit these changes?[/bold blue] [(Yes)y/(No)n/(Edit)e]",
        choices=["y", "n", "e"],
        show_choices=False,
    )
    # edit message use vim
    if action == "e":
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(result)
            f.flush()
            subprocess.call(["vim", f.name])
            with open(f.name, "r") as f:
                result = f.read()
        action = Prompt.ask(
            "[bold blue]Do you want to commit these changes?[/bold blue] [(Yes)y/(No)n]",
            choices=["y", "n"],
            show_choices=False,
        )
    if action == "y":
        git.commit(result)


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
    "commit": commit_cmd,
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
