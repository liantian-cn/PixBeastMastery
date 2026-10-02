"""猎群领袖兽王猎：按优先级执行第一个满足条件的动作。"""

from pix.action import Cast, Idle, Use
from pix.context import Context


class Rotation:
    def __init__(self) -> None:
        self.keymap: dict[str, str] = {
            "倒刺射击": "RCTRL-NUMPAD1",
            "焦点反制射击": "RCTRL-NUMPAD2",
            "目标反制射击": "RCTRL-NUMPAD3",
            "鼠标指向反制射击": "RSHIFT-NUMPAD0",
            "狂野怒火": "RCTRL-NUMPAD4",
            "狂野鞭笞": "RCTRL-NUMPAD5",
            "杀戮命令": "RCTRL-NUMPAD6",
            "眼镜蛇射击": "RCTRL-NUMPAD7",
            "鲁莽药水": "RCTRL-NUMPAD8",
            "治疗宠物": "RCTRL-NUMPAD9",
            "召唤/复活宠物": "RCTRL-NUMPAD0",
            "误导party1": "RSHIFT-NUMPAD1",
            "误导party2": "RSHIFT-NUMPAD2",
            "误导party3": "RSHIFT-NUMPAD3",
            "误导party4": "RSHIFT-NUMPAD4",
            "治疗石": "RSHIFT-NUMPAD5",
            "银月城生命药水": "RSHIFT-NUMPAD6",
            "意气风发": "RSHIFT-NUMPAD7",
            "上饰品": "RSHIFT-NUMPAD8",
            "下饰品": "RSHIFT-NUMPAD9",
        }

    def main_rotation(self, ctx: Context) -> Cast | Use | Idle:
        if not ctx.enable:
            return Idle("插件未启用")
        if ctx.delaying:
            return Idle("手动操作延迟中")
        if not ctx.player_is_alive:
            return Idle("玩家未存活")
        if ctx.player_in_vehicle or ctx.player_is_chatting or ctx.player_is_targeting_spell:
            return Idle("坐骑、载具、输入或地面选点中")
        if ctx.player_cast_progress > 0 or ctx.player_is_empowering:
            return Idle("玩家正在施法、引导或蓄力")

        # 宠物恢复优先于误导、战斗和目标门控。
        if not ctx.pet_is_exists or not ctx.pet_is_alive:
            if ctx.player_is_moving:
                return Idle("等待站定召唤或复活宠物")
            return Cast("召唤/复活宠物")

        if (not ctx.player_in_combat and ctx.player_in_party
                and ctx.spell_known_misdirection and ctx.spell_cd_misdirection == 0
                and 1 <= ctx.party_tank_index <= 4 and ctx.party_tank_in_misdirection_range):
            return Cast(f"误导party{ctx.party_tank_index}")
        if not ctx.player_in_combat:
            return Idle("玩家不在战斗")
        if not (ctx.target_is_exists and ctx.target_is_alive and ctx.target_can_attack):
            return Idle("目标不可攻击")

        if ctx.spell_cd_counter_shot == 0:
            # 三种打断共用已过进度阈值，按焦点、鼠标指向、目标依次判断。
            interrupt_progress = ctx.interrupt_progress_threshold
            if (ctx.focus_is_exists and ctx.focus_is_alive and ctx.focus_can_attack
                    and not ctx.focus_can_assist and ctx.focus_in_interrupt_range
                    and ctx.focus_cast_interruptible and ctx.focus_cast_progress > interrupt_progress):
                return Cast("焦点反制射击")
            if (ctx.mouseover_interrupt_enabled and ctx.mouseover_is_exists and ctx.mouseover_is_alive
                    and ctx.mouseover_can_attack and not ctx.mouseover_can_assist
                    and ctx.mouseover_in_interrupt_range and ctx.mouseover_cast_interruptible
                    and ctx.mouseover_cast_progress > interrupt_progress):
                return Cast("鼠标指向反制射击")
            if (ctx.target_interrupt_enabled and not ctx.target_can_assist and ctx.target_in_interrupt_range
                    and ctx.target_cast_interruptible and ctx.target_cast_progress > interrupt_progress):
                return Cast("目标反制射击")

        if ctx.player_health_pct <= 30 and ctx.healthstone_ready:
            return Use("治疗石")
        if ctx.player_health_pct <= 30 and ctx.heal_potion_ready:
            return Use("银月城生命药水")
        if ctx.player_health_pct <= 50 and ctx.spell_cd_exhilaration == 0:
            return Cast("意气风发")

        attack_range = ctx.target_in_interrupt_range
        if ctx.in_burst and attack_range:
            if ctx.burst_potion_enabled and ctx.reckless_potion_ready:
                return Use("鲁莽药水")
            if ctx.auto_trinket_enabled:
                if ctx.ticket_13_ready:
                    return Use("上饰品")
                if ctx.ticket_14_ready:
                    return Use("下饰品")

        IsAOE = ctx.player_enemies_count >= 2
        if ctx.attack_mode == 10:
            IsAOE = False
        elif ctx.attack_mode == 20:
            IsAOE = True

        if attack_range:
            focus = ctx.power_focus
            barbed_ready = ctx.spell_cd_barbed_shot == 0 and ctx.spell_charges_barbed_shot > 0
            thrash_cd = ctx.spell_cd_wild_thrash
            single_or_thrash_cooling = not IsAOE or thrash_cd > 0

            if IsAOE and focus >= 35 and thrash_cd == 0 and ctx.player_has_buff_bestial_wrath:
                return Cast("狂野鞭笞", "狂野怒火增益期间优先")
            if (IsAOE and ctx.spell_cd_bestial_wrath == 0 and not ctx.finishing
                    and ctx.player_has_buff_beast_cleave and thrash_cd < 1.5):
                return Cast("狂野怒火", "野兽顺劈期间优先")
            if barbed_ready and (ctx.spell_recharge_barbed_shot < 2
                                 or (not IsAOE and ctx.spell_cd_bestial_wrath < 3)):
                return Cast("倒刺射击", "充能将满或单体怒火将就绪")
            if IsAOE and focus >= 35 and thrash_cd == 0:
                return Cast("狂野鞭笞")
            if not IsAOE and not ctx.finishing and ctx.spell_cd_bestial_wrath == 0:
                return Cast("狂野怒火")
            # 杀戮命令要求自然之友增益存在。
            if (focus >= 30 and ctx.spell_cd_kill_command == 0 and ctx.spell_charges_kill_command > 0
                    and ctx.player_has_buff_natures_ally):
                return Cast("杀戮命令")
            if focus >= 35 and ctx.player_has_buff_cobra_fangs and single_or_thrash_cooling:
                return Cast("眼镜蛇射击", "眼镜蛇利牙")
            if barbed_ready:
                return Cast("倒刺射击")
            if focus >= 35 and single_or_thrash_cooling:
                return Cast("眼镜蛇射击")

        if ctx.pet_is_exists and ctx.pet_is_alive and ctx.pet_health_pct < 70 and ctx.spell_cd_mend_pet == 0:
            return Cast("治疗宠物")
        return Idle("没有满足条件的动作")
