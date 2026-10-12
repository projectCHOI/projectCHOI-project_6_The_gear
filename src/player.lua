local Player = {}
Player.__index = Player
function Player.new()
    local self = setmetatable({selected=nil,lastAngle=nil,hasKey=false,timer=0},Player)
    local ok,img = pcall(love.graphics.newImage,"assets/images/player.png")
    if ok then self.image=img end
    return self
end
local function mouseAngle(gear,x,y)
    if (x-gear.x)^2 + (y-gear.y)^2 < 100 then return nil end
    return math.deg(math.atan2(gear.y-y,x-gear.x))
end
function Player:press(x,y,gears)
    for _,gear in ipairs(gears) do
        if gear.isDriver and gear:contains(x,y) then
            self.selected=gear
            self.lastAngle=mouseAngle(gear,x,y)
            return true
        end
    end
    return false
end
function Player:release()
    self.selected=nil
    self.lastAngle=nil
end
function Player:reset()
    self:release()
    self.hasKey=false
end
function Player:update(dt,x,y)
    self.timer=self.timer+dt
    if not self.selected then return end
    local angle=mouseAngle(self.selected,x,y)
    if angle and self.lastAngle then
        local delta=(angle-self.lastAngle+180)%360-180
        self.selected:rotate(delta)
    end
    self.lastAngle=angle
end
function Player:draw()
    local g=love.graphics
    g.setColor(1,1,1)
    local y=560+(self.selected and math.sin(self.timer*20)*3 or 0)
    if self.image then
        g.draw(self.image,80,y,0,96/self.image:getWidth(),96/self.image:getHeight())
    else
        g.setColor(0.3,0.8,0.4)
        g.rectangle("fill",80,y,96,96)
    end
    g.setColor(0.95,0.87,0.50)
    g.print("BAG: " .. (self.hasKey and "KEY" or "empty"), 210,590)
end
return Player
