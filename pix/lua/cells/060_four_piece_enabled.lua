-- 四件套：使用现有配置面板并持久化。
local addonName, addonTable = ...

local insert = table.insert
local Cell = addonTable.Cell
local COLOR = addonTable.COLOR
local Config = addonTable.Config
local ConfigRows = addonTable.ConfigRows
local UIInitFuncs = addonTable.UIInitFuncs

local X = 60
local config = Config("four_piece_enabled")
local cell
config:set_default(true)

insert(ConfigRows, {
    type = "combo",
    name = "四件套",
    tooltip = "启用烈日惩戒骑 JSON 的四件套特殊消耗规则；无四件套时关闭。",
    bind_config = config,
    default_value = true,
    options = {
        { k = false, v = "关闭" },
        { k = true, v = "开启" },
    },
})

local function Refresh()
    if not cell then return end
    cell:setCell(config:get_value() == true and COLOR.WHITE or COLOR.BLACK)
end

local function Initialize()
    cell = Cell:New({ x = X })
    Refresh()
end

config:register_callback(Refresh)
insert(UIInitFuncs, Initialize)
