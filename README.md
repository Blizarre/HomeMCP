# A short experiment using MCP server at home

This is a small [MCP](https://en.wikipedia.org/wiki/Model_Context_Protocol) server that I used to experiment with the concept. It can play a radio based on a list in `radios.json`, stop the radio, and send a telegram message to me or to my wife.

I use the `send.sh` script to record my voice, transcribe it locally using `whisper`, and then use claude to ask my own personal butler to action it. It is pretty limited and very janky but still is better than siri!

I scraped the radios from various sources using claude. I haven't listened to most of them yet.

## How to use

1. Copy the env file to .env and update it with your config
2. Run the MCP server

```shell
uv run python main.py
```
