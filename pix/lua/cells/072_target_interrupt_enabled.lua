-- 目标打断开关：默认关闭，配置持久化保存。
local _, addonTable = ...
local config = addonTable.Config("target_interrupt_enabled")
config:set_default(false)
local cell

local function Refresh()
    if not cell then return end
    cell:setCell(config:get_value() == true and addonTable.COLOR.WHITE or addonTable.COLOR.BLACK)
end

table.insert(addonTable.ConfigRows, {
    type = "combo", name = "目标打断",
    tooltip = "允许打断当前目标；优先级低于焦点和鼠标指向，共用打断进度阈值与黑名单。",
    bind_config = config, default_value = false,
    options = { { k = false, v = "否" }, { k = true, v = "是" } },
})
config:register_callback(Refresh)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 72 })
    Refresh()
end)
