-- 第 64 格显示玩家自身可驱散的中毒或疾病：存在为白色，否则为黑色。
-- 原生光环容器负责匹配与显隐，不读取秘密光环数据。
local addonName, addonTable    = ...

-- Lua 内置方法
local insert                  = table.insert

-- WoW API
local CreateFrame             = CreateFrame
local After                   = C_Timer.After

-- 项目引用
local Cell                    = addonTable.Cell
local COLOR                   = addonTable.COLOR
local SIZE                    = addonTable.SIZE
local FrameLevel              = addonTable.FrameLevel
local UIInitFuncs             = addonTable.UIInitFuncs

-- 本地配置与状态
local X = 64
local DISPEL_TYPES = { Poison = true, Disease = true }
local eventFrame              = CreateFrame("Frame")
local container

local function Refresh()
    if not container then
        return
    end
    container:UpdateAllAuras()
end

local function Initialize()
    local cell = Cell:New({ x = X })
    container = CreateFrame("AuraContainer", nil, cell.Frame, "CustomAuraContainerTemplate")
    container:SetAllPoints(cell.Frame)
    container:SetFrameLevel(FrameLevel.AuraContainer)
    container:SetUnit("player")

    container:AddAuraSlot("aura", "HARMFUL|RAID_PLAYER_DISPELLABLE", {
        candidateFilters = { includeDispelTypes = DISPEL_TYPES },
        initializeFrame = function(frame)
            frame:SetSize(SIZE.CELL, SIZE.CELL)
            frame:SetPoint("TOPLEFT", container, "TOPLEFT")
            frame:SetFrameLevel(FrameLevel.AuraButton)
            local color = COLOR.WHITE
            local overlay = frame:CreateTexture(nil, "OVERLAY")
            overlay:SetAllPoints(frame)
            overlay:SetTexture("Interface\\Buttons\\WHITE8X8")
            overlay:SetVertexColor(color:GetRGBA())
        end,
    })
    Refresh()
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
eventFrame:SetScript("OnEvent", function()
    After(0, Refresh)
end)
insert(UIInitFuncs, Initialize)
