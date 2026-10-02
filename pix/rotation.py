"""烈日先驱惩戒骑战斗优先级：从上到下判断，执行首个满足条件的动作。"""

from pix.action import Cast, Idle, Use
from pix.context import Context


class Rotation:
    def __init__(self) -> None:
        self.keymap: dict[str, str] = {
            "最终审判": "RCTRL-NUMPAD1",
            "焦点责难": "RCTRL-NUMPAD2",
            "目标责难": "RCTRL-NUMPAD3",
            "复仇之怒": "RCTRL-NUMPAD4",
            "处决宣判": "RCTRL-NUMPAD5",
            "灰烬觉醒": "RCTRL-NUMPAD6",
            "公正之剑": "RCTRL-NUMPAD7",
            "圣光潜力": "RCTRL-NUMPAD8",
            "审判": "RCTRL-NUMPAD9",
            "神圣风暴": "RCTRL-NUMPAD0",
            "圣洁鸣钟": "RSHIFT-NUMPAD1",
            "圣疗术": "RSHIFT-NUMPAD2",
            "圣盾术": "RSHIFT-NUMPAD3",
            "荣耀圣令": "RSHIFT-NUMPAD4",
            "治疗石": "RSHIFT-NUMPAD5",
            "银月城生命药水": "RSHIFT-NUMPAD6",
            "清毒术": "RSHIFT-NUMPAD7",
            "上饰品": "RSHIFT-NUMPAD8",
            "下饰品": "RSHIFT-NUMPAD9",
        }

    def main_rotation(self, ctx: Context) -> Cast | Use | Idle:
        # 如果 插件未启用
        # => 不执行动作
        if not ctx.enable:
            return Idle("插件未启用")

        # 如果 处于手动操作后的延迟窗口
        # => 不执行动作，等待手动操作结束
        if ctx.delaying:
            return Idle("手动操作延迟中")

        # 如果 玩家未存活
        # => 不执行动作
        if not ctx.player_is_alive:
            return Idle("玩家未存活")

        # 如果 玩家不在战斗
        # => 不执行动作
        if not ctx.player_in_combat:
            return Idle("玩家不在战斗")

        # 如果 玩家在载具中、正在输入聊天或选择地面施法位置（任一条件成立）
        # => 不执行动作
        if ctx.player_in_vehicle or ctx.player_is_chatting or ctx.player_is_targeting_spell:
            return Idle("载具、输入或地面选点中")

        # 如果 玩家正在施法、引导或蓄力
        # => 不执行动作
        if ctx.player_cast_progress > 0 or ctx.player_is_empowering:
            return Idle("玩家正在施法、引导或蓄力")

        # 如果 目标不存在、已死亡或不可攻击（任一条件成立）
        # => 不执行动作
        if not (ctx.target_is_exists and ctx.target_is_alive and ctx.target_can_attack):
            return Idle("目标不可攻击")

        # 如果 责难冷却就绪
        # => 优先检查焦点打断，再检查目标打断
        if ctx.spell_cd_rebuke == 0:
            # 如果 焦点存在且存活、可攻击且不可被援助
            # 如果 焦点在打断范围内，且施法满足打断条件
            # => 对焦点施放 责难
            if (ctx.focus_is_exists and ctx.focus_is_alive and ctx.focus_can_attack
                    and not ctx.focus_can_assist and ctx.focus_in_interrupt_range
                    and ctx.focus_cast_interruptible):
                return Cast("焦点责难")

            # 如果 目标不可被援助，在打断范围内且施法满足打断条件
            # => 对目标施放 责难
            if (not ctx.target_can_assist and ctx.target_in_interrupt_range
                    and ctx.target_cast_interruptible):
                return Cast("目标责难")

        holy_power = ctx.power_holy_power

        # 如果 玩家生命值不高于 20%，且圣疗术冷却就绪
        # => 施放 圣疗术
        if ctx.player_health_pct <= 20 and ctx.spell_cd_lay_on_hands == 0:
            return Cast("圣疗术")

        # 如果 玩家生命值不高于 15%，且圣盾术冷却就绪
        # => 施放 圣盾术
        if ctx.player_health_pct <= 15 and ctx.spell_cd_divine_shield == 0:
            return Cast("圣盾术")

        # 如果 玩家生命值不高于 60%，且圣能不少于 3 点
        # => 施放 荣耀圣令
        if ctx.player_health_pct <= 60 and holy_power >= 3:
            return Cast("荣耀圣令")

        # 如果 玩家生命值不高于 30%，且治疗石可用
        # => 使用 治疗石
        if ctx.player_health_pct <= 30 and ctx.healthstone_ready:
            return Use("治疗石")

        # 如果 玩家生命值不高于 30%，且治疗药水可用
        # => 使用 银月城生命药水
        if ctx.player_health_pct <= 30 and ctx.heal_potion_ready:
            return Use("银月城生命药水")

        # 如果 自动清毒开启，玩家有可驱散的中毒或疾病效果
        # 如果 清毒术冷却就绪
        # => 施放 清毒术
        if (ctx.auto_cleanse_enabled and ctx.player_has_dispellable_poison_or_disease
                and ctx.spell_cd_cleanse_toxins == 0):
            return Cast("清毒术")

        # 如果 独立爆发药水开关开启，且圣光潜力药水可用
        # => 使用 圣光潜力药水
        if ctx.burst_potion_enabled and ctx.item_cd_lights_potential:
            return Use("圣光潜力")

        # 以下进攻规则使用制裁之锤射程判断目标是否在攻击范围内。
        attack_range = ctx.target_in_hammer_of_justice_range

        # 如果 自动饰品开启，处于爆发状态且目标在攻击范围内
        if ctx.auto_trinket_enabled and ctx.in_burst and attack_range:
            # 如果 上饰品可用
            # => 使用 上饰品
            if ctx.ticket_13_ready:
                return Use("上饰品")
            # 如果 下饰品可用
            # => 使用 下饰品
            if ctx.ticket_14_ready:
                return Use("下饰品")

        wings = ctx.player_has_buff_avenging_wrath

        # 如果 复仇之怒冷却就绪，且处于爆发状态
        # => 施放 复仇之怒
        if ctx.spell_cd_avenging_wrath == 0 and ctx.in_burst:
            return Cast("复仇之怒")

        # 如果 处决宣判冷却就绪，玩家有复仇之怒增益且目标在攻击范围内
        # => 施放 处决宣判
        if ctx.spell_cd_execution_sentence == 0 and wings and attack_range:
            return Cast("处决宣判")

        # 多目标：未强制单体，且玩家近战范围内敌人不少于 2 个。
        # 单体：已强制单体，或玩家近战范围内恰有 1 个敌人。
        enemies = ctx.player_melee_enemies_count
        multi_target = not ctx.force_single_target and enemies >= 2
        single_target = ctx.force_single_target or enemies == 1
        # 四件套触发：四件套开关开启，有神圣意志增益且没有神圣仲裁风暴增益。
        four_piece_proc = (ctx.four_piece_enabled and ctx.player_has_buff_divine_purpose
                           and not ctx.player_has_buff_divine_arbiter_storm)

        # 如果 满足四件套触发条件
        if four_piece_proc:
            # 如果 处于多目标条件，且目标在攻击范围内
            # => 施放 最终审判
            if multi_target and attack_range:
                return Cast("最终审判", "四件套多目标触发")
            # 如果 处于单体条件，且目标在攻击范围内
            # => 施放 神圣风暴
            if single_target and attack_range:
                return Cast("神圣风暴", "四件套单体触发")

        # 如果 圣能不少于 4 点
        if holy_power >= 4:
            # 如果 处于多目标条件，且目标在攻击范围内
            # => 施放 神圣风暴
            if multi_target and attack_range:
                return Cast("神圣风暴", "至少4圣能")
            # 如果 处于单体条件，且目标在攻击范围内
            # => 施放 最终审判
            if single_target and attack_range:
                return Cast("最终审判", "至少4圣能")

        # 如果 灰烬觉醒冷却就绪，圣能不多于 2 点且目标在攻击范围内
        # => 施放 灰烬觉醒
        if ctx.spell_cd_wake_of_ashes == 0 and holy_power <= 2 and attack_range:
            return Cast("灰烬觉醒")

        # 如果 圣能不少于 3 点，且玩家有晨光增益
        if holy_power >= 3 and ctx.player_has_buff_dawnlight:
            # 如果 处于多目标条件，且目标在攻击范围内
            # => 施放 神圣风暴
            if multi_target and attack_range:
                return Cast("神圣风暴", "晨光")
            # 如果 处于单体条件，且目标在攻击范围内
            # => 施放 最终审判
            if single_target and attack_range:
                return Cast("最终审判", "晨光")

        # 如果 圣洁鸣钟冷却就绪，玩家有复仇之怒增益且目标在攻击范围内
        # => 施放 圣洁鸣钟
        if ctx.spell_cd_divine_toll == 0 and wings and attack_range:
            return Cast("圣洁鸣钟")
        judgment_ready = ctx.spell_charges_judgment
        blade_ready = ctx.spell_cd_blade_of_justice == 0

        # 如果 审判充能为 2 层，且圣能不多于 2 点
        # 如果 处于多目标条件，且目标在攻击范围内
        # => 施放 审判
        if judgment_ready == 2 and holy_power <= 2 and multi_target and attack_range:
            return Cast("审判", "多目标满充能")

        # 如果 玩家没有战争艺术增益，公正之剑冷却就绪且目标在攻击范围内
        # => 施放 公正之剑
        if not ctx.player_has_buff_art_of_war and blade_ready and attack_range:
            return Cast("公正之剑", "无战争艺术")

        # 如果 审判充能为 2 层，且圣能不多于 2 点
        # 如果 处于单体条件，且目标在攻击范围内
        # => 施放 审判
        if judgment_ready == 2 and holy_power <= 2 and single_target and attack_range:
            return Cast("审判", "单体满充能")

        # 如果 满足四件套触发条件，处于多目标条件且目标在攻击范围内
        # => 施放 最终审判
        if four_piece_proc and multi_target and attack_range:
            return Cast("最终审判", "四件套多目标触发")

        # 如果 圣能为 4 点，处于多目标条件且目标在攻击范围内
        # => 施放 神圣风暴
        if holy_power == 4 and multi_target and attack_range:
            return Cast("神圣风暴", "4圣能")

        # 如果 满足四件套触发条件，处于单体条件且目标在攻击范围内
        # => 施放 神圣风暴
        if four_piece_proc and single_target and attack_range:
            return Cast("神圣风暴", "四件套单体触发")

        # 如果 圣能为 4 点，处于单体条件且目标在攻击范围内
        # => 施放 最终审判
        if holy_power == 4 and single_target and attack_range:
            return Cast("最终审判", "4圣能")

        # 如果 审判充能不少于 1 层，圣能不多于 2 点且目标在攻击范围内
        # => 施放 审判
        if judgment_ready >= 1 and holy_power <= 2 and attack_range:
            return Cast("审判", "低圣能")

        # 如果 公正之剑冷却就绪，圣能不多于 3 点且目标在攻击范围内
        # => 施放 公正之剑
        if blade_ready and holy_power <= 3 and attack_range:
            return Cast("公正之剑")

        # 如果 审判充能不少于 1 层，圣能不多于 4 点且目标在攻击范围内
        # => 施放 审判
        if judgment_ready >= 1 and holy_power <= 4 and attack_range:
            return Cast("审判")

        # 如果 圣能不少于 3 点
        if holy_power >= 3:
            # 如果 处于多目标条件，且目标在攻击范围内
            # => 施放 神圣风暴
            if multi_target and attack_range:
                return Cast("神圣风暴")
            # 如果 处于单体条件，且目标在攻击范围内
            # => 施放 最终审判
            if single_target and attack_range:
                return Cast("最终审判")

        # 如果 以上规则均未满足
        # => 不执行动作
        return Idle("没有满足条件的动作")
