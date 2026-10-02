local addonName, addonTable = ...
local insert = table.insert
local CreateFrame = CreateFrame
local SetOverrideBindingClick = SetOverrideBindingClick
local logging = addonTable.logging

-- 复用 base.lua 的检查结果，不为待重载插件绑定技能宏。
if addonTable.RELOAD_REQUIRED then return end

local macroList = {}
insert(macroList, { title = "reloadUI", key = "CTRL-F12", text = "/reload" })
insert(macroList, { title = "倒刺射击", key = "RCTRL-NUMPAD1", text = "/cast [@target,harm,nodead] 倒刺射击" })
insert(macroList, { title = "焦点反制射击", key = "RCTRL-NUMPAD2", text = "/cast [@focus,harm,nodead] 反制射击" })
insert(macroList, { title = "目标反制射击", key = "RCTRL-NUMPAD3", text = "/cast [@target,harm,nodead] 反制射击" })
insert(macroList, { title = "狂野怒火", key = "RCTRL-NUMPAD4", text = "/cast 狂野怒火" })
insert(macroList, { title = "狂野鞭笞", key = "RCTRL-NUMPAD5", text = "/cast [@target,harm,nodead] 狂野鞭笞" })
insert(macroList, { title = "杀戮命令", key = "RCTRL-NUMPAD6", text = "/cast [@target,harm,nodead] 杀戮命令" })
insert(macroList, { title = "眼镜蛇射击", key = "RCTRL-NUMPAD7", text = "/cast [@target,harm,nodead] 眼镜蛇射击" })
insert(macroList, { title = "鲁莽药水", key = "RCTRL-NUMPAD8", text = "/use item:241288\n/use item:241289" })
insert(macroList, { title = "治疗宠物", key = "RCTRL-NUMPAD9", text = "/cast 治疗宠物" })
insert(macroList, { title = "召唤/复活宠物", key = "RCTRL-NUMPAD0", text = "/cast [@pet,dead] 复活宠物\n/castsequence [nopet] reset=3 召唤宠物 1,复活宠物" })
insert(macroList, { title = "误导party1", key = "RSHIFT-NUMPAD1", text = "/cast [@party1,help,nodead] 误导" })
insert(macroList, { title = "误导party2", key = "RSHIFT-NUMPAD2", text = "/cast [@party2,help,nodead] 误导" })
insert(macroList, { title = "误导party3", key = "RSHIFT-NUMPAD3", text = "/cast [@party3,help,nodead] 误导" })
insert(macroList, { title = "误导party4", key = "RSHIFT-NUMPAD4", text = "/cast [@party4,help,nodead] 误导" })
insert(macroList, { title = "治疗石", key = "RSHIFT-NUMPAD5", text = "/use item:5512" })
insert(macroList, { title = "银月城生命药水", key = "RSHIFT-NUMPAD6", text = "/use item:241304" })
insert(macroList, { title = "意气风发", key = "RSHIFT-NUMPAD7", text = "/cast 意气风发" })
insert(macroList, { title = "上饰品", key = "RSHIFT-NUMPAD8", text = "/use 13" })
insert(macroList, { title = "下饰品", key = "RSHIFT-NUMPAD9", text = "/use 14" })

for _, macro in ipairs(macroList) do
    local buttonName = addonName .. "Button" .. macro.title
    local frame = CreateFrame("Button", buttonName, UIParent, "SecureActionButtonTemplate")
    frame:SetAttribute("type", "macro")
    frame:SetAttribute("macrotext", macro.text)
    frame:RegisterForClicks("AnyDown", "AnyUp")
    SetOverrideBindingClick(frame, true, macro.key, buttonName)
    logging("bind " .. macro.key .. " > " .. macro.text)
end
