![yaya](https://github.com/y-ne/yaya/blob/main/yaya.jpg?raw=true)

## Yaya (夜々) of the Moon, Banned Doll Automaton.

## Dev Notes

```
uv python list

# i'm locking python 3.14.0
uv python pin cpython-3.14.0-macos-aarch64-none

# development
uv run fastapi dev app/main.py
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
