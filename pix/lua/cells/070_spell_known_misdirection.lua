local _, addonTable = ...
local cell
local frame = CreateFrame("Frame")
local function Refresh()
    if cell then cell:setCell(C_CurveUtil.EvaluateColorFromBoolean(C_SpellBook.IsSpellInSpellBook(34477) or C_SpellBook.IsSpellKnown(34477), addonTable.COLOR.WHITE, addonTable.COLOR.BLACK)) end
end
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("SPELLS_CHANGED")
frame:SetScript("OnEvent", function() C_Timer.After(0, Refresh) end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 70 })
    Refresh()
end)
