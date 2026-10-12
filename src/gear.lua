local Gear = {}
Gear.__index = Gear

function Gear.new(x, y, radius, teeth, driver)
    return setmetatable({x=x, y=y, radius=radius, teeth=teeth,
        isDriver=driver or false, angle=0, connections={}}, Gear)
end

function Gear:connect(other)
    for _, gear in ipairs(self.connections) do
        if gear == other then return end
    end
    table.insert(self.connections, other)
    table.insert(other.connections, self)
end

-- Angles are degrees; positive rotation is counterclockwise.
-- This model supports the original tree-shaped gear networks.
function Gear:rotate(delta, visited)
    visited = visited or {}
    if visited[self] then return end
    visited[self] = true
    self.angle = self.angle + delta
    for _, other in ipairs(self.connections) do
        other:rotate(-delta * self.teeth / other.teeth, visited)
    end
end

function Gear:contains(x, y)
    return (x-self.x)^2 + (y-self.y)^2 <= self.radius^2
end

function Gear:draw(target)
    local g = love.graphics
    g.push()
    g.translate(self.x, self.y)
    g.rotate(-math.rad(self.angle % 360))
    g.setColor(self.isDriver and 0.85 or 0.45, self.isDriver and 0.65 or 0.55, 0.30)
    -- Decorative teeth; rotation ratios use the logical tooth counts.
    for i=0,self.teeth-1 do
        g.push()
        g.rotate(i * 2 * math.pi / self.teeth)
        g.rectangle("fill", self.radius-9, -4, 13, 8, 2)
        g.pop()
    end
    g.circle("fill", 0, 0, self.radius-5)
    g.setColor(0.12, 0.14, 0.18)
    g.circle("fill", 0, 0, self.radius*0.64)
    g.setColor(0.98, 0.40, 0.30)
    g.setLineWidth(4)
    g.line(0, 0, self.radius-14, 0)
    g.setColor(0.85, 0.88, 0.93)
    g.circle("fill", 0, 0, 8)
    g.pop()
    if target then
        g.setColor(0.35, 0.90, 0.70)
        g.setLineWidth(2)
        g.circle("line", self.x, self.y, self.radius+10)
    end
    g.setColor(0.90, 0.92, 0.96)
    g.printf(self.teeth .. " teeth", self.x-self.radius, self.y+self.radius+14,
        self.radius*2, "center")
end

return Gear
