-- 集中值比例；绝对点数由 Python 结合配置上限还原。
local _, addonTable = ...
local cell
local frame = CreateFrame("Frame")
local function Refresh()
    if cell then
        cell:setCell(UnitPowerPercent("player", Enum.PowerType.Focus, false, addonTable.CURVE.percent))
    end
end
for _, event in ipairs({ "PLAYER_ENTERING_WORLD", "UNIT_POWER_UPDATE", "UNIT_MAXPOWER", "UNIT_DISPLAYPOWER" }) do
    frame:RegisterEvent(event)
end
frame:SetScript("OnEvent", function() C_Timer.After(0, Refresh) end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 6 })
    Refresh()
end)
