-- 输出模式：使用现有配置面板并持久化。
local addonName, addonTable = ...

local insert = table.insert
local Cell = addonTable.Cell
local COLOR = addonTable.COLOR
local Config = addonTable.Config
local ConfigRows = addonTable.ConfigRows
local UIInitFuncs = addonTable.UIInitFuncs

local X = 7
local config = Config("force_single_target")
local cell
config:set_default(false)

insert(ConfigRows, {
    type = "combo",
    name = "输出模式",
    tooltip = "自动按责难范围内的敌人数分支；单体模式仍保留四件套特殊规则。",
    bind_config = config,
    default_value = false,
    options = {
        { k = false, v = "自动" },
        { k = true, v = "强制单体" },
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
