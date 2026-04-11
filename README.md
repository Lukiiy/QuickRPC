# Quick RPC

Quick Discord RPC with arRPC! Written in Python. 
Made with [uv](https://github.com/astral-sh/uv).

### Install

You can download the repository to use it or download the compiled binaries in the [Releases tab](https://github.com/Lukiiy/QuickRPC/releases)!

### Usage

You can use `uv run main.py [args]` or `quickrpc [args]`

```bash
quickrpc --client-id [clientid] --details "Playing Game" --state "Level 2"
```

```bash
quickrpc --client-id [clientid] --details "Playing Game" --large-image game_logo --large-text "Game Logo"
```

```bash
quickrpc --client-id [clientid] --details "Playing Game" --state "Ranked Match" --large-image game_logo --large-text "Game Logo" --small-image ranked_icon --small-text "Ranked logo"
```

### Dependencies

[pypresence](https://github.com/qwertyquerty/pypresence)  
[pyinstaller](https://pyinstaller.org/) (optional - dev)