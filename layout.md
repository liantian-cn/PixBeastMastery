# PixRetribution 像素布局

Lua 的 `cells/NNN_name.lua`、本表与 `Context` 属性必须同时更新。此版本与 PixBlood 的职业字段不兼容，插件和 Python 必须配套使用。

## 基本协议

- 正式模式 Cell 为 4×4 物理像素，基板高 12 px；位置由现有 Cell、ValueBar、IconTile 实现计算。截图和 Matrix 保持原协议。
- 布尔通常白=真、黑=假；圣能直接使用灰度字节值。百分比为灰度 / 255 × 100。
- 技能冷却沿用亮度 `0/25/115/155/255` 对应剩余秒数 `245/120/30/10/0` 的分段曲线；白=就绪，黑也可能表示技能未知或不可用，不能当成就绪。
- 审判充能使用单个 CellBackplate 承载实心字符，RGB 灰度字节直接表示 0–2 充能，Python 四舍五入返回整数；零充能或缺失数据均为黑色。光环只读取存在性，由 AuraContainer 原生筛选和显隐。
- 射程布尔代表指定技能射程，不代表精确码数。敌人数只包含射程可观察的姓名板，不能解释为完整的周围敌人数；自动模式计数为 0 时，不强行假定单体。

## 普通区

| 位置 | 字段 / 文件名后缀 | 类型 | 含义 |
| --- | --- | --- | --- |
| 1 | `enable` | Cell / 布尔 | 反应addonTable.ENABLE的状态 |
| 2 | `in_burst` | Cell / 布尔 | 反应addonTable.InBurst()的状态 |
| 3 | `delaying` | Cell / 布尔 | 白=延迟中；Python 暂停全部自动动作，包括打断、自保和物品。 |
| 4 | `player_is_alive` | Cell / 布尔 | 玩家存活 |
| 5 | `player_health_pct` | Cell / 百分比 | 玩家生命值（百分比） |
| 6 | `power_holy_power` | Cell / 整数 | 圣能；普通整数直接编码为灰度字节，Python 四舍五入读取；秘密值或非法整数明确报错。 |
| 7 | `force_single_target` | Cell / 布尔 | 白=强制单体，黑=自动；默认自动，配置持久化。强制单体仍允许四件套特殊风暴规则。 |
| 8 | `player_in_combat` | Cell / 布尔 | 玩家是否处于战斗。 |
| 9 | `player_is_player_target` | Cell / 布尔 | 玩家的目标是自己 |
| 10 | `player_is_moving` | Cell / 布尔 | 玩家正在移动 |
| 11 | `player_in_vehicle` | Cell / 布尔 | 玩家在坐骑/载具上 |
| 12 | `player_is_targeting_spell` | Cell / 布尔 | 玩家在选取施法目标的状态 |
| 13 | `player_is_chatting` | Cell / 布尔 | 玩家在聊天 |
| 14 | `ticket_13_ready` | Cell / 布尔 | 一号饰品可用（SLOT 13）；自动饰品开启、爆发窗口内且目标在 853 射程内时优先使用。 |
| 15 | `ticket_14_ready` | Cell / 布尔 | 二号饰品可用（SLOT 14）；同上，优先级低于一号饰品，每轮重新读取可用状态。 |
| 16 | `healthstone_ready` | Cell / 布尔 | 治疗石 item:5512；冷却启用且物品可使用时为白色。 |
| 17 | `heal_potion_ready` | Cell / 布尔 | 银月城生命药水 item:241304；冷却启用且物品可使用时为白色。 |
| 18 | `player_has_heal_absorb` | StatusBar / 阈值布尔 | 玩家有治疗吸收盾(250,000以上) |
| 19 | `player_has_damage_absorb` | StatusBar / 阈值布尔 | 玩家有治疗吸收盾(500,000以上) |
| 20 | `player_cast_progress` | Cell / 百分比 | 玩家的cast/channel进度 |
| 21 | `player_is_empowering` | Cell / 布尔 | 玩家是否在蓄力 |
| 22 | `target_is_exists` | Cell / 布尔 | 目标存在 |
| 23 | `target_is_alive` | Cell / 布尔 | 目标存活 |
| 24 | `target_can_attack` | Cell / 布尔 | 目标可攻击 |
| 25 | `target_can_assist` | Cell / 布尔 | 目标可协助 |
| 26 | `target_health_pct` | Cell / 百分比 | 目标生命值（百分比） |
| 27 | `target_cast_interruptible` | Cell / 布尔 | 目标可打断 |
| 28 | `target_cast_progress` | Cell / 百分比 | 目标的cast/channel进度 |
| 29 | `target_in_melee_range` | Cell / 布尔 | target 在责难 96231 技能射程内；nil 或无单位显示黑色。 |
| 30 | `target_in_ranged_range` | Cell / 布尔 | target 在最终审判 383328 技能射程内；不是精确 20 码测距。 |
| 31 | `target_in_interrupt_range` | Cell / 布尔 | target 在责难 96231 技能射程内；nil 或无单位显示黑色。 |
| 32 | `focus_is_exists` | Cell / 布尔 | 焦点存在 |
| 33 | `focus_is_alive` | Cell / 布尔 | 焦点存活 |
| 34 | `focus_can_attack` | Cell / 布尔 | 焦点可攻击 |
| 35 | `focus_can_assist` | Cell / 布尔 | 焦点可协助 |
| 36 | `focus_health_pct` | Cell / 百分比 | 焦点生命值（百分比） |
| 37 | `focus_cast_interruptible` | Cell / 布尔 | 焦点可打断 |
| 38 | `focus_cast_progress` | Cell / 百分比 | 焦点的cast/channel进度 |
| 39 | `focus_in_melee_range` | Cell / 布尔 | focus 在责难 96231 技能射程内；nil 或无单位显示黑色。 |
| 40 | `focus_in_ranged_range` | Cell / 布尔 | focus 在最终审判 383328 技能射程内；不是精确 20 码测距。 |
| 41 | `focus_in_interrupt_range` | Cell / 布尔 | focus 在责难 96231 技能射程内；nil 或无单位显示黑色。 |
| 42 | `spell_cd_global_cooldown` | Cell / 冷却曲线 | [Global Cooldown]。SPELLID:61304 的冷却时间,ignore_gcd = false |
| 43 | `spell_cd_rebuke` | Cell / 冷却曲线 | 责难 96231 冷却。 |
| 44 | `spell_cd_avenging_wrath` | Cell / 冷却曲线 | 复仇之怒 31884 冷却。 |
| 45 | `spell_cd_execution_sentence` | Cell / 冷却曲线 | 处决宣判 343527 冷却。 |
| 46 | `spell_cd_wake_of_ashes` | Cell / 冷却曲线 | 灰烬觉醒 255937 冷却。 |
| 47 | `spell_cd_blade_of_justice` | Cell / 冷却曲线 | 公正之剑 184575 冷却。 |
| 48 | `spell_charges_judgment` | Cell / 0–2 | 审判 20271；RGB 灰度字节直接表示充能数，Python 四舍五入返回整数；零充能或缺失数据均为黑色。 |
| 49 | `mouseover_in_melee_range` | Cell / 布尔 | 鼠标指向在责难 96231 技能射程内；保留监控，不用于手动插入。 |
| 50 | `burst_potion_enabled` | Cell / 布尔 | 独立爆发药水开关；默认关闭，配置持久化，不随爆发窗口联动。 |
| 51 | `spell_cd_divine_toll` | Cell / 冷却曲线 | 圣洁鸣钟 375576 冷却。 |
| 52 | `spell_cd_lay_on_hands` | Cell / 冷却曲线 | 圣疗术 633 冷却。 |
| 53 | `spell_cd_divine_shield` | Cell / 冷却曲线 | 圣盾术 642 冷却。 |
| 54 | `item_cd_lights_potential` | Cell / 布尔 | 圣光潜力 item:241308 有非银行库存且冷却结束；沿用原监控。宏保留 241308、241309。 |
| 55 | `player_has_buff_avenging_wrath` | Cell / 布尔 | 玩家复仇之怒 31884 是否存在。 |
| 56 | `player_has_buff_divine_purpose` | Cell / 布尔 | 玩家神圣意志 408458 是否存在；按源 JSON 的 ID，不替换成 223819。 |
| 57 | `player_has_buff_dawnlight` | Cell / 布尔 | 玩家晨光 431522 是否存在；无需层数或剩余时间。 |
| 58 | `player_has_buff_art_of_war` | Cell / 布尔 | 玩家战争艺术 406086 是否存在。 |
| 59 | `player_has_buff_divine_arbiter_storm` | Cell / 布尔 | 玩家神圣仲裁风暴 1306162 是否存在。 |
| 60 | `four_piece_enabled` | Cell / 布尔 | 白=启用四件套规则，黑=关闭；默认开启，配置持久化。 |
| 61 | `target_in_blade_of_justice_range` | Cell / 布尔 | 目标在公正之剑 184575 技能射程内；不是精确 12 码测距。 |
| 62 | `target_in_judgment_range` | Cell / 布尔 | 目标在审判 20271 技能射程内。 |
| 63 | `target_in_hammer_of_justice_range` | Cell / 布尔 | 目标在制裁之锤 853 技能射程内；七个输出技能及自动饰品统一使用，nil 或无目标为黑色。 |
| 64 | `player_has_dispellable_poison_or_disease` | Cell / 布尔 | 玩家自身存在可驱散的中毒或疾病；AuraContainer 使用 HARMFUL\|RAID_PLAYER_DISPELLABLE 及 Poison、Disease 类型筛选，不检查其他单位。 |
| 65 | `spell_cd_cleanse_toxins` | Cell / 冷却曲线 | 清毒术 213644 冷却，忽略 GCD；技能未知或不可用为黑色，不视为就绪。 |
| 66 | `auto_cleanse_enabled` | Cell / 布尔 | 自动清毒开关，默认开启，游戏内配置持久化。 |
| 67 | `auto_trinket_enabled` | Cell / 布尔 | 自动饰品开关，默认开启，游戏内配置持久化。 |
| 68 | `player_melee_enemies_count` | Cell / 0–40 | 制裁之锤 853 范围内可观察、存活、可攻击的姓名板敌人数；保留历史字段名，不要求入战；上限 40，灰度=count/40，每 0.2 秒刷新。秘密或 nil 射程不计入。 |

普通区连续占用 1–68 格；审判充能仅占第 48 格。其余旧 DK 专属字段、光环层数条和沸点计时已移除。

第 29、30、39、40、49、61、62 格保留原射程监控，不用于输出循环的距离判断。责难仍使用第 31、41 格自身射程。审判、公正之剑、灰烬觉醒、最终审判、神圣风暴、圣洁鸣钟、处决宣判均使用第 63 格；AOE 使用第 68 格，至少 2 个进入多目标，保留强制单体规则。

自动动作沿用现有入口限制：插件启用、玩家存活且在战斗、有可攻击目标，并且不处于手动延迟、载具、聊天、地面选点或施法状态。优先级为原打断与自保、治疗石、治疗药水、清毒、原爆发药水、上饰品、下饰品、复仇之怒、其余输出。清毒同时要求第 64 格为真和清毒冷却就绪；饰品要求 `in_burst`、第 63 格及对应槽位可用，每轮最多使用一个。

新增宏与 Python 键位对应：`RSHIFT-NUMPAD7` → `/cast [@player]清毒术`；`RSHIFT-NUMPAD8` → `/use 13`；`RSHIFT-NUMPAD9` → `/use 14`。

## IconTile 区（保持原位置）

| 位置 | 字段 | 含义 |
| --- | --- | --- |
| I01 | `player_cast_icon` | 玩家施法／引导图标。 |
| I02 | `assisted_combat_icon` | 游戏辅助战斗推荐图标；不替代本项目手写循环。 |
| I03 | `target_cast_icon` | 目标施法／引导图标。 |
| I04 | `focus_cast_icon` | 焦点施法／引导图标。 |
| I05–I19 | `interrupt_blacklist` | 按法术 ID 升序取前 15 个黑名单图标；加载失败的槽位留空。 |

`Context.target_cast_interruptible` 和 `focus_cast_interruptible` 同时要求可打断 cell 为真、施法图标非空、图标不在黑名单。Rotation 再检查对应单位有效性、责难冷却和责难射程。两个单位均满足时优先焦点。

## 游戏内验收

本表描述编码约定，不表示已通过游戏实测。安装配套插件后核对：圣能 0–5、审判 0/1/2 充能、五个 buff 的出现与消失、四件套与输出模式开关、目标／焦点责难射程、853 射程及范围敌人数、爆发和延迟状态，以及图标黑名单。保持 `debug = false`，先用 `uv run python -m pix.test_captura` 检查定位。

新增行为验收：验证七个输出技能超出 853 射程时不触发；AOE 计数 0/1/2 及强制单体；自身中毒、疾病、不可驱散减益、仅队友中毒、清毒冷却和开关关闭；爆发窗口、目标超距、单个或两个饰品就绪、共用冷却和开关关闭。确认两个开关重新加载后保持设置，以及清毒、饰品遵守上述优先级。
