-- 配置、命令、像素及独立状态按钮均由本文件管理。
local addonName, addonTable = ...
local config = addonTable.Config("finishing")
local position = addonTable.Config("finishing_position")
config:set_default(0)
config:set_value(0) -- 每次加载恢复自动，按钮位置单独保存。
local states = {
    { value = 0, label = "收尾：自动", icon = 19574, color = { 0.15, 0.65, 0.35 } },
    { value = 10, label = "收尾：关闭", icon = 19574, color = { 0.35, 0.38, 0.4 } },
    { value = 20, label = "收尾：开启", icon = 19574, color = { 0.85, 0.2, 0.2 } }
}
local options = {}
for _, state in ipairs(states) do options[#options + 1] = { k = state.value, v = state.label } end
table.insert(addonTable.ConfigRows, {
    type = "combo", name = "收尾状态", tooltip = "自动：非遭遇战且目标血量低于阈值时不使用狂野怒火。左击按自动、关闭、开启循环；Shift+左键拖动。脱战及重载恢复自动。",
    bind_config = config, default_value = 0, options = options,
})
local cell, button, icon, label, background
local function CurrentState()
    local value = config:get_value()
    for index, state in ipairs(states) do if state.value == value then return state, index end end
    return states[1], 1
end
local function CycleState()
    local _, index = CurrentState()
    config:set_value(states[index % #states + 1].value)
end
local function Refresh()
    local state = CurrentState()
    local value = state.value
    if cell then
        local gray = value / 255
        cell:setCellRGBA(gray, gray, gray)
    end
    if button then
        icon:SetTexture(C_Spell.GetSpellTexture(state.icon))
        label:SetText(state.label)
        background:SetColorTexture(state.color[1] * 0.3, state.color[2] * 0.3, state.color[3] * 0.3, 1)
        label:SetTextColor(state.color[1], state.color[2], state.color[3], 1)
    end
end
config:register_callback(Refresh)
addonTable.CommandHandler["end"] = function(_, arguments)
    if arguments == "auto" then config:set_value(0)
    elseif arguments == "off" then config:set_value(10)
    elseif arguments == "on" then config:set_value(20)
    elseif arguments == "toggle" then CycleState()
    else addonTable.PrintCommandHelp() end
end
local previousHelp = addonTable.PrintCommandHelp
addonTable.PrintCommandHelp = function()
    previousHelp()
    print("/pix end auto|off|on|toggle — 收尾状态，toggle按自动、关闭、开启循环")
end

local events = CreateFrame("Frame")
events:RegisterEvent("PLAYER_REGEN_ENABLED")
events:SetScript("OnEvent", function() config:set_value(0) end)
table.insert(addonTable.UIInitFuncs, function()
    cell = addonTable.Cell:New({ x = 60 })
    button = CreateFrame("Button", addonName .. "FinishingFrame", UIParent)
    addonTable.FinishingFrame = button
    -- 控制按钮使用原生 UI 单位，不参与像素采样区的分辨率换算。
    button:SetSize(100, 24)
    button:SetFrameStrata("DIALOG")
    button:SetClampedToScreen(true)
    button:SetMovable(true)
    button:RegisterForClicks("LeftButtonUp")
    button:RegisterForDrag("LeftButton")
    local function PlaceSaved()
        local saved = position:get_value()
        if type(saved) == "table" and type(saved.x) == "number" and type(saved.y) == "number" then
            button:SetPoint("CENTER", UIParent, "CENTER", saved.x, saved.y)
        else
            button:SetPoint("CENTER", UIParent, "CENTER", 0, -144)
        end
    end
    local anchor = addonTable.AttackModeFrame
    if anchor then
        button:SetPoint("TOPLEFT", anchor, "BOTTOMLEFT", 0, 0)
    else
        PlaceSaved()
    end
    background = button:CreateTexture(nil, "BACKGROUND")
    background:SetAllPoints(button)
    icon = button:CreateTexture(nil, "ARTWORK")
    icon:SetSize(18, 18)
    icon:SetPoint("LEFT", button, "LEFT", 3, 0)
    label = button:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    label:SetFont(GameFontNormal:GetFont(), 12, "")
    label:SetPoint("LEFT", icon, "RIGHT", 4, 0)
    label:SetPoint("RIGHT", button, "RIGHT", -3, 0)
    label:SetJustifyH("LEFT")
    local dragging = false
    button:SetScript("OnDragStart", function()
    if addonTable.AttackModeFrame then return end
        if IsShiftKeyDown() then dragging = true; button:StartMoving() end
    end)
    button:SetScript("OnDragStop", function()
        if not dragging then return end
        button:StopMovingOrSizing()
        local x, y = button:GetCenter()
        local centerX, centerY = UIParent:GetCenter()
        position:set_value({ x = x - centerX, y = y - centerY })
        -- 保留本帧标记，防止拖动结束被识别为点击。
        C_Timer.After(0, function() dragging = false end)
    end)
    button:SetScript("OnClick", function()
        if dragging or IsShiftKeyDown() then return end
        CycleState()
    end)
    Refresh()
end)
