"""Multiplexer class that is wrapper of multiplexers."""

import os
import subprocess
import time
from typing import Annotated

import typer
from typer import Argument
from typer import Option


class Multiplexer:
    """A unified wrapper of terminal multiplexers."""

    def __init__(self):
        """Initializer of Multiplexer."""
        self.backend = self._detect_backend()
        self.pane_id = self._detect_self_pane_id()
        self.app = typer.Typer(no_args_is_help=True)
        self.app.command(help="Write keys to a pane.", no_args_is_help=True)(
            self.send
        )
        self.app.command(
            help="Read contents of a pane.", no_args_is_help=(True)
        )(self.read)

    def _detect_backend(self) -> str:
        if (os.environ.get("ZELLIJ_PANE_ID", None)) is not None:
            backend = "Zellij"
        elif (os.environ.get("TMUX_PANE", None)) is not None:
            backend = "Tmux"
        elif (os.environ.get("WEZTERM_PANE", None)) is not None:
            backend = "WezTerm"
        return backend

    def _detect_self_pane_id(self):
        match self.backend:
            case "Zellij":
                pane_id = int(os.environ["ZELLIJ_PANE_ID"])
            case "Tmux":
                pane_id = int(os.environ["TMUX_PANE"].replace("%", ""))
            case "WezTerm":
                pane_id = int(os.environ["WEZTERM_PANE"])
        return pane_id

    def send(
        self,
        pane_id: Annotated[int, Argument(help="Pane id")],
        message: Annotated[str, Argument(help="Message contents.")],
        wait_seconds: Annotated[
            float,
            Option(help="Wait time between messages and enter.", min=0.0),
        ] = 0.1,
        with_enter: Annotated[bool, Option(is_flag=True)] = True,
    ):
        """Send a message to the target pane."""
        match self.backend:
            case "Zellij":
                cmd = [
                    "zellij",
                    "action",
                    "write-chars",
                    "--pane-id",
                    f"{pane_id}",
                    f"{message}",
                ]
                enter_cmd = [
                    "zellij",
                    "action",
                    "write",
                    "--pane-id",
                    f"{pane_id}",
                    "13",
                ]
            case "Tmux":
                cmd = [
                    "tmux",
                    "send-keys",
                    "-t",
                    f"{pane_id}",
                    f"{message}",
                ]
                enter_cmd = [
                    "tmux",
                    "send-keys",
                    "-t",
                    f"{pane_id}",
                    "Enter",
                ]
            case "WezTerm":
                cmd = [
                    "wezterm",
                    "cli",
                    "send-text",
                    "--pane-id",
                    f"{pane_id}",
                    f"{message}",
                ]
                enter_cmd = [
                    "wezterm",
                    "cli",
                    "send-text",
                    "--pane-id",
                    f"{pane_id}",
                    "--no-paste",
                    "\r",
                ]
            case _:
                cmd = []
                enter_cmd = []
        subprocess.run(cmd, shell=False)
        if with_enter:
            time.sleep(wait_seconds)
            subprocess.run(enter_cmd, shell=False)

    def read(self, pane_id: Annotated[int, Argument(help="Pane id")]) -> None:
        """Read buffer of the target pane."""
        match self.backend:
            case "Zellij":
                cmd = [
                    "zellij",
                    "action",
                    "dump-screen",
                    "--pane-id",
                    f"{pane_id}",
                ]
            case "Tmux":
                cmd = ["tmux", "capture-pane", "-p", "-t", f"{pane_id}"]
            case "WezTerm":
                cmd = [
                    "wezterm",
                    "cli",
                    "get-text",
                    "--pane-id",
                    f"{pane_id}",
                ]
            case _:
                cmd = []
        result = subprocess.run(cmd, shell=False, capture_output=True)
        result_str = result.stdout.decode("utf-8")
        out = result_str.replace("\\n", "\n")
        print(out)
