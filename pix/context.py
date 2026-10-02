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
    def power_focus_pct(self) -> float:
        return self.readPercentCell(6)

    @property
    def attack_mode(self) -> int:
        return int(self.readNumberCell(7) + 0.5)

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
    def spell_cd_counter_shot(self) -> float:
        return self.readSpellCDCell(43)

    @property
    def spell_cd_bestial_wrath(self) -> float:
        return self.readSpellCDCell(44)

    @property
    def spell_cd_wild_thrash(self) -> float:
        return self.readSpellCDCell(45)

    @property
    def spell_cd_kill_command(self) -> float:
        return self.readSpellCDCell(46)

    @property
    def spell_cd_barbed_shot(self) -> float:
        return self.readSpellCDCell(47)

    @property
    def spell_charges_barbed_shot(self) -> int:
        return int(self.readNumberCell(48) + 0.5)

    @property
    def mouseover_in_melee_range(self) -> bool:
        return self.readBooleanCell(49)

    @property
    def mouseover_in_interrupt_range(self) -> bool:
        return self.readBooleanCell(49)

    @property
    def burst_potion_enabled(self) -> bool:
        return self.readBooleanCell(50)

    @property
    def spell_cd_mend_pet(self) -> float:
        return self.readSpellCDCell(51)

    @property
    def spell_cd_exhilaration(self) -> float:
        return self.readSpellCDCell(52)

    @property
    def spell_cd_misdirection(self) -> float:
        return self.readSpellCDCell(53)

    @property
    def reckless_potion_ready(self) -> bool:
        return self.readBooleanCell(54)

    @property
    def player_has_buff_pack_wyvern(self) -> bool:
        return self.readBooleanCell(55)

    @property
    def player_has_buff_natures_ally(self) -> bool:
        # 玩家是否存在自然之友（Nature’s Ally，1276720）增益。
        return self.readBooleanCell(56)

    @property
    def player_has_buff_pack_boar(self) -> bool:
        return self.readBooleanCell(57)

    @property
    def player_has_buff_pack_bear(self) -> bool:
        return self.readBooleanCell(58)

    @property
    def player_has_buff_cobra_fangs(self) -> bool:
        return self.readBooleanCell(59)

    @property
    def finishing(self) -> bool:
        return self.readBooleanCell(60)

    @property
    def power_focus_max(self) -> int:
        return int(self.readNumberCell(61) + 0.5)

    @property
    def pet_is_exists(self) -> bool:
        return self.readBooleanCell(63)

    @property
    def pet_is_alive(self) -> bool:
        return self.readBooleanCell(64)

    @property
    def pet_health_pct(self) -> float:
        return self.readPercentCell(65)

    @property
    def party_tank_index(self) -> int:
        return int(self.readNumberCell(66) + 0.5)

    @property
    def auto_trinket_enabled(self) -> bool:
        return self.readBooleanCell(67)

    @property
    def player_in_party(self) -> bool:
        return self.readBooleanCell(69)

    @property
    def spell_known_misdirection(self) -> bool:
        return self.readBooleanCell(70)

    @property
    def party_tank_in_misdirection_range(self) -> bool:
        return self.readBooleanCell(71)

    @property
    def target_interrupt_enabled(self) -> bool:
        return self.readBooleanCell(72)

    @property
    def mouseover_interrupt_enabled(self) -> bool:
        return self.readBooleanCell(73)

    @property
    def spell_charges_kill_command(self) -> int:
        return int(self.readNumberCell(74) + 0.5)

    @property
    def spell_max_charges_barbed_shot(self) -> int:
        return int(self.readNumberCell(75) + 0.5)

    @property
    def player_has_buff_beast_cleave(self) -> bool:
        return self.readBooleanCell(76)

    @property
    def interrupt_progress_threshold(self) -> int:
        value = int(self.readNumberCell(77) + 0.5)
        return value if 10 <= value <= 90 else 30

    @property
    def mouseover_is_exists(self) -> bool:
        return self.readBooleanCell(78)

    @property
    def mouseover_is_alive(self) -> bool:
        return self.readBooleanCell(79)

    @property
    def mouseover_can_attack(self) -> bool:
        return self.readBooleanCell(80)

    @property
    def mouseover_can_assist(self) -> bool:
        return self.readBooleanCell(81)

    @property
    def mouseover_cast_interruptible(self) -> bool:
        if not self.readBooleanCell(82):
            return False
        icon = self.mouseover_cast_icon
        return icon is not None and icon not in self.interrupt_blacklist

    @property
    def mouseover_cast_progress(self) -> float:
        return self.readPercentCell(83)

    @property
    def player_has_buff_bestial_wrath(self) -> bool:
        return self.readBooleanCell(84)

    @property
    def player_buff_beast_cleave_remaining(self) -> float:
        return self.readAuraDurationCell(85)

    @property
    def power_focus(self) -> int:
        maximum = self.power_focus_max
        if not 100 <= maximum <= 120:
            return 0
        return int(self.power_focus_pct * maximum / 100.0 + 0.5)

    @property
    def spell_recharge_barbed_shot(self) -> float:
        maximum = self.spell_max_charges_barbed_shot
        if maximum > 0 and self.spell_charges_barbed_shot >= maximum:
            return 0.0
        return self.readSpellCDCell(62)

    @property
    def player_enemies_count(self) -> int:
        """Observable living, attackable, in-combat nameplates in Counter Shot range."""
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
    def mouseover_cast_icon(self) -> str | None:
        return self.readIconTile(20)

    @property
    def interrupt_blacklist(self) -> list[str]:
        return [icon for x in range(5, 20) if (icon := self.readIconTile(x)) is not None]
