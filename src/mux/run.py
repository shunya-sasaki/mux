"""Mux is a unifiled warpper of terminal multiplexers."""

from mux.multiplexer import Multiplexer


def run():
    """Entrypoint of mux."""
    mux = Multiplexer()
    mux.app()


if __name__ == "__main__":
    run()
