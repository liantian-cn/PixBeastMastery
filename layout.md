# PixBeastMastery 像素布局

Lua Cell、Context和本表必须同步更新。插件与Python必须配套使用。

## 编码

正式模式每格4×4物理像素，基板12px高。普通区占1–76列，加左右检测列总宽312px。IconTile仍为8×8，位于基板下方两行。Capture和Matrix协议不变。

- 布尔：白255为真、黑0为假。
- 灰度整数：直接读取字节并四舍五入，不除255。
- 百分比：灰度/255×100；集中值点数=四舍五入(第6格比例×第61格上限)。上限不在100–120时按0点处理。
- 冷却：亮度0/25/115/155/255对应245/120/30/10/0秒；黑色也包含未知技能和缺失数据，不表示就绪。
- 充能：currentCharges和maxCharges经原生文字显示秘密计数，Python读取灰度。最大充能>0且当前充能≥上限时，下一层恢复时间视为0；否则读取62格。没有恢复对象时62格为黑。
- 攻击模式先按人数≥2计算IsAOE，再由10/20强制覆盖；自动模式0人也按单体。
- 所有攻击射程字段均参考反制射击147362，包括保留名称中的melee/ranged；坦克误导范围单独使用34477。
- 施法剩余时间按0.1秒量化；空闲为0，须同时检查可打断状态及施法图标，不能只靠秒数判断。

## 普通区

| 位置 | 字段 / 文件名后缀 | 类型 | 含义 |
| --- | --- | --- | --- |
| 1 | `enable` | Cell / 布尔 | 反应addonTable.ENABLE的状态 |
| 2 | `in_burst` | Cell / 布尔 | 反应addonTable.InBurst()的状态 |
| 3 | `delaying` | Cell / 布尔 | 白=延迟中；Python 暂停全部自动动作，包括打断、自保和物品。 |
| 4 | `player_is_alive` | Cell / 布尔 | 玩家存活 |
| 5 | `player_health_pct` | Cell / 百分比 | 玩家生命值（百分比） |
| 6 | `power_focus_pct` | 百分比 | UnitPowerPercent，灰度/255×100；与61格组合还原点数 |
| 7 | `attack_mode` | 枚举 | 灰度0自动、10单体、20AOE；脱战及重载恢复0 |
| 8 | `player_in_combat` | Cell / 布尔 | 玩家是否处于战斗。 |
| 9 | `player_is_player_target` | Cell / 布尔 | 玩家的目标是自己 |
| 10 | `player_is_moving` | Cell / 布尔 | 玩家正在移动 |
| 11 | `player_in_vehicle` | Cell / 布尔 | 玩家在坐骑/载具上 |
| 12 | `player_is_targeting_spell` | Cell / 布尔 | 玩家在选取施法目标的状态 |
| 13 | `player_is_chatting` | Cell / 布尔 | 玩家在聊天 |
| 14 | `ticket_13_ready` | Cell / 布尔 | 一号饰品可用（SLOT 13）；自动饰品开启、爆发窗口内且目标在 147362 射程内时优先使用。 |
| 15 | `ticket_14_ready` | Cell / 布尔 | 二号饰品可用（SLOT 14）；同上，优先级低于一号饰品，每轮重新读取可用状态。 |
| 16 | `healthstone_ready` | Cell / 布尔 | 治疗石 item:5512；冷却启用且物品可使用时为白色。 |
| 17 | `heal_potion_ready` | Cell / 布尔 | 银月城生命药水 item:241304；冷却启用且物品可使用时为白色。 |
| 18 | `player_has_heal_absorb` | StatusBar / 阈值布尔 | 玩家有治疗吸收盾(250,000以上) |
| 19 | `player_has_damage_absorb` | StatusBar / 阈值布尔 | 玩家有伤害吸收盾(500,000以上) |
| 20 | `player_cast_progress` | Cell / 百分比 | 玩家的cast/channel进度 |
| 21 | `player_is_empowering` | Cell / 布尔 | 玩家是否在蓄力 |
| 22 | `target_is_exists` | Cell / 布尔 | 目标存在 |
| 23 | `target_is_alive` | Cell / 布尔 | 目标存活 |
| 24 | `target_can_attack` | Cell / 布尔 | 目标可攻击 |
| 25 | `target_can_assist` | Cell / 布尔 | 目标可协助 |
| 26 | `target_health_pct` | Cell / 百分比 | 目标生命值（百分比） |
| 27 | `target_cast_interruptible` | Cell / 布尔 | 目标可打断 |
| 28 | `target_cast_progress` | Cell / 百分比 | 目标的cast/channel进度 |
| 29 | `target_in_melee_range` | 布尔 | 单位在反制射击147362射程内；nil或无单位显示黑色。 |
| 30 | `target_in_ranged_range` | 布尔 | 单位在反制射击147362射程内；nil或无单位显示黑色。 |
| 31 | `target_in_interrupt_range` | 布尔 | 单位在反制射击147362射程内；nil或无单位显示黑色。 |
| 32 | `focus_is_exists` | Cell / 布尔 | 焦点存在 |
| 33 | `focus_is_alive` | Cell / 布尔 | 焦点存活 |
| 34 | `focus_can_attack` | Cell / 布尔 | 焦点可攻击 |
| 35 | `focus_can_assist` | Cell / 布尔 | 焦点可协助 |
| 36 | `focus_health_pct` | Cell / 百分比 | 焦点生命值（百分比） |
| 37 | `focus_cast_interruptible` | Cell / 布尔 | 焦点可打断 |
| 38 | `focus_cast_progress` | Cell / 百分比 | 焦点的cast/channel进度 |
| 39 | `focus_in_melee_range` | 布尔 | 单位在反制射击147362射程内；nil或无单位显示黑色。 |
| 40 | `focus_in_ranged_range` | 布尔 | 单位在反制射击147362射程内；nil或无单位显示黑色。 |
| 41 | `focus_in_interrupt_range` | 布尔 | 单位在反制射击147362射程内；nil或无单位显示黑色。 |
| 42 | `spell_cd_global_cooldown` | Cell / 冷却曲线 | [Global Cooldown]。SPELLID:61304 的冷却时间,ignore_gcd = false |
| 43 | `spell_cd_counter_shot` | 冷却 | 反制射击147362 |
| 44 | `spell_cd_bestial_wrath` | 冷却 | 狂野怒火19574 |
| 45 | `spell_cd_wild_thrash` | 冷却 | 狂野鞭笞1264359 |
| 46 | `spell_cd_kill_command` | 冷却 | 杀戮命令34026；同时参考74格充能 |
| 47 | `spell_cd_barbed_shot` | 冷却 | 倒刺射击217200；同时参考48格充能 |
| 48 | `spell_charges_barbed_shot` | 整数 | 倒刺射击当前充能；灰度字节即数量 |
| 49 | `mouseover_in_melee_range` | 布尔 | 鼠标单位在147362射程 |
| 50 | `burst_potion_enabled` | 布尔 | 自动鲁莽药水开关，默认开启 |
| 51 | `spell_cd_mend_pet` | 冷却 | 治疗宠物136 |
| 52 | `spell_cd_exhilaration` | 冷却 | 意气风发109304 |
| 53 | `spell_cd_misdirection` | 冷却 | 误导34477 |
| 54 | `reckless_potion_ready` | 布尔 | 241288或241289有库存且冷却好 |
| 55 | `player_has_buff_pack_wyvern` | 布尔 | 玩家增益471878 |
| 56 | `player_has_buff_natures_ally` | 布尔 | 玩家自然之友（Nature’s Ally）增益1276720 |
| 57 | `player_has_buff_pack_boar` | 布尔 | 玩家增益472324 |
| 58 | `player_has_buff_pack_bear` | 布尔 | 玩家增益472325 |
| 59 | `player_has_buff_cobra_fangs` | 布尔 | 眼镜蛇利牙1299389 |
| 60 | `finishing` | 布尔 | 收尾开关：0关闭、255开启；脱战及重载关闭 |
| 61 | `power_focus_max` | 整数 | 配置集中值上限100–120，默认100，灰度直接表示点数 |
| 62 | `spell_recharge_barbed_shot` | 冷却曲线 | 倒刺射击下一层充能剩余时间；满充能由48和75格识别 |
| 63 | `pet_is_exists` | 布尔 | 宠物存在 |
| 64 | `pet_is_alive` | 布尔 | 宠物存在且存活 |
| 65 | `pet_health_pct` | 百分比 | 宠物预测生命比例 |
| 66 | `party_tank_index` | 整数 | 0无合格坦克，1–4表示party编号；只选存活在线坦克 |
| 67 | `auto_trinket_enabled` | 布尔 | 自动饰品开关，默认开启 |
| 68 | `player_enemies_count` | 比例计数 | 灰度/255×40并四舍五入；147362范围内可攻击、存活、战斗中的可观察姓名板数量 |
| 69 | `player_in_party` | 布尔 | 在小队且不在团队 |
| 70 | `spell_known_misdirection` | 布尔 | 误导34477已学会 |
| 71 | `party_tank_in_misdirection_range` | 布尔 | 66格选中的坦克在34477射程内 |
| 72 | `target_cast_remaining` | 秒数 | 目标施法/引导剩余时间，灰度/10，25.5秒饱和 |
| 73 | `focus_cast_remaining` | 秒数 | 焦点施法/引导剩余时间，灰度/10，25.5秒饱和 |
| 74 | `spell_charges_kill_command` | 整数 | 杀戮命令当前充能 |
| 75 | `spell_max_charges_barbed_shot` | 整数 | 倒刺射击最大充能；0表示缺失 |
| 76 | `player_has_buff_beast_cleave` | 布尔 | 玩家野兽顺劈（Beast Cleave）增益268877是否存在 |

## IconTile

| 槽位 | 内容 |
| --- | --- |
| I01 | 玩家施法/引导图标 |
| I02 | 游戏辅助战斗推荐技能图标 |
| I03 | 目标施法/引导图标 |
| I04 | 焦点施法/引导图标 |
| I05–I19 | 打断黑名单，法术ID升序取前15项；加载失败留空 |

黑名单默认ID保留1241214、1228176、371984、384194、1294815。匹配沿用Matrix的内区裁剪和指纹算法；黑底表示无图标。可打断判断必须有当前施法图标，并且不在黑名单中。

## 刷新与控制

冷却、充能恢复、射程和施法剩余时间保留0.1秒刷新；充能数量由事件更新并每秒兜底；资源/生命由对应事件刷新，光环由AuraContainer原生绑定。

敌人数按姓名板及进出战斗事件刷新，每秒兜底。坦克编号在进入地图、队伍/职责、连接、生命状态及进出战斗时更新，每2秒兜底；误导射程每0.1秒刷新。

攻击模式与收尾按钮的设置、命令、显示分别完全位于007和060文件中。状态脱战/重载恢复默认，位置单独持久化；上限与消耗品开关保存在PixBeastMasteryDB中。

秘密充能、冷却、施法时间和实际灰度渲染仍须在游戏内验证；语法和Python验证不能代替客户端验收。
