from __future__ import annotations

import json
import os
import re
import secrets
from pathlib import Path
from typing import Any

from flask import Flask, Response, make_response, render_template, request

from warscroll_app.catalog import (
    ABILITY_ICONS,
    ABILITY_KEYWORDS,
    ABILITY_PHASES,
    ABILITY_RESTRICTIONS,
    ABILITY_TIMINGS,
    ABILITY_TYPES,
    ALLIANCE_ORDER,
    FACTIONS,
    KEYWORD_ABILITY_OPTIONS,
    KEYWORD_IDENTITY_OPTIONS,
)
from warscroll_app.models import Ability, WarscrollPayload, Weapon, payload_from_form
from warscroll_app.renderer import render_warscroll_fragment

BASE_DIR = Path(__file__).resolve().parent
COOKIE_NAME = "warscroll_session_id"
SESSION_ID_PATTERN = re.compile(r"^[0-9a-f]{48}$")
SESSION_STORE: dict[str, dict[str, Any]] = {}

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/static",
    template_folder=str(BASE_DIR / "templates"),
)


@app.get("/")
def index() -> Response:
    session_id, payload = _get_current_payload()
    return _render_index(payload, session_id)


@app.post("/")
def update() -> Response:
    session_id, _ = _get_current_payload()
    action = request.form.get("action", "preview")
    payload = (
        WarscrollPayload.default()
        if action == "reset"
        else payload_from_form(request.form)
    )

    if action == "add_ranged_weapon":
        payload.ranged_weapons.append(Weapon())
    elif action.startswith("remove_ranged_weapon:"):
        payload = _remove_item(payload, "ranged_weapons", action)
    elif action == "add_melee_weapon":
        payload.melee_weapons.append(Weapon())
    elif action.startswith("remove_melee_weapon:"):
        payload = _remove_item(payload, "melee_weapons", action)
    elif action == "add_ability":
        payload.abilities.append(Ability())
    elif action.startswith("remove_ability:"):
        payload = _remove_item(payload, "abilities", action)
    elif action == "add_loadout_point":
        payload.loadout_points.append("")
    elif action.startswith("remove_loadout_point:"):
        payload = _remove_item(payload, "loadout_points", action)

    return _render_index(payload, session_id)


@app.post("/import")
def import_payload() -> Response:
    session_id, _ = _get_current_payload()
    upload = request.files.get("payload_file")
    if not upload or not upload.filename:
        return _render_index(
            WarscrollPayload.default(),
            session_id,
            error_message="Choose a JSON file to import.",
        )
    try:
        payload = WarscrollPayload.from_any_dict(json.load(upload.stream))
    except (json.JSONDecodeError, TypeError, ValueError):
        return _render_index(
            WarscrollPayload.default(),
            session_id,
            error_message="The uploaded file was not valid JSON.",
        )
    return _render_index(
        payload, session_id, success_message=f"Imported {upload.filename}."
    )


@app.get("/export")
def export_payload() -> Response:
    _, payload = _get_current_payload()
    filename_root = payload.warscroll_name.strip().replace(" ", "_") or "warscroll"
    response = make_response(json.dumps(payload.to_dict(), indent=2))
    response.headers["Content-Type"] = "application/json"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{filename_root}.json"'
    )
    return response


@app.post("/fragment")
def render_fragment() -> Response:
    payload = WarscrollPayload.from_any_dict(request.get_json(silent=True) or {})
    fragment = render_warscroll_fragment(
        payload, asset_base_url=request.args.get("asset_base_url", "/static")
    )
    return Response(fragment, mimetype="text/html")


@app.get("/health")
def health() -> Response:
    return Response("ok", mimetype="text/plain")


def _render_index(
    payload: WarscrollPayload,
    session_id: str | None,
    *,
    error_message: str | None = None,
    success_message: str | None = None,
) -> Response:
    next_session_id = secrets.token_hex(24)
    SESSION_STORE[next_session_id] = payload.to_dict()
    if session_id and session_id in SESSION_STORE and session_id != next_session_id:
        del SESSION_STORE[session_id]
    response = make_response(
        render_template(
            "index.html",
            payload=payload,
            preview_fragment=render_warscroll_fragment(payload),
            faction_groups=_group_factions(),
            ability_phases=ABILITY_PHASES,
            ability_types=ABILITY_TYPES,
            ability_icons=ABILITY_ICONS,
            ability_timings=ABILITY_TIMINGS,
            ability_restrictions=ABILITY_RESTRICTIONS,
            ability_keywords=ABILITY_KEYWORDS,
            keyword_ability_options=KEYWORD_ABILITY_OPTIONS,
            keyword_identity_options=KEYWORD_IDENTITY_OPTIONS,
            error_message=error_message,
            success_message=success_message,
        )
    )
    response.set_cookie(
        COOKIE_NAME,
        next_session_id,
        httponly=True,
        samesite="Lax",
        secure=request.is_secure,
    )
    return response


def _get_current_payload() -> tuple[str | None, WarscrollPayload]:
    session_id = request.cookies.get(COOKIE_NAME)
    if (
        not session_id
        or not SESSION_ID_PATTERN.fullmatch(session_id)
        or session_id not in SESSION_STORE
    ):
        return None, WarscrollPayload.default()
    return session_id, WarscrollPayload.from_dict(SESSION_STORE[session_id])


def _remove_item(
    payload: WarscrollPayload, attribute: str, action: str
) -> WarscrollPayload:
    index = int(action.split(":", 1)[1])
    values = list(getattr(payload, attribute))
    if 0 <= index < len(values):
        values.pop(index)
    setattr(payload, attribute, values)
    return payload


def _group_factions() -> list[tuple[str, list[Any]]]:
    grouped: list[tuple[str, list[Any]]] = []
    for alliance in ALLIANCE_ORDER:
        factions = sorted(
            (theme for theme in FACTIONS.values() if theme.alliance == alliance),
            key=lambda item: item.name,
        )
        grouped.append((alliance, factions))
    return grouped


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
