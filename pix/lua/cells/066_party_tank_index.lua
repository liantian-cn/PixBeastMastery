-- 0表示无合格坦克，1至4直接表示party编号。
local _, addonTable = ...
local cell
local frame = CreateFrame("Frame")
addonTable.PartyTankUnit = nil
local function Refresh()
    local selected = 0
    if IsInGroup() and not IsInRaid() then
        for index = 1, 4 do
            local unit = "party" .. index
            if UnitExists(unit) and UnitIsConnected(unit) and not UnitIsDeadOrGhost(unit) then
                local role = UnitGroupRolesAssigned(unit)
                if not issecretvalue(role) and role == "TANK" then selected = index; break end
            end
        end
    end
    addonTable.PartyTankUnit = selected > 0 and ("party" .. selected) or nil
    if addonTable.RefreshMisdirectionRange then addonTable.RefreshMisdirectionRange() end
    if cell then
        local gray = selected / 255
        cell:setCellRGBA(gray, gray, gray)
    end
end
for _, event in ipairs({ "PLAYER_ENTERING_WORLD", "GROUP_ROSTER_UPDATE", "PLAYER_ROLES_ASSIGNED", "ROLE_CHANGED_INFORM", "UNIT_CONNECTION", "UNIT_HEALTH", "UNIT_FLAGS", "PARTY_MEMBER_ENABLE", "PARTY_MEMBER_DISABLE", "PLAYER_REGEN_ENABLED", "PLAYER_REGEN_DISABLED" }) do frame:RegisterEvent(event) end
local pending = false
frame:SetScript("OnEvent", function()
    if pending then return end
    pending = true
    C_Timer.After(0, function() pending = false; Refresh() end)
end)
local elapsed = 0
frame:SetScript("OnUpdate", function(_, delta)
    elapsed = elapsed + delta
    if elapsed >= 2 then elapsed = elapsed % 2; Refresh() end
end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 66 })
    Refresh()
end)
