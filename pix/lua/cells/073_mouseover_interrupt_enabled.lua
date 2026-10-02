-- 鼠标指向打断开关：默认开启，配置持久化保存。
local _, addonTable = ...
local config = addonTable.Config("mouseover_interrupt_enabled")
config:set_default(true)
local cell

local function Refresh()
    if not cell then return end
    cell:setCell(config:get_value() == true and addonTable.COLOR.WHITE or addonTable.COLOR.BLACK)
end

table.insert(addonTable.ConfigRows, {
    type = "combo", name = "鼠标指向打断",
    tooltip = "允许打断鼠标指向的敌人；优先级低于焦点、高于目标，共用打断进度阈值与黑名单。",
    bind_config = config, default_value = true,
    options = { { k = false, v = "否" }, { k = true, v = "是" } },
})
config:register_callback(Refresh)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 73 })
    Refresh()
end)
