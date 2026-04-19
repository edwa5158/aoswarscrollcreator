from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping

from .catalog import (
    DEFAULT_FACTION_ID,
    LEGACY_ABILITY_BANNER_TO_PHASE,
    LEGACY_ABILITY_ICON_TO_ID,
    LEGACY_ABILITY_TYPE_ICON_TO_ID,
    LEGACY_BANNER_TO_FACTION_ID,
    LEGACY_TEMPLATE_TO_FACTION_ID,
)

RANGED_OVERRIDE_ORDER = ["range", "atk", "to_hit", "to_wound", "rend", "damage"]
MELEE_OVERRIDE_ORDER = ["atk", "to_hit", "to_wound", "rend", "damage"]


@dataclass
class Weapon:
    name: str = ""
    range: str = ""
    atk: str = ""
    to_hit: str = ""
    to_wound: str = ""
    rend: str = "-"
    damage: str = ""
    ability: str = ""
    is_battle_damaged: bool = False
    override_fields: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        rend_value = self.rend.strip()
        return not any(
            [
                self.name.strip(),
                self.range.strip(),
                self.atk.strip(),
                self.to_hit.strip(),
                self.to_wound.strip(),
                rend_value and rend_value != "-",
                self.damage.strip(),
                self.ability.strip(),
                self.is_battle_damaged,
                self.override_fields,
            ]
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "Weapon":
        if not data:
            return cls()
        return cls(
            name=str(data.get("name", "")),
            range=str(data.get("range", "")),
            atk=str(data.get("atk", "")),
            to_hit=str(data.get("to_hit", data.get("toHit", ""))),
            to_wound=str(data.get("to_wound", data.get("toWound", ""))),
            rend=str(data.get("rend", "-")) or "-",
            damage=str(data.get("damage", "")),
            ability=str(data.get("ability", "")),
            is_battle_damaged=bool(data.get("is_battle_damaged", data.get("isBattleDamaged", False))),
            override_fields=_normalize_override_fields(data.get("override_fields", [])),
        )

    @classmethod
    def from_legacy(cls, data: Mapping[str, Any] | None, kind: str) -> "Weapon":
        if not data:
            return cls()
        override_fields: list[str] = []
        if data.get("isOverride") and data.get("override"):
            override_fields = [
                _legacy_override_field_name(key)
                for key, enabled in dict(data.get("override", [{}])[0]).items()
                if enabled
            ]
        if kind == "melee":
            override_fields = [field for field in override_fields if field in MELEE_OVERRIDE_ORDER]
        else:
            override_fields = [field for field in override_fields if field in RANGED_OVERRIDE_ORDER]
        return cls(
            name=str(data.get("name", "")),
            range=str(data.get("range", "")),
            atk=str(data.get("atk", "")),
            to_hit=str(data.get("toHit", "")),
            to_wound=str(data.get("toWound", "")),
            rend=str(data.get("rend", "-")) or "-",
            damage=str(data.get("damage", "")),
            ability=str(data.get("ability", "")),
            is_battle_damaged=bool(data.get("isBattleDamaged", False)),
            override_fields=override_fields,
        )


@dataclass
class Ability:
    name: str = ""
    name_desc: str = ""
    declare_desc: str = ""
    effect_desc: str = ""
    keywords: list[str] = field(default_factory=list)
    phase: str = "start_deployment"
    timing: str = ""
    ability_type: str = "standard"
    ability_type_value: str = ""
    restriction: str = ""
    icon: str = "none"

    def is_empty(self) -> bool:
        return not any(
            [
                self.name.strip(),
                self.name_desc.strip(),
                self.declare_desc.strip(),
                self.effect_desc.strip(),
                self.keywords,
                self.timing.strip(),
                self.ability_type_value.strip(),
                self.restriction.strip(),
                self.icon != "none",
                self.phase != "start_deployment",
                self.ability_type != "standard",
            ]
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "Ability":
        if not data:
            return cls()
        return cls(
            name=str(data.get("name", "")),
            name_desc=str(data.get("name_desc", "")),
            declare_desc=str(data.get("declare_desc", "")),
            effect_desc=str(data.get("effect_desc", "")),
            keywords=_normalize_string_list(data.get("keywords", [])),
            phase=str(data.get("phase", "start_deployment")) or "start_deployment",
            timing=str(data.get("timing", "")),
            ability_type=str(data.get("ability_type", "standard")) or "standard",
            ability_type_value=str(data.get("ability_type_value", "")),
            restriction=str(data.get("restriction", "")),
            icon=str(data.get("icon", "none")) or "none",
        )

    @classmethod
    def from_legacy(cls, data: Mapping[str, Any] | None) -> "Ability":
        if not data:
            return cls()
        return cls(
            name=str(data.get("name", "")),
            name_desc=str(data.get("name_desc", "")),
            declare_desc=str(data.get("declare_desc", "")),
            effect_desc=str(data.get("effect_desc", "")),
            keywords=_split_csv_or_lines(data.get("keywords", "")),
            phase=LEGACY_ABILITY_BANNER_TO_PHASE.get(str(data.get("ability_banner", "")), "start_deployment"),
            timing=str(data.get("ability_timing", "")),
            ability_type=LEGACY_ABILITY_TYPE_ICON_TO_ID.get(str(data.get("ability_icon_type_path", "")), "standard"),
            ability_type_value=str(data.get("ability_type_value", "")),
            restriction=str(data.get("ability_restriction", "")).rstrip(", "),
            icon=LEGACY_ABILITY_ICON_TO_ID.get(str(data.get("ability_icon_path", "")), "none"),
        )


@dataclass
class WarscrollPayload:
    faction_id: str = DEFAULT_FACTION_ID
    custom_faction_name: str = ""
    warscroll_name: str = ""
    warscroll_subtype: str = ""
    move: str = ""
    health: str = "1"
    control: str = "1"
    save: str = "-"
    keyword_abilities: list[str] = field(default_factory=list)
    keyword_identities: list[str] = field(default_factory=list)
    ranged_weapons: list[Weapon] = field(default_factory=list)
    melee_weapons: list[Weapon] = field(default_factory=list)
    loadout_body: str = ""
    loadout_points: list[str] = field(default_factory=list)
    abilities: list[Ability] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "faction_id": self.faction_id,
            "custom_faction_name": self.custom_faction_name,
            "warscroll_name": self.warscroll_name,
            "warscroll_subtype": self.warscroll_subtype,
            "move": self.move,
            "health": self.health,
            "control": self.control,
            "save": self.save,
            "keyword_abilities": list(self.keyword_abilities),
            "keyword_identities": list(self.keyword_identities),
            "ranged_weapons": [weapon.to_dict() for weapon in self.ranged_weapons],
            "melee_weapons": [weapon.to_dict() for weapon in self.melee_weapons],
            "loadout_body": self.loadout_body,
            "loadout_points": list(self.loadout_points),
            "abilities": [ability.to_dict() for ability in self.abilities],
        }

    @classmethod
    def default(cls) -> "WarscrollPayload":
        return cls()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "WarscrollPayload":
        if not data:
            return cls.default()
        return cls(
            faction_id=str(data.get("faction_id", DEFAULT_FACTION_ID)) or DEFAULT_FACTION_ID,
            custom_faction_name=str(data.get("custom_faction_name", "")),
            warscroll_name=str(data.get("warscroll_name", "")),
            warscroll_subtype=str(data.get("warscroll_subtype", "")),
            move=str(data.get("move", "")),
            health=str(data.get("health", "1")) or "1",
            control=str(data.get("control", "1")) or "1",
            save=str(data.get("save", "-")) or "-",
            keyword_abilities=_normalize_string_list(data.get("keyword_abilities", [])),
            keyword_identities=_normalize_string_list(data.get("keyword_identities", [])),
            ranged_weapons=[Weapon.from_dict(item) for item in data.get("ranged_weapons", [])],
            melee_weapons=[Weapon.from_dict(item) for item in data.get("melee_weapons", [])],
            loadout_body=str(data.get("loadout_body", "")),
            loadout_points=_normalize_string_list(data.get("loadout_points", [])),
            abilities=[Ability.from_dict(item) for item in data.get("abilities", [])],
        )

    @classmethod
    def from_any_dict(cls, data: Mapping[str, Any] | None) -> "WarscrollPayload":
        if not data:
            return cls.default()
        if "faction_id" in data:
            return cls.from_dict(data)
        return cls.from_legacy_state(data)

    @classmethod
    def from_legacy_state(cls, data: Mapping[str, Any]) -> "WarscrollPayload":
        faction = data.get("faction", {})
        characteristics = data.get("characteristics", {})
        weapons = data.get("weapons", {})
        abilities = data.get("abilities", {})
        loadout = data.get("loadout", {})
        keywords = data.get("keywords", {})
        faction_id = LEGACY_TEMPLATE_TO_FACTION_ID.get(
            str(faction.get("factionTemplate", "")),
            LEGACY_BANNER_TO_FACTION_ID.get(str(faction.get("factionWeaponBanner", "")), DEFAULT_FACTION_ID),
        )
        return cls(
            faction_id=faction_id,
            custom_faction_name=str(faction.get("customFactionName", "")),
            warscroll_name=str(characteristics.get("warscrollName", "")),
            warscroll_subtype=str(characteristics.get("warscrollSubtype", "")),
            move=str(characteristics.get("warscrollMove", "")),
            health=str(characteristics.get("warscrollHealth", "1")) or "1",
            control=str(characteristics.get("warscrollControl", "1")) or "1",
            save=str(characteristics.get("warscrollSave", "-")) or "-",
            keyword_abilities=_normalize_string_list(keywords.get("keywordAbilities", [])),
            keyword_identities=_normalize_string_list(keywords.get("keywordIdentities", [])),
            ranged_weapons=[Weapon.from_legacy(item, "ranged") for item in weapons.get("rangedWeaponStats", [])],
            melee_weapons=[Weapon.from_legacy(item, "melee") for item in weapons.get("meleeWeaponStats", [])],
            loadout_body=str(loadout.get("body", "")),
            loadout_points=_normalize_string_list(loadout.get("points", [])),
            abilities=[Ability.from_legacy(item) for item in abilities.get("abilities", [])],
        )


def payload_from_form(form: Mapping[str, Any]) -> WarscrollPayload:
    ranged_count = _read_int(form.get("ranged_weapon_count"), 0)
    melee_count = _read_int(form.get("melee_weapon_count"), 0)
    ability_count = _read_int(form.get("ability_count"), 0)
    loadout_point_count = _read_int(form.get("loadout_point_count"), 0)

    ranged_weapons = [_weapon_from_form(form, "ranged", index) for index in range(ranged_count)]
    melee_weapons = [_weapon_from_form(form, "melee", index) for index in range(melee_count)]
    abilities = [_ability_from_form(form, index) for index in range(ability_count)]
    loadout_points = [str(form.get(f"loadout_point_{index}", "")).strip() for index in range(loadout_point_count)]

    return WarscrollPayload(
        faction_id=str(form.get("faction_id", DEFAULT_FACTION_ID)) or DEFAULT_FACTION_ID,
        custom_faction_name=str(form.get("custom_faction_name", "")).strip(),
        warscroll_name=str(form.get("warscroll_name", "")).strip(),
        warscroll_subtype=str(form.get("warscroll_subtype", "")).strip(),
        move=str(form.get("move", "")).strip(),
        health=str(form.get("health", "1")).strip() or "1",
        control=str(form.get("control", "1")).strip() or "1",
        save=str(form.get("save", "-")).strip() or "-",
        keyword_abilities=_split_csv_or_lines(form.get("keyword_abilities", "")),
        keyword_identities=_split_csv_or_lines(form.get("keyword_identities", "")),
        ranged_weapons=ranged_weapons,
        melee_weapons=melee_weapons,
        loadout_body=str(form.get("loadout_body", "")).strip(),
        loadout_points=loadout_points,
        abilities=abilities,
    )


def _weapon_from_form(form: Mapping[str, Any], prefix: str, index: int) -> Weapon:
    override_name = f"{prefix}_weapon_{index}_override_fields"
    if hasattr(form, "getlist"):
        override_fields = form.getlist(override_name)
    else:
        override_fields = form.get(override_name, [])
    return Weapon(
        name=str(form.get(f"{prefix}_weapon_{index}_name", "")).strip(),
        range=str(form.get(f"{prefix}_weapon_{index}_range", "")).strip(),
        atk=str(form.get(f"{prefix}_weapon_{index}_atk", "")).strip(),
        to_hit=str(form.get(f"{prefix}_weapon_{index}_to_hit", "")).strip(),
        to_wound=str(form.get(f"{prefix}_weapon_{index}_to_wound", "")).strip(),
        rend=str(form.get(f"{prefix}_weapon_{index}_rend", "-")).strip() or "-",
        damage=str(form.get(f"{prefix}_weapon_{index}_damage", "")).strip(),
        ability=str(form.get(f"{prefix}_weapon_{index}_ability", "")).strip(),
        is_battle_damaged=bool(form.get(f"{prefix}_weapon_{index}_is_battle_damaged")),
        override_fields=_normalize_override_fields(override_fields),
    )


def _ability_from_form(form: Mapping[str, Any], index: int) -> Ability:
    return Ability(
        name=str(form.get(f"ability_{index}_name", "")).strip(),
        name_desc=str(form.get(f"ability_{index}_name_desc", "")).strip(),
        declare_desc=str(form.get(f"ability_{index}_declare_desc", "")).strip(),
        effect_desc=str(form.get(f"ability_{index}_effect_desc", "")).strip(),
        keywords=_split_csv_or_lines(form.get(f"ability_{index}_keywords", "")),
        phase=str(form.get(f"ability_{index}_phase", "start_deployment")) or "start_deployment",
        timing=str(form.get(f"ability_{index}_timing", "")).strip(),
        ability_type=str(form.get(f"ability_{index}_ability_type", "standard")) or "standard",
        ability_type_value=str(form.get(f"ability_{index}_ability_type_value", "")).strip(),
        restriction=str(form.get(f"ability_{index}_restriction", "")).strip(),
        icon=str(form.get(f"ability_{index}_icon", "none")) or "none",
    )


def _normalize_override_fields(value: Any) -> list[str]:
    if isinstance(value, str):
        values = _split_csv_or_lines(value)
    else:
        values = [str(item).strip() for item in value or []]
    result: list[str] = []
    for item in values:
        normalized = _legacy_override_field_name(item)
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def _normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return _split_csv_or_lines(value)
    if isinstance(value, Iterable):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _split_csv_or_lines(value: Any) -> list[str]:
    if value is None:
        return []
    text = str(value).replace("\r", "\n")
    if "\n" in text or "," in text:
        parts = [part.strip() for part in text.replace("\n", ",").split(",")]
        return [part for part in parts if part]
    stripped = text.strip()
    return [stripped] if stripped else []


def _legacy_override_field_name(field_name: str) -> str:
    mapping = {
        "toHit": "to_hit",
        "toWound": "to_wound",
        "range": "range",
        "atk": "atk",
        "rend": "rend",
        "damage": "damage",
    }
    return mapping.get(field_name, field_name)


def _read_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
