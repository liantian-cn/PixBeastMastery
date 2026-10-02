local addonName, addonTable = ...
local insert = table.insert
local CreateFrame = CreateFrame
local SetOverrideBindingClick = SetOverrideBindingClick
local logging = addonTable.logging

-- 复用 base.lua 的检查结果，不为待重载插件绑定技能宏。
if addonTable.RELOAD_REQUIRED then return end

local macroList = {}
insert(macroList, { title = "reloadUI", key = "CTRL-F12", text = "/reload" })
insert(macroList, { title = "最终审判", key = "RCTRL-NUMPAD1", text = "/cast [@target,harm,nodead] 最终审判" })
insert(macroList, { title = "焦点责难", key = "RCTRL-NUMPAD2", text = "/cast [@focus,harm,nodead] 责难" })
insert(macroList, { title = "目标责难", key = "RCTRL-NUMPAD3", text = "/cast [@target,harm,nodead] 责难" })
insert(macroList, { title = "复仇之怒", key = "RCTRL-NUMPAD4", text = "/cast 复仇之怒" })
insert(macroList, { title = "处决宣判", key = "RCTRL-NUMPAD5", text = "/cast [@target,harm,nodead] 处决宣判" })
insert(macroList, { title = "灰烬觉醒", key = "RCTRL-NUMPAD6", text = "/cast 灰烬觉醒" })
insert(macroList, { title = "公正之剑", key = "RCTRL-NUMPAD7", text = "/cast [@target,harm,nodead] 公正之剑" })
insert(macroList, { title = "圣光潜力", key = "RCTRL-NUMPAD8", text = "/use item:241308\n/use item:241309" })
insert(macroList, { title = "审判", key = "RCTRL-NUMPAD9", text = "/cast [@target,harm,nodead] 审判" })
insert(macroList, { title = "神圣风暴", key = "RCTRL-NUMPAD0", text = "/cast 神圣风暴" })
insert(macroList, { title = "圣洁鸣钟", key = "RSHIFT-NUMPAD1", text = "/cast [@target,harm,nodead] 圣洁鸣钟" })
insert(macroList, { title = "圣疗术", key = "RSHIFT-NUMPAD2", text = "/cast [@player] 圣疗术" })
insert(macroList, { title = "圣盾术", key = "RSHIFT-NUMPAD3", text = "/cast 圣盾术" })
insert(macroList, { title = "荣耀圣令", key = "RSHIFT-NUMPAD4", text = "/cast [@player] 荣耀圣令" })
insert(macroList, { title = "治疗石", key = "RSHIFT-NUMPAD5", text = "/use item:5512" })
insert(macroList, { title = "银月城生命药水", key = "RSHIFT-NUMPAD6", text = "/use item:241304" })
insert(macroList, { title = "清毒术", key = "RSHIFT-NUMPAD7", text = "/cast [@player]清毒术" })
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
