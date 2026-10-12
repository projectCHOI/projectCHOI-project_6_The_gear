local Stages = require("src.stages")
local Puzzle = {}
Puzzle.__index = Puzzle
function Puzzle.new()
    local self = setmetatable({}, Puzzle)
    self:load(1)
    return self
end
function Puzzle:load(level)
    self.level = level
    self.stage = Stages.create(level)
    self.phase = "rotate"
    self.box = {x=750,y=310,w=100,h=100}
    self.key = {x=775,y=335,w=50,h=30}
    self.door = {x=1050,y=260,w=120,h=200}
end
function Puzzle:update()
    if self.phase == "rotate" and math.abs(self.stage.target.angle) >= self.stage.requiredAngle then
        self.phase = "collect"
        return "box"
    end
end
local function contains(r,x,y)
    return x>=r.x and x<r.x+r.w and y>=r.y and y<r.y+r.h
end
function Puzzle:click(x,y)
    if self.phase == "collect" and contains(self.key,x,y) then
        self.phase = "unlock"
        return "key"
    elseif self.phase == "unlock" and contains(self.door,x,y) then
        self.phase = "clear"
        return "clear"
    end
end
function Puzzle:next()
    if self.phase == "clear" and self.level < Stages.count then
        self:load(self.level+1)
        return true
    end
    return false
end
function Puzzle:guide()
    if self.phase == "rotate" then return "Drag the GOLD gear around its center. Turn the GREEN target through 360 degrees." end
    if self.phase == "collect" then return "Chest opened! Click the golden KEY inside." end
    if self.phase == "unlock" then return "Key collected! Click the door on the right." end
    if self.level == Stages.count then return "All 5 stages cleared! Press ENTER to play again." end
    return "Stage cleared! Press SPACE for the next room."
end
function Puzzle:draw()
    local g = love.graphics
    for _, gear in ipairs(self.stage.gears) do gear:draw(gear==self.stage.target) end
    local open = self.phase ~= "rotate"
    g.setColor(0.55,0.30,0.13)
    g.rectangle(open and "fill" or "line", self.box.x,self.box.y,self.box.w,self.box.h,6)
    g.setColor(0.95,0.85,0.65)
    g.print(open and "OPEN CHEST" or "LOCKED CHEST", self.box.x-6,self.box.y-28)
    if self.phase == "collect" then
        g.setColor(1,0.82,0.18)
        g.rectangle("fill",self.key.x,self.key.y,self.key.w,self.key.h,4)
        g.setColor(0.15,0.12,0.07)
        g.print("KEY",self.key.x+7,self.key.y+5)
    end
    g.setColor(self.phase=="clear" and 0.30 or 0.65, self.phase=="clear" and 0.75 or 0.40, 0.35)
    g.rectangle(self.phase=="clear" and "fill" or "line",self.door.x,self.door.y,self.door.w,self.door.h,4)
    g.setColor(0.90,0.92,0.96)
    g.print(self.phase=="clear" and "OPEN DOOR" or "LOCKED DOOR",self.door.x,self.door.y-28)
end
return Puzzle
