import tiktoken


def get_token_count(text: str, model: str = "gpt-3.5-turbo") -> int:
    if model.startswith("o1"):
        model = "gpt-4o"
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)
