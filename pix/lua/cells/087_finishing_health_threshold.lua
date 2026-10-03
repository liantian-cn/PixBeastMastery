-- 灰度字节直接表示收尾血量阈值；设置持久化，脱战和重载不重置。
local _, addonTable = ...
local config = addonTable.Config("finishing_health_threshold")
config:set_default(20)
local cell

local function Refresh()
    if not cell then return end
    local value = math.floor(math.max(0, math.min(50, tonumber(config:get_value()) or 20)) + 0.5)
    local gray = value / 255
    cell:setCellRGBA(gray, gray, gray)
end

table.insert(addonTable.ConfigRows, {
    type = "slider", name = "收尾血量阈值（%）",
    tooltip = "仅影响自动收尾：非遭遇战且目标血量严格低于此百分比时不使用狂野怒火。0表示自动模式不收尾。脱战及重载保留设置。",
    bind_config = config, default_value = 20, min_value = 0, max_value = 50, step = 5,
})
config:register_callback(Refresh)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 87 })
    Refresh()
end)
