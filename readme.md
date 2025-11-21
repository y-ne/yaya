## Yaya (夜々) of the Moon, Banned Doll Automaton.

![yaya](https://github.com/y-ne/yaya/blob/main/yaya.jpg?raw=true)

## Dev Notes

```
uv python list

# i'm locking python 3.14.0 with GIL disabled
uv python pin cpython-3.14.0+freethreaded-macos-aarch64-none

uv sync

# development
uv run fastapi dev app/main.py

# fully disabled GIL
uv run python -X gil=0 -m fastapi dev app/main.py
```

## Project Structure

```
yaya/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── *.py
│   ├── schemas/
│   │   └── *.py
│   ├── routers/
│   │   └── *.py
│   └── services/
│       └── *_service.py
├── .env.example
├── pyproject.toml
└── readme.md
```
