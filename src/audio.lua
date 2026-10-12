local Audio = {}
Audio.__index = Audio
local function source(path,kind)
    local ok,result=pcall(love.audio.newSource,path,kind)
    if ok then return result end
    print("Audio skipped: " .. path .. " / " .. tostring(result))
end
function Audio.new()
    local self=setmetatable({effects={},muted=false},Audio)
    self.bgm=source("assets/audio/play_bgm.mp3","stream")
    self.clear=source("assets/audio/stage_clear.mp3","stream")
    for i=1,5 do
        local effect=source(string.format("assets/audio/music%02d.wav",i),"static")
        if effect then table.insert(self.effects,effect) end
    end
    if self.bgm then self.bgm:setLooping(true); self.bgm:setVolume(0.35) end
    if self.clear then self.clear:setVolume(0.5) end
    return self
end
function Audio:playBgm()
    if self.clear then self.clear:stop() end
    if self.bgm then self.bgm:stop(); self.bgm:play() end
end
function Audio:effect()
    if #self.effects==0 then return end
    local s=self.effects[love.math.random(#self.effects)]
    s:stop(); s:play()
end
function Audio:stageClear()
    if self.bgm then self.bgm:stop() end
    if self.clear then self.clear:stop(); self.clear:play() end
end
function Audio:toggleMute()
    self.muted=not self.muted
    love.audio.setVolume(self.muted and 0 or 1)
end
return Audio
