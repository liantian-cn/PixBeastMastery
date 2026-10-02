-- 玩家野兽顺劈（Beast Cleave）增益 268877 的剩余秒数。
-- 原生光环容器与字体颜色绑定负责计时，不读取秘密光环数据。
local addonName, addonTable    = ...

-- Lua 内置方法
local insert                  = table.insert
local ipairs                  = ipairs

-- WoW API
local CreateFrame             = CreateFrame
local After                   = C_Timer.After
local GameFontNormal          = GameFontNormal
local CreateDurationTextBinding = C_DurationUtil.CreateDurationTextBinding
local RemainingDuration       = Enum.DurationTextBindingProperty.RemainingDuration

-- 项目引用
local Cell                    = addonTable.Cell
local COLOR                   = addonTable.COLOR
local SIZE                    = addonTable.SIZE
local FrameLevel              = addonTable.FrameLevel
local UIInitFuncs             = addonTable.UIInitFuncs
local AuraRemaining           = addonTable.CURVE.AuraRemaining

-- 本地配置与状态
local X = 85
local AURA_IDS = { 268877 }
local CHARACTER = "█"
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

    local includeSpellIDs = {}
    for _, spellID in ipairs(AURA_IDS) do
        includeSpellIDs[spellID] = true
    end
    container:AddAuraSlot("aura", "HELPFUL|PLAYER", {
        candidateFilters = { includeSpellIDs = includeSpellIDs },
        initializeFrame = function(frame)
            frame:SetSize(SIZE.CELL, SIZE.CELL)
            frame:SetPoint("TOPLEFT", container, "TOPLEFT")
            frame:SetFrameLevel(FrameLevel.AuraButton)
            frame:SetClipsChildren(true)

            local color = COLOR.WHITE
            local background = frame:CreateTexture(nil, "BACKGROUND")
            background:SetAllPoints(frame)
            background:SetTexture("Interface\\Buttons\\WHITE8X8")
            background:SetVertexColor(color:GetRGBA())

            local fontPath = GameFontNormal:GetFont()
            local text = frame:CreateFontString(nil, "ARTWORK")
            text:SetFont(fontPath, SIZE.CELL_FONT_SIZE, "")
            text:SetPoint("CENTER", frame, "CENTER", 0, 0)
            text:SetJustifyH("CENTER")
            text:SetJustifyV("MIDDLE")
            text:SetShadowOffset(0, 0)
            text:SetShadowColor(0, 0, 0, 0)
            text:SetTextColor(color:GetRGBA())

            local binding = CreateDurationTextBinding()
            binding:SetZeroDurationText("")
            binding:SetExpiredText(CHARACTER)
            frame:SetDurationText(text, {
                binding = binding,
                textFormat = { formatString = CHARACTER, components = {} },
                textColor = { curve = AuraRemaining, property = RemainingDuration },
            })
        end,
    })
    Refresh()
end

eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
eventFrame:SetScript("OnEvent", function()
    After(0, Refresh)
end)
insert(UIInitFuncs, Initialize)
