import json
from typing import Optional
from fastmcp import FastMCP
from subprocess import Popen
from contextlib import asynccontextmanager
import requests
from pathlib import Path
from typing import Any
from dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    telegram_bot_token: str
    my_chat_id: str
    madame_chat_id: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    port: int
    host: str


config = Config()


@dataclass()
class ServerContext:
    radios: dict[Any, Any]
    player: Optional[Popen[bytes]] = None
    current_radio = None

    def stop_radio(self):
        if self.player:
            self.player.terminate()
        if self.current_radio:
            self.current_radio = None

    def start_radio(self, radio_id: str):
        self.stop_radio()
        radios = [radio for radio in context.radios if radio["id"] == radio_id]
        if len(radios) != 1:
            raise ValueError(f"Could not find the radio with id {radio_id}")
        radio = radios[0]
        context.player = Popen(["cvlc", radio["url"]])
        context.current_radio = radio


with open(Path(__file__).parent / "radios.json") as fd:
    radios = json.load(fd)

context = ServerContext(radios=radios)


@asynccontextmanager
async def app_lifespan(_server: FastMCP):
    try:
        yield
    finally:
        if context.player:
            context.player.terminate()


mcp = FastMCP(
    name="HomeMCP",
    instructions="""
A simple server that play and stop radio and can send messages.
""",
    lifespan=app_lifespan,
)


@mcp.tool()
def stop_radio():
    """Stop playing the radio"""
    context.stop_radio()


@mcp.tool()
def play_radio(radio_id: str):
    """Play a radio given it's id"""
    context.start_radio(radio_id)


@mcp.tool()
def current_radio():
    """Return the currently playing radio"""
    return context.current_radio


@mcp.tool()
def list_radios():
    """Return a list of all the radios"""
    return context.radios


@mcp.tool()
def send_message_me(content: str):
    """Send a message to me, or monsieur via telegram"""
    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    data = {"chat_id": config.my_chat_id, "text": content}
    requests.post(url, data=data)


@mcp.tool()
def send_message_madame(content: str):
    """Send a message to my wife, or Madame, via telegram"""
    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    data = {"chat_id": config.madame_chat_id, "text": content}
    requests.post(url, data=data)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        port=config.port,
        host=config.host,
    )
