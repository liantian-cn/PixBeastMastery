-- 两种普通鲁莽药水：有库存且冷却结束。
local _, addonTable = ...
local cell
local frame = CreateFrame("Frame")
local function Refresh()
    if not cell then return end
    local ready = false
    for _, id in ipairs({ 241288, 241289 }) do
        local start, duration, enabled = C_Item.GetItemCooldown(id)
        if C_Item.GetItemCount(id, false, false, false, false) > 0
            and start ~= nil and duration ~= nil and enabled and enabled ~= 0
            and (duration == 0 or start + duration <= GetTime()) then
            ready = true
        end
    end
    cell:setCell(ready and addonTable.COLOR.WHITE or addonTable.COLOR.BLACK)
end
for _, event in ipairs({ "PLAYER_ENTERING_WORLD", "BAG_UPDATE", "BAG_UPDATE_COOLDOWN", "SPELL_UPDATE_COOLDOWN" }) do frame:RegisterEvent(event) end
frame:SetScript("OnEvent", function() C_Timer.After(0, Refresh) end)
local elapsed = 0
frame:SetScript("OnUpdate", function(_, delta)
    elapsed = elapsed + delta
    if elapsed >= 1 then elapsed = elapsed % 1; Refresh() end
end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 54 })
    Refresh()
end)
