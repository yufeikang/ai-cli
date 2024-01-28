Release v0.4.0
---------------------------

- fix: upgrade openai sdk
- feat: support azure openai

Release v0.3.8
---------------------------

- fix: upgrade tiktoken to support new model

Release v0.3.5
---------------------------

- fix: EdgeGPT bot error
- `commit` command add user-prompt option

Release v0.3.4
---------------------------

- fix: `commit` command error when delete file from git

Release v0.3.2
---------------------------

- fix: small bug fix

Release v0.3.0
---------------------------

- feat: `chat` and `review` command now can auto summary previous conversation.

Release v0.2.0
---------------------------

- feat: now support **New Bing** bot, you can use `ai setting --edit bot=BingBot` to switch to it
- feat: add `--bot` option to `ask` command, you can use `ai ask --bot BingBot "Hello"` to use BingBot
- refactor: setting file moved to `~/.config/ai_cli/setting.json`

Release v0.1.1
---------------------------

- fix: fix `commit` command, use --cache option to diff code changes
- feat: the `commit` add `--message` option, you can add message to generated commit message after
- feat: now you can edit generated commit message before commit

Release v0.1.0
---------------------------

- feat: add `commit` command, now you can commit your code changes by using `ai commit` command

Release v0.0.9
---------------------------

- feat: `ask` command now supports `--prompt` option. use `help` command to see more details

Release v0.0.8
---------------------------

- fix: fix chat command

Release v0.0.7 (2023-03-07)
---------------------------

- feat:  add `review` command, now you can review your code changes by using `ai review` command
- feat:  handle rate limit errors and retry

Release v0.0.6 (2023-03-06)
---------------------------

- feat: support multi-line input, to enable it, use `ai setting --edit multi_line_input=yes`
- feat: `setting` command now supports `--edit` option example: `setting --edit api_key=xxx raw=yes`

Release v0.0.5 (2023-03-05)
---------------------------

## [Update] - 2023-03-05

- feat: add `setting` command. now you can save settings to a file
