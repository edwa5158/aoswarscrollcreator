from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactionTheme:
    id: str
    name: str
    alliance: str
    template_path: str
    weapon_banner_path: str


FACTIONS: dict[str, FactionTheme] = {
    "beasts_of_chaos": FactionTheme("beasts_of_chaos", "Beasts of Chaos", "Chaos", "FactionBackgrounds/Chaos/Beasts/Beasts_Warscroll_Template.png", "FactionBackgrounds/Chaos/Beasts/Beasts_Weapon_Banner.png"),
    "blades_of_khorne": FactionTheme("blades_of_khorne", "Blades of Khorne", "Chaos", "FactionBackgrounds/Chaos/Khorne/Khorne_Warscroll_Template.png", "FactionBackgrounds/Chaos/Khorne/Khorne_Weapon_Banner.png"),
    "bonesplittaz": FactionTheme("bonesplittaz", "Bonesplittaz", "Destruction", "FactionBackgrounds/Destruction/Bonesplittaz/Bonesplittaz_Warscroll_Template.png", "FactionBackgrounds/Destruction/Orruks/Orruks_Weapon_Banner.png"),
    "cities_of_sigmar": FactionTheme("cities_of_sigmar", "Cities of Sigmar", "Order", "FactionBackgrounds/Order/Cities/Cities_Warscroll_Template.png", "FactionBackgrounds/Order/Cities/Cities_Weapon_Banner.png"),
    "daughters_of_khaine": FactionTheme("daughters_of_khaine", "Daughters of Khaine", "Order", "FactionBackgrounds/Order/Dok/Dok_Warscroll_Template.png", "FactionBackgrounds/Order/Dok/Dok_Weapon_Banner.png"),
    "disciples_of_tzeentch": FactionTheme("disciples_of_tzeentch", "Disciples of Tzeentch", "Chaos", "FactionBackgrounds/Chaos/Tzeench/Tzeench_Warscroll_Template.png", "FactionBackgrounds/Chaos/Tzeench/Tzeench_Weapon_Banner.png"),
    "flesh_eater_courts": FactionTheme("flesh_eater_courts", "Flesh-Eater Courts", "Death", "FactionBackgrounds/Death/FE/FE_Warscroll_Template.png", "FactionBackgrounds/Death/FE/FE_Weapon_Banner.png"),
    "fyreslayers": FactionTheme("fyreslayers", "Fyreslayers", "Order", "FactionBackgrounds/Order/Fyreslayers/Fyreslayers_Warscroll_Template.png", "FactionBackgrounds/Order/Fyreslayers/Fyreslayers_Weapon_Banner.png"),
    "gloomspite_gitz": FactionTheme("gloomspite_gitz", "Gloomspite Gitz", "Destruction", "FactionBackgrounds/Destruction/Gitz/Gitz_Warscroll_Template.png", "FactionBackgrounds/Destruction/Gitz/Gitz_Weapon_Banner.png"),
    "hedonites_of_slaanesh": FactionTheme("hedonites_of_slaanesh", "Hedonites of Slaanesh", "Chaos", "FactionBackgrounds/Chaos/Slaanesh/Slaanesh_Warscroll_Template.png", "FactionBackgrounds/Chaos/Slaanesh/Slaanesh_Weapon_Banner.png"),
    "helsmiths_of_hashut": FactionTheme("helsmiths_of_hashut", "Helsmiths of Hashut", "Chaos", "FactionBackgrounds/Chaos/Hashut/SonsOfHashut_Warscroll_Template.png", "FactionBackgrounds/Chaos/Hashut/SonsOfHashut_Weapon_Banner.png"),
    "idoneth_deepkin": FactionTheme("idoneth_deepkin", "Idoneth Deepkin", "Order", "FactionBackgrounds/Order/Idoneth/Idoneth_Warscroll_Template.png", "FactionBackgrounds/Order/Idoneth/Idoneth_Weapon_Banner.png"),
    "kharadron_overlords": FactionTheme("kharadron_overlords", "Kharadron Overlords", "Order", "FactionBackgrounds/Order/Kharadron/Kharadron_Warscroll_Template.png", "FactionBackgrounds/Order/Kharadron/Kharadron_Weapon_Banner.png"),
    "lumineth_realm_lords": FactionTheme("lumineth_realm_lords", "Lumineth Realm-Lords", "Order", "FactionBackgrounds/Order/Lumineth/Lumineth_Warscroll_Template.png", "FactionBackgrounds/Order/Lumineth/Lumineth_Weapon_Banner.png"),
    "maggotkin_of_nurgle": FactionTheme("maggotkin_of_nurgle", "Maggotkin of Nurgle", "Chaos", "FactionBackgrounds/Chaos/Nurgle/Nurgle_Warscroll_Template.png", "FactionBackgrounds/Chaos/Nurgle/Nurgle_Weapon_Banner.png"),
    "nighthaunt": FactionTheme("nighthaunt", "Nighthaunt", "Death", "FactionBackgrounds/Death/Nighthaunt/Nighthaunt_Warscroll_Template.png", "FactionBackgrounds/Death/Nighthaunt/Nighthaunt_Weapon_Banner.png"),
    "ogor_mawtribes": FactionTheme("ogor_mawtribes", "Ogor Mawtribes", "Destruction", "FactionBackgrounds/Destruction/Ogors/Ogors_Warscroll_Template.png", "FactionBackgrounds/Destruction/Ogors/Ogors_Weapon_Banner.png"),
    "orruk_warclans": FactionTheme("orruk_warclans", "Orruk Warclans", "Destruction", "FactionBackgrounds/Destruction/Orruks/Orruks_Warscroll_Template.png", "FactionBackgrounds/Destruction/Orruks/Orruks_Weapon_Banner.png"),
    "ossiarch_bonereapers": FactionTheme("ossiarch_bonereapers", "Ossiarch Bonereapers", "Death", "FactionBackgrounds/Death/OBR/OBR_Warscroll_Template.png", "FactionBackgrounds/Death/Nighthaunt/Nighthaunt_Weapon_Banner.png"),
    "seraphon": FactionTheme("seraphon", "Seraphon", "Order", "FactionBackgrounds/Order/Seraphon/Seraphon_Warscroll_Template.png", "FactionBackgrounds/Order/Seraphon/Seraphon_Weapon_Banner.png"),
    "skaven": FactionTheme("skaven", "Skaven", "Chaos", "FactionBackgrounds/Chaos/Skaven/Skaven_Warscroll_Template.png", "FactionBackgrounds/Chaos/Skaven/Skaven_Weapon_Banner.png"),
    "slaves_to_darkness": FactionTheme("slaves_to_darkness", "Slaves to Darkness", "Chaos", "FactionBackgrounds/Chaos/Slaves/Slaves_Warscroll_Template.png", "FactionBackgrounds/Chaos/Slaves/Slaves_Weapon_Banner.png"),
    "sons_of_behemat": FactionTheme("sons_of_behemat", "Sons of Behemat", "Destruction", "FactionBackgrounds/Destruction/Gargants/Gargants_Warscroll_Template.png", "FactionBackgrounds/Destruction/Gargants/Gargants_Weapon_Banner.png"),
    "soulblight_gravelords": FactionTheme("soulblight_gravelords", "Soulblight Gravelords", "Death", "FactionBackgrounds/Death/SBGL/SBGL_Warscroll_Template.png", "FactionBackgrounds/Death/FE/FE_Weapon_Banner.png"),
    "stormcast_eternals": FactionTheme("stormcast_eternals", "Stormcast Eternals", "Order", "FactionBackgrounds/Order/Stormcast/Stormcast_Warscroll_Template.png", "FactionBackgrounds/Order/Stormcast/Stormcast_Weapon_Banner.png"),
    "sylvaneth": FactionTheme("sylvaneth", "Sylvaneth", "Order", "FactionBackgrounds/Order/Sylvaneth/Sylvaneth_Warscroll_Template.png", "FactionBackgrounds/Order/Sylvaneth/Sylvaneth_Weapon_Banner.png"),
}

DEFAULT_FACTION_ID = "stormcast_eternals"
ALLIANCE_ORDER = ("Order", "Chaos", "Death", "Destruction")

ABILITY_PHASES = {
    "start_deployment": {"label": "Start of Turn", "banner_path": "Banners/Ability_Banner_StartDeploy.png", "line_color": "black"},
    "hero": {"label": "Hero Phase", "banner_path": "Banners/Ability_Banner_Hero.png", "line_color": "darkgoldenrod"},
    "move": {"label": "Movement Phase", "banner_path": "Banners/Ability_Banner_Movement.png", "line_color": "gray"},
    "shoot": {"label": "Shooting Phase", "banner_path": "Banners/Ability_Banner_Shooting.png", "line_color": "darkblue"},
    "charge": {"label": "Charge Phase", "banner_path": "Banners/Ability_Banner_Charge.png", "line_color": "#A36303"},
    "combat": {"label": "Combat Phase", "banner_path": "Banners/Ability_Banner_Combat.png", "line_color": "darkred"},
    "end": {"label": "End of Turn", "banner_path": "Banners/Ability_Banner_EndOfTurn.png", "line_color": "indigo"},
    "defensive": {"label": "Defensive", "banner_path": "Banners/Ability_Banner_Defensive.png", "line_color": "darkgreen"},
}

ABILITY_TYPES = {
    "standard": {"label": "Standard", "icon_path": "", "text_color": "white"},
    "command": {"label": "Command", "icon_path": "Icons/CommandIcon.png", "text_color": "black"},
    "prayer": {"label": "Prayer", "icon_path": "Icons/PrayerIcon.png", "text_color": "white"},
    "spell": {"label": "Spell", "icon_path": "Icons/SpellIcon.png", "text_color": "white"},
}

ABILITY_ICONS = {
    "none": {"label": "None", "path": ""},
    "battle_damaged": {"label": "Battle Damaged", "path": "Icons/BattleDamaged_AbilityIcon.png"},
    "control": {"label": "Control", "path": "Icons/ControlIcon.png"},
    "defensive": {"label": "Defensive", "path": "Icons/DefensiveIcon.png"},
    "movement": {"label": "Movement", "path": "Icons/MovementIcon.png"},
    "offensive": {"label": "Offensive", "path": "Icons/OffensiveIcon.png"},
    "rallying": {"label": "Rallying", "path": "Icons/RallyingIcon.png"},
    "shooting": {"label": "Shooting", "path": "Icons/ShootingIcon.png"},
    "special": {"label": "Special", "path": "Icons/SpecialIcon.png"},
}

ABILITY_RESTRICTIONS = (
    "",
    "Once Per Turn",
    "Once Per Turn (Army)",
    "Once Per Battle",
    "Once Per Battle (Army)",
)

ABILITY_TIMINGS = (
    "",
    "Any Charge Phase",
    "Any Combat Phase",
    "Any Hero Phase",
    "Any Movement Phase",
    "Any Shooting Phase",
    "Deployment Phase",
    "End of Any Turn",
    "End of Enemy Turn",
    "End of Your Turn",
    "Enemy Charge Phase",
    "Enemy Combat Phase",
    "Enemy Hero Phase",
    "Enemy Movement Phase",
    "Enemy Shooting Phase",
    "Passive",
    "Reaction: Opponent declared a Spell ability",
    "Reaction: Opponent declared an ATTACK ability",
    "Reaction: This unit was picked as the target of a non-Core ability",
    "Reaction: You declared a Charge ability for this unit",
    "Reaction: You declared a Fight ability for this unit",
    "Reaction: You declared an ATTACK ability",
    "Start of Any Turn",
    "Start of Enemy Turn",
    "Start of Your Turn",
    "Your Charge Phase",
    "Your Combat Phase",
    "Your Hero Phase",
    "Your Movement Phase",
    "Your Shooting Phase",
)

ABILITY_KEYWORDS = (
    "Attack",
    "Banish",
    "Charge",
    "Core",
    "Deploy",
    "Deploy Terrain",
    "Fight",
    "Honour Guard",
    "Move",
    "Prayer",
    "Rampage",
    "Retreat",
    "Run",
    "Shoot",
    "Spell",
    "Summon",
    "Unbind",
    "Unlimited",
)

KEYWORD_ABILITY_OPTIONS = (
    "Beast",
    "Cavalry",
    "Champion",
    "Champion (1/10)",
    "Champion (1/5)",
    "Champion (1/8)",
    "Champion (1/9)",
    "Endless Spell",
    "Faction Terrain",
    "Fly",
    "Hero",
    "Infantry",
    "Invocation",
    "Manifestation",
    "Monster",
    "Musician (1/10)",
    "Musician (1/20)",
    "Musician (1/3)",
    "Musician (1/4)",
    "Musician (1/5)",
    "Musician (1/6)",
    "Priest (1)",
    "Priest (2)",
    "Priest (3)",
    "Priest (4)",
    "Reinforcements",
    "Standard bearer (1/10)",
    "Standard bearer (1/20)",
    "Standard bearer (1/3)",
    "Standard bearer (1/5)",
    "Standard bearer (1/6)",
    "Unique",
    "Ward (2+)",
    "Ward (3+)",
    "Ward (4+)",
    "Ward (5+)",
    "Ward (6+)",
    "War Machine",
    "Warmaster",
    "Wizard (1)",
    "Wizard (2)",
    "Wizard (3)",
)

KEYWORD_IDENTITY_OPTIONS = (
    "Abhorrant",
    "Aelf",
    "Akhelian",
    "Alarith",
    "Arcanite",
    "Beast-Smasher",
    "Beastclaw Raiders",
    "Beasts of Chaos",
    "Blades of Khorne",
    "Bonesplittaz",
    "Chaos",
    "Cities of Sigmar",
    "Daemon",
    "Darkoath",
    "Daughters of Khaine",
    "Death",
    "Destruction",
    "Disciples of Tzeentch",
    "Duardin",
    "Flesh-Eater Courts",
    "Fyreslayers",
    "Gargant",
    "Gloomspite Gitz",
    "Hedonites of Slaanesh",
    "Helsmiths of Hashut",
    "Human",
    "Idoneth Deepkin",
    "Ironjawz",
    "Kharadron Overlords",
    "Kruleboyz",
    "Lumineth Realm-Lords",
    "Maggotkin of Nurgle",
    "Nighthaunt",
    "Ogor Mawtribes",
    "Order",
    "Orruk Warclans",
    "Ossiarch Bonereapers",
    "Priest",
    "Seraphon",
    "Skaven",
    "Slaves to Darkness",
    "Sons of Behemat",
    "Soulblight Gravelords",
    "Stormcast Eternals",
    "Sylvaneth",
    "Warrior Chamber",
    "Wizard",
)

LEGACY_TEMPLATE_TO_FACTION_ID = {theme.template_path: theme.id for theme in FACTIONS.values()}
LEGACY_BANNER_TO_FACTION_ID = {theme.weapon_banner_path: theme.id for theme in FACTIONS.values()}
LEGACY_ABILITY_BANNER_TO_PHASE = {config["banner_path"]: key for key, config in ABILITY_PHASES.items()}
LEGACY_ABILITY_ICON_TO_ID = {config["path"]: key for key, config in ABILITY_ICONS.items() if config["path"]}
LEGACY_ABILITY_TYPE_ICON_TO_ID = {config["icon_path"]: key for key, config in ABILITY_TYPES.items() if config["icon_path"]}


def get_faction(faction_id: str) -> FactionTheme:
    return FACTIONS.get(faction_id, FACTIONS[DEFAULT_FACTION_ID])


def asset_url(asset_base_url: str, asset_path: str) -> str:
    if not asset_path:
        return ""
    return f"{asset_base_url.rstrip('/')}/{asset_path.lstrip('/')}"
