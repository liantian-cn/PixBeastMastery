-- 配置上限为普通整数；灰度字节直接表示100至120点。
local _, addonTable = ...
local config = addonTable.Config("power_focus_max")
config:set_default(100)
local cell
local function Refresh()
    if not cell then return end
    local value = math.floor(math.max(100, math.min(120, tonumber(config:get_value()) or 100)) + 0.5)
    local gray = value / 255
    cell:setCellRGBA(gray, gray, gray)
end
table.insert(addonTable.ConfigRows, {
    type = "slider", name = "集中值上限", tooltip = "请设置为角色实际集中值上限，用于像素比例还原点数。",
    bind_config = config, default_value = 100, min_value = 100, max_value = 120, step = 1,
})
config:register_callback(Refresh)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 61 })
    Refresh()
end)
