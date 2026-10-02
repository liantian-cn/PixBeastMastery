local _, addonTable = ...
local cell
local frame = CreateFrame("Frame")
local function Refresh()
    if cell then cell:setCell(C_CurveUtil.EvaluateColorFromBoolean(IsInGroup() and not IsInRaid(), addonTable.COLOR.WHITE, addonTable.COLOR.BLACK)) end
end
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("GROUP_ROSTER_UPDATE")
frame:SetScript("OnEvent", function() C_Timer.After(0, Refresh) end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 69 })
    Refresh()
end)
