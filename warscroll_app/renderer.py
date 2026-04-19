from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .catalog import (
    ABILITY_ICONS,
    ABILITY_PHASES,
    ABILITY_TYPES,
    asset_url,
    get_faction,
)
from .models import (
    Ability,
    MELEE_OVERRIDE_ORDER,
    RANGED_OVERRIDE_ORDER,
    WarscrollPayload,
    Weapon,
)

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_renderer_environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(enabled_extensions=("html",)),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_warscroll_fragment(
    payload: WarscrollPayload, asset_base_url: str = "/static"
) -> str:
    template = _renderer_environment.get_template("_warscroll_fragment.html")
    return template.render(**build_render_context(payload, asset_base_url))


def build_render_context(
    payload: WarscrollPayload, asset_base_url: str = "/static"
) -> dict[str, Any]:
    faction = get_faction(payload.faction_id)
    display_faction_name = payload.custom_faction_name.strip() or faction.name
    loadout_points = [point for point in payload.loadout_points if point.strip()]
    show_loadout = bool(payload.loadout_body.strip() or loadout_points)
    show_abilities = any(not ability.is_empty() for ability in payload.abilities)
    return {
        "asset_base_url": asset_base_url,
        "background_url": asset_url(asset_base_url, faction.template_path),
        "weapon_banner_url": asset_url(asset_base_url, faction.weapon_banner_path),
        "display_faction_name": display_faction_name,
        "title_strip": f"• {display_faction_name.upper()} WARSCROLL •",
        "warscroll_name": payload.warscroll_name.strip().upper(),
        "warscroll_subtype": payload.warscroll_subtype.strip().upper(),
        "move": f'{payload.move.strip()}"' if payload.move.strip() else "",
        "health": payload.health.strip(),
        "control": payload.control.strip(),
        "save": payload.save.strip(),
        "keyword_abilities": ", ".join(payload.keyword_abilities).upper(),
        "keyword_identities": ", ".join(payload.keyword_identities).upper(),
        "weapon_tables": _build_weapon_tables(payload, asset_base_url),
        "loadout_body": payload.loadout_body.strip(),
        "loadout_points": loadout_points,
        "ability_columns": _build_ability_columns(payload.abilities, asset_base_url),
        "show_loadout": show_loadout,
        "show_abilities": show_abilities,
        "show_lower_sections": show_loadout or show_abilities,
    }


def _build_weapon_tables(
    payload: WarscrollPayload, asset_base_url: str
) -> list[dict[str, Any]]:
    faction = get_faction(payload.faction_id)
    banner_url = asset_url(asset_base_url, faction.weapon_banner_path)
    tables: list[dict[str, Any]] = []
    ranged_rows = [weapon for weapon in payload.ranged_weapons if not weapon.is_empty()]
    melee_rows = [weapon for weapon in payload.melee_weapons if not weapon.is_empty()]
    if ranged_rows:
        tables.append(
            {
                "title": "Ranged Weapons",
                "headers": [
                    "Weapon",
                    "Rng",
                    "Atk",
                    "Hit",
                    "Wnd",
                    "Rnd",
                    "Dmg",
                    "Ability",
                ],
                "rows": [
                    _build_weapon_row(weapon, True, index)
                    for index, weapon in enumerate(ranged_rows)
                ],
                "banner_url": banner_url,
            }
        )
    if melee_rows:
        tables.append(
            {
                "title": "Melee Weapons",
                "headers": ["Weapon", "Atk", "Hit", "Wnd", "Rnd", "Dmg", "Ability"],
                "rows": [
                    _build_weapon_row(weapon, False, index)
                    for index, weapon in enumerate(melee_rows)
                ],
                "banner_url": banner_url,
            }
        )
    return tables


def _build_weapon_row(weapon: Weapon, is_ranged: bool, index: int) -> dict[str, Any]:
    stats = (
        [
            ("range", _display_range(weapon.range)),
            ("atk", weapon.atk),
            ("to_hit", weapon.to_hit),
            ("to_wound", weapon.to_wound),
            ("rend", weapon.rend),
            ("damage", weapon.damage),
        ]
        if is_ranged
        else [
            ("atk", weapon.atk),
            ("to_hit", weapon.to_hit),
            ("to_wound", weapon.to_wound),
            ("rend", weapon.rend),
            ("damage", weapon.damage),
        ]
    )
    return {
        "is_battle_damaged": weapon.is_battle_damaged,
        "battle_damage_icon": ABILITY_ICONS["battle_damaged"]["path"],
        "name": weapon.name,
        "ability": weapon.ability or "-",
        "cells": _build_stat_cells(
            stats,
            weapon.override_fields,
            RANGED_OVERRIDE_ORDER if is_ranged else MELEE_OVERRIDE_ORDER,
        ),
        "row_opacity": 0.16 if index % 2 == 0 else 0.28,
    }


def _build_stat_cells(
    stats: list[tuple[str, str]], override_fields: list[str], override_order: list[str]
) -> list[dict[str, Any]]:
    active_fields = [field for field in override_order if field in override_fields]
    if not active_fields:
        return [
            {"value": value or "-", "colspan": 1, "is_override": False}
            for _, value in stats
        ]
    first_index = override_order.index(active_fields[0])
    last_index = override_order.index(active_fields[-1])
    cells: list[dict[str, Any]] = []
    for index, (_, value) in enumerate(stats):
        if index < first_index or index > last_index:
            cells.append({"value": value or "-", "colspan": 1, "is_override": False})
        elif index == first_index:
            cells.append(
                {
                    "value": "*" if first_index == last_index else "See Below",
                    "colspan": last_index - first_index + 1,
                    "is_override": True,
                }
            )
    return cells


def _build_ability_columns(
    abilities: list[Ability], asset_base_url: str
) -> list[list[dict[str, Any]]]:
    rendered = [
        _build_ability_view(ability, asset_base_url)
        for ability in abilities
        if not ability.is_empty()
    ]
    columns: list[list[dict[str, Any]]] = [[], []]
    heights = [0, 0]
    for ability in rendered:
        target = 0 if heights[0] <= heights[1] else 1
        columns[target].append(ability)
        heights[target] += ability["estimated_height"]
    return columns


def _build_ability_view(ability: Ability, asset_base_url: str) -> dict[str, Any]:
    phase = ABILITY_PHASES.get(ability.phase, ABILITY_PHASES["start_deployment"])
    ability_type = ABILITY_TYPES.get(ability.ability_type, ABILITY_TYPES["standard"])
    icon = ABILITY_ICONS.get(ability.icon, ABILITY_ICONS["none"])
    title_parts = [
        part.strip() for part in [ability.restriction, ability.timing] if part.strip()
    ]
    title = " • ".join(title_parts)
    return {
        "banner_url": asset_url(asset_base_url, phase["banner_path"]),
        "line_color": phase["line_color"],
        "title": title,
        "icon_url": asset_url(asset_base_url, icon["path"]),
        "type_icon_url": asset_url(asset_base_url, ability_type["icon_path"]),
        "type_value": ability.ability_type_value,
        "type_text_color": ability_type["text_color"],
        "name": ability.name.upper(),
        "name_desc": ability.name_desc,
        "declare_desc": ability.declare_desc,
        "effect_desc": ability.effect_desc,
        "keywords": ", ".join(ability.keywords),
        "estimated_height": _estimate_ability_height(ability, title),
    }


def _estimate_ability_height(ability: Ability, title: str) -> int:
    text_blocks = [
        title,
        ability.name,
        ability.name_desc,
        ability.declare_desc,
        ability.effect_desc,
        ", ".join(ability.keywords),
    ]
    return 120 + sum(len(block) for block in text_blocks) // 3


def _display_range(value: str) -> str:
    stripped = value.strip()
    return f'{stripped}"' if stripped else "-"
