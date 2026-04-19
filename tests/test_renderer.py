from __future__ import annotations

import unittest

from warscroll_app.models import WarscrollPayload
from warscroll_app.renderer import render_warscroll_fragment


class RendererTests(unittest.TestCase):
    def test_renderer_returns_embeddable_fragment(self) -> None:
        payload = WarscrollPayload.from_dict(
            {
                "faction_id": "stormcast_eternals",
                "warscroll_name": "Liberators",
                "warscroll_subtype": "With Warhammers",
                "move": "5",
                "health": "2",
                "control": "1",
                "save": "4+",
                "keyword_abilities": ["Infantry", "Ward (6+)"],
                "keyword_identities": ["Order", "Stormcast Eternals"],
                "ranged_weapons": [
                    {
                        "name": "Boltstorm Pistol",
                        "range": "10",
                        "atk": "2",
                        "to_hit": "3+",
                        "to_wound": "4+",
                        "rend": "1",
                        "damage": "1",
                        "ability": "Crit (Mortal)",
                    }
                ],
                "abilities": [
                    {
                        "name": "Lay Low the Tyrants",
                        "name_desc": "Add 1 to wound rolls.",
                        "effect_desc": "If the target is a Monster, add 1 damage instead.",
                        "keywords": ["Attack"],
                        "phase": "combat",
                        "timing": "Your Combat Phase",
                    }
                ],
            }
        )

        fragment = render_warscroll_fragment(payload)

        self.assertIn('class="warscroll-card"', fragment)
        self.assertIn("LIBERATORS", fragment)
        self.assertIn("Boltstorm Pistol", fragment)
        self.assertIn("LAY LOW THE TYRANTS", fragment)
        self.assertIn(
            "/static/FactionBackgrounds/Order/Stormcast/Stormcast_Warscroll_Template.png",
            fragment,
        )

    def test_legacy_state_import_maps_to_canonical_payload(self) -> None:
        payload = WarscrollPayload.from_any_dict(
            {
                "faction": {
                    "factionTemplate": "FactionBackgrounds/Order/Stormcast/Stormcast_Warscroll_Template.png",
                    "customFactionName": "My Host",
                },
                "characteristics": {
                    "warscrollName": "Judicators",
                    "warscrollSubtype": "Prime",
                    "warscrollMove": "5",
                    "warscrollHealth": "2",
                    "warscrollControl": "1",
                    "warscrollSave": "4+",
                },
                "weapons": {
                    "rangedWeaponStats": [
                        {
                            "name": "Skybolt Bow",
                            "range": "24",
                            "atk": "2",
                            "toHit": "3+",
                            "toWound": "3+",
                            "rend": "1",
                            "damage": "1",
                            "ability": "Crit (2 Hits)",
                            "isBattleDamaged": True,
                            "isOverride": True,
                            "override": [
                                {
                                    "range": False,
                                    "atk": False,
                                    "toHit": True,
                                    "toWound": True,
                                    "rend": False,
                                    "damage": False,
                                }
                            ],
                        }
                    ]
                },
                "abilities": {
                    "abilities": [
                        {
                            "name": "Thunderbolt Volley",
                            "effect_desc": "Pick an enemy unit and deal D3 mortal damage.",
                            "ability_banner": "Banners/Ability_Banner_Shooting.png",
                            "ability_timing": "Your Shooting Phase",
                            "ability_icon_path": "Icons/ShootingIcon.png",
                        }
                    ]
                },
                "loadout": {
                    "body": "One model can be a Prime.",
                    "points": ["Prime has +1 attack."],
                },
                "keywords": {
                    "keywordAbilities": ["Infantry"],
                    "keywordIdentities": ["Order", "Stormcast Eternals"],
                },
            }
        )

        self.assertEqual(payload.faction_id, "stormcast_eternals")
        self.assertEqual(payload.custom_faction_name, "My Host")
        self.assertEqual(
            payload.ranged_weapons[0].override_fields, ["to_hit", "to_wound"]
        )
        self.assertEqual(payload.abilities[0].phase, "shoot")
        self.assertEqual(payload.abilities[0].icon, "shooting")


if __name__ == "__main__":
    unittest.main()
