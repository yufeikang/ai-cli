#!/usr/bin/env python3
import argparse
import logging
import os

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
    "--proxy",
    "-p",
    dest="proxy",
    type=str,
    nargs="?",
    help="the proxy to use, if env var HTTP_PROXY/HTTPS+PROXY/SOCKS_PROXY/ALL_PROXY is set, this will default to that. When use socks proxy. you need install pysocks first. pip install pysocks",
)

command_parser = parser.add_subparsers(dest="command", help="command to run")

ask_parser = command_parser.add_parser("ask", help="ask a question")
ask_parser.add_argument("question", type=str, nargs="*", help="the question to ask")

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

args = parser.parse_args()
logging.basicConfig()
logger = logging.getLogger("cli")
logger.setLevel(args.log_level)

if args.api_key:
    openai.api_key = args.api_key
elif "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]
else:
    openai.api_key = Prompt.ask("OpenAI API Key", password=True)

proxy = None
if args.proxy:
    proxy = args.proxy
elif "HTTP_PROXY" in os.environ:
    proxy = os.environ["HTTP_PROXY"]
elif "HTTPS_PROXY" in os.environ:
    proxy = os.environ["HTTPS_PROXY"]
elif "SOCKS_PROXY" in os.environ:
    proxy = os.environ["SOCKS_PROXY"]
elif "ALL_PROXY2" in os.environ:
    proxy = os.environ["ALL_PROXY2"]


if proxy:
    openai.proxy = proxy
    if proxy.startswith('socks'):
        logger.debug("using socks proxy: %s", proxy)
        try:
            import socks
        except ImportError:
            print("Please install pysocks: pip install pysocks")
            exit(1)

def _print(text, render):
    content = text
    if args.raw:
        render(content)
        return
    markdown = Markdown(
        content,
        inline_code_lexer="auto",
        inline_code_theme="monokai",
    )
    render(markdown)


def _ask(question, stream=False):
    messages = []
    if isinstance(question, list):
        messages = question
    else:
        messages = [{"role": "user", "content": question}]
    return openai.ChatCompletion.create(
        model=args.model,
        messages=messages,
        stream=stream,
    )


def ask(question, stream=False):
    content = ""
    if stream:
        with Live("[bold green]Asking...", refresh_per_second=3) as live:
            logger.debug("asking question: %s", question)
            response = _ask(question, stream=stream)
            for v in response:
                if (
                    v.choices
                    and "content" in v.choices[0].delta
                    and v.choices[0].delta.content
                ):
                    content += v.choices[0].delta.content
                    _print(content, live.update)
    else:
        with console.status("[bold green]Asking...", spinner="point") as status:
            response = _ask(question)
            content = response.choices[0].message.content
            _print(content, console.print)
            status.update("[bold green]Done!")
    return content


def chat():
    stream = not args.no_stream
    messages = []
    while True:
        question = Prompt.ask(
            "[bold blue]You[/bold blue]",
            console=console,
        )
        if not question:
            break
        messages.append({"role": "user", "content": question})
        console.print("\n[bold green]Assistant[/bold green]:")
        answer = ask(messages, stream)
        console.print("\n")
        messages.append({"role": "assistant", "content": answer})


def _get_text_from_clipboard():
    try:
        import pyperclip

        return pyperclip.paste()
    except ImportError:
        logger.error(
            "pyperclip is not installed, please install it use: pip install pyperclip"
        )
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


def translate():
    stream = not args.no_stream
    text = args.text
    if args.file:
        text = _get_text_from_file()
    elif args.clipboard:
        text = _get_text_from_clipboard()
    if not text:
        text = Prompt.ask("Please enter a text to translate")
    if isinstance(text, list):
        text = " ".join(text)
    if args.source:
        question = f"{text} \n\n Please translate the above content from {args.source} to {args.target}"
    else:
        question = f"{text} \n\n Please translate the above content into {args.target}"

    ask(question, stream=stream)


def ask_cmd():
    stream = not args.no_stream
    args.question = args.question or Prompt.ask("Please enter a question")
    if isinstance(args.question, list):
        args.question = " ".join(args.question)
    ask(args.question, stream=stream)


CMD = {
    "ask": ask_cmd,
    "chat": chat,
    "translate": translate,
    "help": parser.print_help,
}


def main():
    command = args.command
    logger.debug(f"command: {command}")
    if command in CMD:
        CMD[command]()
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        logger.debug(f"args: {args}")
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
        exit(0)
