-- 游戏是否正在进行遭遇战，不附加玩家存活、战斗或目标条件。
local addonName, addonTable = ...

-- Lua 内置方法
local insert = table.insert
local random = math.random

-- WoW API
local CreateFrame = CreateFrame
local After = C_Timer.After
local EvaluateColorFromBoolean = C_CurveUtil.EvaluateColorFromBoolean
local IsEncounterInProgress = C_InstanceEncounter.IsEncounterInProgress

-- 项目引用
local Cell = addonTable.Cell
local COLOR = addonTable.COLOR
local UIInitFuncs = addonTable.UIInitFuncs

local X = 86
local cell
local eventFrame = CreateFrame("Frame")

local function Update()
    if not cell then return end
    local color = EvaluateColorFromBoolean(IsEncounterInProgress(), COLOR.WHITE, COLOR.BLACK)
    cell:setCell(color)
end

local function Initialize()
    cell = Cell:New({ x = X })
    Update()
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
eventFrame:RegisterEvent("ENCOUNTER_STATE_CHANGED")
eventFrame:SetScript("OnEvent", function()
    After(0, Update)
end)

local elapsedTime = -random()
eventFrame:SetScript("OnUpdate", function(_, elapsed)
    elapsedTime = elapsedTime + elapsed
    if elapsedTime >= 1 then
        elapsedTime = elapsedTime % 1
        Update()
    end
end)
insert(UIInitFuncs, Initialize)
