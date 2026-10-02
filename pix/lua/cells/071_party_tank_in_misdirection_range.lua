-- 对已选坦克使用误导自身射程，秘密布尔只交给颜色消费者。
local _, addonTable = ...
local cell
local frame = CreateFrame("Frame")
local function Refresh()
    if not cell then return end
    local color = addonTable.COLOR.BLACK
    local unit = addonTable.PartyTankUnit
    if unit and UnitExists(unit) and UnitIsConnected(unit) and not UnitIsDeadOrGhost(unit) then
        local inRange = C_Spell.IsSpellInRange(34477, unit)
        if not issecretvalue(inRange) and inRange == nil then inRange = false end
        color = C_CurveUtil.EvaluateColorFromBoolean(inRange, addonTable.COLOR.WHITE, addonTable.COLOR.BLACK)
    end
    cell:setCell(color)
end
addonTable.RefreshMisdirectionRange = Refresh
local elapsed = 0
frame:SetScript("OnUpdate", function(_, delta)
    elapsed = elapsed + delta
    if elapsed >= 0.1 then elapsed = elapsed % 0.1; Refresh() end
end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 71 })
    Refresh()
end)
