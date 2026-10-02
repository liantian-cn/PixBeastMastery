-- 施法/引导剩余秒数：每级0.1秒，25.5秒饱和；空闲为黑。
local _, addonTable = ...
local UNIT = "target"
local cell
local frame = CreateFrame("Frame")
local curve = C_CurveUtil.CreateColorCurve()
curve:SetType(Enum.LuaCurveType.Linear)
curve:AddPoint(0, addonTable.COLOR.BLACK)
curve:AddPoint(25.5, addonTable.COLOR.WHITE)
local function Refresh()
    if not cell then return end
    local color = addonTable.COLOR.BLACK
    if UnitExists(UNIT) then
        local duration
        if select(11, UnitCastingInfo(UNIT)) ~= nil then
            duration = UnitCastingDuration(UNIT)
        elseif select(9, UnitChannelInfo(UNIT)) ~= nil then
            duration = UnitChannelDuration(UNIT)
        end
        if issecretvalue(duration) or duration ~= nil then color = duration:EvaluateRemainingDuration(curve) end
    end
    cell:setCell(color)
end
for _, event in ipairs({ "PLAYER_ENTERING_WORLD", "PLAYER_TARGET_CHANGED", "PLAYER_FOCUS_CHANGED" }) do frame:RegisterEvent(event) end
for _, event in ipairs({ "UNIT_SPELLCAST_START", "UNIT_SPELLCAST_STOP", "UNIT_SPELLCAST_DELAYED", "UNIT_SPELLCAST_INTERRUPTED", "UNIT_SPELLCAST_CHANNEL_START", "UNIT_SPELLCAST_CHANNEL_STOP", "UNIT_SPELLCAST_CHANNEL_UPDATE" }) do frame:RegisterUnitEvent(event, UNIT) end
frame:SetScript("OnEvent", function() C_Timer.After(0, Refresh) end)
local elapsed = 0
frame:SetScript("OnUpdate", function(_, delta)
    elapsed = elapsed + delta
    if elapsed >= 0.1 then elapsed = elapsed % 0.1; Refresh() end
end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 72 })
    Refresh()
end)
