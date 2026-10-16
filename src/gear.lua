local Gear={}; Gear.__index=Gear
function Gear.new(x,y,radius,kind)
 return setmetatable({x=x,y=y,radius=radius,teeth=radius/1.5,kind=kind or 'placed',angle=0,speed=0,powered=false},Gear)
end
function Gear:contains(x,y)
 return (x-self.x)^2+(y-self.y)^2<=(self.radius+4)^2
end
function Gear:draw(alpha)
 local g=love.graphics
 local color=self.kind=='target' and {1,0.76,0.16} or self.kind=='source' and {0.25,0.85,0.72}
  or self.powered and {0.51,0.75,0.97} or {0.48,0.53,0.62}
 g.setColor(color[1],color[2],color[3],alpha or 1)
 g.push(); g.translate(self.x,self.y); g.rotate(self.angle)
 local width=2*math.pi*self.radius/self.teeth*0.5
 for i=1,self.teeth do
  g.push(); g.rotate(i*2*math.pi/self.teeth)
  g.rectangle('fill',self.radius-4,-width/2,8,width,1); g.pop()
 end
 g.circle('fill',0,0,self.radius-3)
 g.setColor(0.08,0.11,0.16,alpha or 1); g.circle('fill',0,0,self.radius*0.63)
 g.setColor(color[1],color[2],color[3],alpha or 1)
 g.setLineWidth(3); g.line(0,0,self.radius-10,0); g.circle('fill',0,0,5)
 g.pop()
end
return Gear
