-- 显示当前施法或引导图标，空闲时清空图标和角标。
local addonName, addonTable    = ...

-- lua 内置方法
local insert = table.insert
local random = math.random

-- wow api
local CreateFrame = CreateFrame
local After = C_Timer.After
local UnitCastingInfo = UnitCastingInfo
local UnitChannelInfo = UnitChannelInfo
local UnitExists = UnitExists
local issecretvalue = issecretvalue
local EvaluateColorFromBoolean = C_CurveUtil.EvaluateColorFromBoolean

-- 项目引用
local COLOR = addonTable.COLOR
local UIInitFuncs = addonTable.UIInitFuncs
local IconTile = addonTable.IconTile

-- 本地配置
local X = 20
local eventFrame = CreateFrame("Frame")
local display

local function Refresh()
    if not display then return end
    if not UnitExists("mouseover") then display:Clear(); return end
    local _, _, texture, _, _, _, _, blocked, _, _, delayTime = UnitCastingInfo("mouseover")
    if delayTime == nil then
        local _, _, channelTexture, _, _, _, channelBlocked, _, empowered = UnitChannelInfo("mouseover")
        if empowered == nil then display:Clear(); return end
        texture = channelTexture
        blocked = channelBlocked
    end
    if not issecretvalue(blocked) and blocked == nil then blocked = true end
    local color = EvaluateColorFromBoolean(blocked, COLOR.SPELL_TYPE.NOT_INTERRUPTIBLE, COLOR.SPELL_TYPE.INTERRUPTIBLE)
    display:SetIcon(texture)
    display:SetBorderColor(color)
end

local function Initialize()
    display = IconTile:New(X)
    Refresh()
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
eventFrame:RegisterEvent("UPDATE_MOUSEOVER_UNIT")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_START", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_STOP", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_INTERRUPTED", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_FAILED", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_FAILED_QUIET", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_DELAYED", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_SUCCEEDED", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_START", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_STOP", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_UPDATE", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_START", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_STOP", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_UPDATE", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_INTERRUPTIBLE", "mouseover")
eventFrame:RegisterUnitEvent("UNIT_SPELLCAST_NOT_INTERRUPTIBLE", "mouseover")
eventFrame:SetScript("OnEvent", function(_, event)
    After(0, function()
        Refresh()
    end)
end)
local elapsedTime = -random() * 0.1
eventFrame:SetScript("OnUpdate", function(_, elapsed)
    elapsedTime = elapsedTime + elapsed
    if elapsedTime >= 0.1 then
        elapsedTime = elapsedTime % 0.1
        Refresh()
    end
end)
insert(UIInitFuncs, Initialize)
