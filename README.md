# AoS Warscroll Creator

AoS Warscroll Creator is now a small Python/Flask application with two explicit parts:

- a backend renderer that turns a canonical warscroll payload into an embeddable HTML fragment
- a server-rendered preview UI that edits that payload with classic HTML forms and keeps draft state on the server between redraws

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Run locally

```bash
uv sync
uv run python app.py
```

Open http://127.0.0.1:5000/

## Project layout

- `pyproject.toml` / `uv.lock` — uv-managed project metadata and locked dependencies
- `app.py` — Flask app, import/export endpoints, preview UI, lightweight server-side session storage
- `warscroll_app/models.py` — canonical payload schema and legacy JSON import adapter
- `warscroll_app/catalog.py` — faction/theme metadata and ability asset registries
- `warscroll_app/renderer.py` — pure renderer that returns an embeddable HTML fragment
- `templates/_warscroll_fragment.html` — HTML/CSS fragment for the rendered warscroll
- `templates/index.html` — server-rendered editor/preview page
- `public/` — static assets reused from the original project

## Renderer contract

`POST /fragment` accepts either:

- the new canonical payload shape used by `WarscrollPayload`
- a legacy Redux export from the previous React application

It returns `text/html` containing a self-styled embeddable fragment.

## JSON workflow

- `GET /export` downloads the current canonical payload as JSON
- `POST /import` accepts either canonical JSON or the legacy Redux export JSON

## Tests

```bash
uv run python -m unittest discover -s tests
```
