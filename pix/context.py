"""Semantic properties decoded from the current Lua cells and icon tiles."""

import numpy as np

from pix.matrix import Matrix


class Context:
    def __init__(self, matrix: Matrix) -> None:
        self.matrix = matrix

    def readBooleanCell(self, x: int) -> bool:
        return self.matrix.getCell(x).is_white

    def readPercentCell(self, x: int) -> float:
        return self.matrix.getCell(x).percent

    def readNumberCell(self, x: int) -> float:
        return self.matrix.getCell(x).mean

    def readValueBarCell(self, x: int, width: int, max_value: float) -> float:
        return self.matrix.getValueBar(x, width).ratio * max_value

    def readSpellCDCell(self, x: int) -> float:
        return float(np.interp(self.matrix.getCell(x).mean, (0, 25, 115, 155, 255), (245, 120, 30, 10, 0)))

    def readAuraDurationCell(self, x: int) -> float:
        return float(np.interp(self.matrix.getCell(x).mean, (0, 150, 180, 210, 255), (0, 15, 30, 60, 240)))

    def readIconTile(self, x: int) -> str | None:
        return self.matrix.getIconTile(x).hash

    @property
    def enable(self) -> bool:
        return self.readBooleanCell(1)

    @property
    def in_burst(self) -> bool:
        return self.readBooleanCell(2)

    @property
    def delaying(self) -> bool:
        return self.readBooleanCell(3)

    @property
    def player_is_alive(self) -> bool:
        return self.readBooleanCell(4)

    @property
    def player_health_pct(self) -> float:
        return self.readPercentCell(5)

    @property
    def power_holy_power(self) -> int:
        return int(self.readNumberCell(6) + 0.5)

    @property
    def force_single_target(self) -> bool:
        return self.readBooleanCell(7)

    @property
    def player_in_combat(self) -> bool:
        return self.readBooleanCell(8)

    @property
    def player_is_player_target(self) -> bool:
        return self.readBooleanCell(9)

    @property
    def player_is_moving(self) -> bool:
        return self.readBooleanCell(10)

    @property
    def player_in_vehicle(self) -> bool:
        return self.readBooleanCell(11)

    @property
    def player_is_targeting_spell(self) -> bool:
        return self.readBooleanCell(12)

    @property
    def player_is_chatting(self) -> bool:
        return self.readBooleanCell(13)

    @property
    def ticket_13_ready(self) -> bool:
        return self.readBooleanCell(14)

    @property
    def ticket_14_ready(self) -> bool:
        return self.readBooleanCell(15)

    @property
    def healthstone_ready(self) -> bool:
        return self.readBooleanCell(16)

    @property
    def heal_potion_ready(self) -> bool:
        return self.readBooleanCell(17)

    @property
    def player_has_heal_absorb(self) -> bool:
        return self.readBooleanCell(18)

    @property
    def player_has_damage_absorb(self) -> bool:
        return self.readBooleanCell(19)

    @property
    def player_cast_progress(self) -> float:
        return self.readPercentCell(20)

    @property
    def player_is_empowering(self) -> bool:
        return self.readBooleanCell(21)

    @property
    def target_is_exists(self) -> bool:
        return self.readBooleanCell(22)

    @property
    def target_is_alive(self) -> bool:
        return self.readBooleanCell(23)

    @property
    def target_can_attack(self) -> bool:
        return self.readBooleanCell(24)

    @property
    def target_can_assist(self) -> bool:
        return self.readBooleanCell(25)

    @property
    def target_health_pct(self) -> float:
        return self.readPercentCell(26)

    @property
    def target_cast_interruptible(self) -> bool:
        if not self.readBooleanCell(27):
            return False
        icon = self.target_cast_icon
        return icon is not None and icon not in self.interrupt_blacklist

    @property
    def target_cast_progress(self) -> float:
        return self.readPercentCell(28)

    @property
    def target_in_melee_range(self) -> bool:
        return self.readBooleanCell(29)

    @property
    def target_in_ranged_range(self) -> bool:
        return self.readBooleanCell(30)

    @property
    def target_in_interrupt_range(self) -> bool:
        return self.readBooleanCell(31)

    @property
    def focus_is_exists(self) -> bool:
        return self.readBooleanCell(32)

    @property
    def focus_is_alive(self) -> bool:
        return self.readBooleanCell(33)

    @property
    def focus_can_attack(self) -> bool:
        return self.readBooleanCell(34)

    @property
    def focus_can_assist(self) -> bool:
        return self.readBooleanCell(35)

    @property
    def focus_health_pct(self) -> float:
        return self.readPercentCell(36)

    @property
    def focus_cast_interruptible(self) -> bool:
        if not self.readBooleanCell(37):
            return False
        icon = self.focus_cast_icon
        return icon is not None and icon not in self.interrupt_blacklist

    @property
    def focus_cast_progress(self) -> float:
        return self.readPercentCell(38)

    @property
    def focus_in_melee_range(self) -> bool:
        return self.readBooleanCell(39)

    @property
    def focus_in_ranged_range(self) -> bool:
        return self.readBooleanCell(40)

    @property
    def focus_in_interrupt_range(self) -> bool:
        return self.readBooleanCell(41)

    @property
    def spell_cd_global_cooldown(self) -> float:
        return self.readSpellCDCell(42)

    @property
    def spell_cd_rebuke(self) -> float:
        return self.readSpellCDCell(43)

    @property
    def spell_cd_avenging_wrath(self) -> float:
        return self.readSpellCDCell(44)

    @property
    def spell_cd_execution_sentence(self) -> float:
        return self.readSpellCDCell(45)

    @property
    def spell_cd_wake_of_ashes(self) -> float:
        return self.readSpellCDCell(46)

    @property
    def spell_cd_blade_of_justice(self) -> float:
        return self.readSpellCDCell(47)

    @property
    def spell_cd_divine_toll(self) -> float:
        return self.readSpellCDCell(51)

    @property
    def spell_cd_lay_on_hands(self) -> float:
        return self.readSpellCDCell(52)

    @property
    def spell_cd_divine_shield(self) -> float:
        return self.readSpellCDCell(53)

    @property
    def spell_charges_judgment(self) -> int:
        """Grayscale charge count (0–2); 0 also includes missing data."""
        return int(self.readNumberCell(48) + 0.5)

    @property
    def item_cd_lights_potential(self) -> bool:
        return self.readBooleanCell(54)

    @property
    def player_has_buff_avenging_wrath(self) -> bool:
        return self.readBooleanCell(55)

    @property
    def player_has_buff_divine_purpose(self) -> bool:
        return self.readBooleanCell(56)

    @property
    def player_has_buff_dawnlight(self) -> bool:
        return self.readBooleanCell(57)

    @property
    def player_has_buff_art_of_war(self) -> bool:
        return self.readBooleanCell(58)

    @property
    def player_has_buff_divine_arbiter_storm(self) -> bool:
        return self.readBooleanCell(59)

    @property
    def four_piece_enabled(self) -> bool:
        return self.readBooleanCell(60)

    @property
    def target_in_blade_of_justice_range(self) -> bool:
        return self.readBooleanCell(61)

    @property
    def target_in_judgment_range(self) -> bool:
        return self.readBooleanCell(62)

    @property
    def target_in_hammer_of_justice_range(self) -> bool:
        return self.readBooleanCell(63)

    @property
    def player_has_dispellable_poison_or_disease(self) -> bool:
        return self.readBooleanCell(64)

    @property
    def spell_cd_cleanse_toxins(self) -> float:
        return self.readSpellCDCell(65)

    @property
    def auto_cleanse_enabled(self) -> bool:
        return self.readBooleanCell(66)

    @property
    def auto_trinket_enabled(self) -> bool:
        return self.readBooleanCell(67)

    @property
    def mouseover_in_melee_range(self) -> bool:
        return self.readBooleanCell(49)

    @property
    def burst_potion_enabled(self) -> bool:
        return self.readBooleanCell(50)

    @property
    def player_melee_enemies_count(self) -> int:
        """Observable living enemies within Hammer of Justice range (0–40)."""
        return int(self.matrix.getCell(68).ratio * 40 + 0.5)

    @property
    def player_cast_icon(self) -> str | None:
        return self.readIconTile(1)

    @property
    def assisted_combat_icon(self) -> str | None:
        return self.readIconTile(2)

    @property
    def target_cast_icon(self) -> str | None:
        return self.readIconTile(3)

    @property
    def focus_cast_icon(self) -> str | None:
        return self.readIconTile(4)

    @property
    def interrupt_blacklist(self) -> list[str]:
        return [icon for x in range(5, 20) if (icon := self.readIconTile(x)) is not None]
