# mux

A unified CLI to send keystrokes to and read the buffer of panes
across Tmux, Zellij, and WezTerm.

## 📦 Requirements

You need **at least one** of the supported multiplexers
— `mux` automatically detects whichever one you are running inside.

- [Tmux](https://github.com/tmux/tmux)
  — terminal multiplexer; panes are addressed via `send-keys` / `capture-pane`.
- [Zellij](https://zellij.dev/)
  — terminal workspace; panes are driven via `zellij action`.
- [WezTerm](https://wezterm.org/)
  — GPU-accelerated terminal whose built-in multiplexer is controlled via `wezterm cli`.

## ⚙️ Setup

Install `mux` as a standalone command-line tool. Using
[uv](https://docs.astral.sh/uv/) is recommended, as it installs `mux` into an
isolated environment and exposes the `mux` command on your `PATH`:

```sh
uv tool install git+https://github.com/shunya-sasaki/mux
```

If you prefer `pip`, install it with [pipx](https://pipx.pypa.io/) to keep it
isolated from your other Python packages:

```sh
pipx install git+https://github.com/shunya-sasaki/mux
```

## 🚀 Usage

## 📚 Reference

- [Tmux](https://github.com/tmux/tmux)
- [Zellij](https://zellij.dev/)
- [WezTerm](https://wezterm.org/)

## 📄 License

MIT License

See [LICENSE](./LICENSE) for the detail.
