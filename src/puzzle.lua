local Gear=require('src.gear')
local Stages=require('src.stages')
local Puzzle={}; Puzzle.__index=Puzzle
local function distance(x,y,a,b) return math.sqrt((x-a)^2+(y-b)^2) end
local function inside(r,x,y) return x>=r.x and x<=r.x+r.w and y>=r.y and y<=r.y+r.h end
local function copy(t) local r={}; for k,v in pairs(t) do r[k]=v end; return r end
local sizes={24,36,48}
function Puzzle.new()
 local self=setmetatable({zone={x=280,y=130,w=570,h=440},toolbox={x=25,y=130,w=230,h=440}},Puzzle)
 self:load(1); return self
end
function Puzzle:load(level)
 self.level=level; self.data=Stages.create(level); self.stock=copy(self.data.stock)
 local a,b=self.data.source,self.data.target
 self.source=Gear.new(a.x,a.y,a.radius,'source'); self.target=Gear.new(b.x,b.y,b.radius,'target')
 self.gears={self.source,self.target}; self.drag=nil; self.phase='build'; self.progress=0
 self.jammed=false; self.hint=false; self.notice=''; self.noticeTime=0; self.beltOffset=0
 self.hasKey=false
 self:rebuildNetwork()
end
function Puzzle:message(text) self.notice=text; self.noticeTime=3 end
function Puzzle:rebuildNetwork()
 self.edges={}; self.adj={}
 for _,a in ipairs(self.gears) do a.speed=0; a.powered=false; self.adj[a]={} end
 for i,a in ipairs(self.gears) do
  for j=i+1,#self.gears do
   local b=self.gears[j]
   if math.abs(distance(a.x,a.y,b.x,b.y)-a.radius-b.radius)<=1.5 then
    self.adj[a][#self.adj[a]+1]=b; self.adj[b][#self.adj[b]+1]=a
    self.edges[#self.edges+1]={a,b}
   end
  end
 end
 local q={self.source}; self.source.speed=1.4; self.source.powered=true; local cursor=1
 self.jammed=false
 while cursor<=#q do
  local a=q[cursor]; cursor=cursor+1
  for _,b in ipairs(self.adj[a]) do
   local expected=-a.speed*a.teeth/b.teeth
   if not b.powered then b.powered=true; b.speed=expected; q[#q+1]=b
   elseif math.abs(b.speed-expected)>0.001 then self.jammed=true end
  end
 end
 if self.jammed then for _,a in ipairs(q) do a.speed=0 end end
end
function Puzzle:valid(x,y,r)
 local z=self.zone
 if x-r<z.x+5 or y-r<z.y+5 or x+r>z.x+z.w-5 or y+r>z.y+z.h-5 then return false end
 for _,a in ipairs(self.gears) do
  if distance(x,y,a.x,a.y)<r+a.radius-1 then return false end
 end
 return true
end
-- Snap to one tangent, or an intersection of two tangency circles.
function Puzzle:placement(x,y,r)
 if not inside(self.zone,x,y) then return {x=x,y=y,valid=false} end
 local best,bestD=nil,19
 local function consider(cx,cy)
  local d=distance(x,y,cx,cy)
  if d<bestD and self:valid(cx,cy,r) then best={x=cx,y=cy,valid=true}; bestD=d end
 end
 for _,a in ipairs(self.gears) do
  local d=distance(x,y,a.x,a.y)
  if d>0.01 then consider(a.x+(x-a.x)*(a.radius+r)/d,a.y+(y-a.y)*(a.radius+r)/d) end
 end
 for i,a in ipairs(self.gears) do
  for j=i+1,#self.gears do
   local b=self.gears[j]; local d=distance(a.x,a.y,b.x,b.y); local ra,rb=a.radius+r,b.radius+r
   if d>0.01 and d<=ra+rb and d>=math.abs(ra-rb) then
    local along=(ra*ra-rb*rb+d*d)/(2*d); local h=math.sqrt(math.max(0,ra*ra-along*along))
    local ux,uy=(b.x-a.x)/d,(b.y-a.y)/d
    consider(a.x+along*ux-h*uy,a.y+along*uy+h*ux)
    consider(a.x+along*ux+h*uy,a.y+along*uy-h*ux)
   end
  end
 end
 return best or {x=x,y=y,valid=self:valid(x,y,r)}
end
function Puzzle:slot(i) return {x=45,y=190+(i-1)*118,w=190,h=108} end
function Puzzle:beginDrag(x,y)
 if self.phase~='build' then return end
 for i,r in ipairs(sizes) do
  if inside(self:slot(i),x,y) then
   if self.stock[r]>0 then
    self.stock[r]=self.stock[r]-1; self.drag={radius=r}; self:moveDrag(x,y)
   else self:message('No gears of this size left.') end
   return
  end
 end
 for i=#self.gears,1,-1 do
  local a=self.gears[i]
  if a.kind=='placed' and a:contains(x,y) then
   table.remove(self.gears,i); self.drag={radius=a.radius,original=a,index=i}
   self:rebuildNetwork(); self:moveDrag(x,y); return
  end
 end
end
function Puzzle:moveDrag(x,y)
 if self.drag then self.drag.x=x; self.drag.y=y; self.drag.preview=self:placement(x,y,self.drag.radius) end
end
function Puzzle:cancelDrag()
 local d=self.drag; if not d then return end
 if d.original then table.insert(self.gears,d.index,d.original) else self.stock[d.radius]=self.stock[d.radius]+1 end
 self.drag=nil; self:rebuildNetwork()
end
function Puzzle:endDrag(x,y)
 local d=self.drag; if not d then return end
 if inside(self.toolbox,x,y) then
  self.stock[d.radius]=self.stock[d.radius]+1; self.drag=nil; self:rebuildNetwork(); return 'return'
 end
 local p=self:placement(x,y,d.radius)
 if p.valid then
  local gear=d.original or Gear.new(p.x,p.y,d.radius)
  gear.x=p.x; gear.y=p.y; self.gears[#self.gears+1]=gear
  self.drag=nil; self:rebuildNetwork(); return 'place'
 end
 self:cancelDrag(); self:message('Cannot place here. Keep gears inside the zone without overlap.')
end
function Puzzle:removeAt(x,y)
 if self.phase~='build' or self.drag then return end
 for i=#self.gears,1,-1 do
  local a=self.gears[i]
  if a.kind=='placed' and a:contains(x,y) then
   self.stock[a.radius]=self.stock[a.radius]+1; table.remove(self.gears,i); self:rebuildNetwork(); return 'return'
  end
 end
end
function Puzzle:chestRect() return {x=1059,y=585-self.progress*275,w=92,h=64} end
function Puzzle:keyRect() local b=self:chestRect(); return {x=b.x+22,y=b.y+21,w=50,h=27} end
function Puzzle:click(x,y)
 if self.phase=='raised' and inside(self:chestRect(),x,y) then self.phase='collect'; return 'open' end
 if self.phase=='collect' and inside(self:keyRect(),x,y) then self.phase='unlock'; self.hasKey=true; return 'key' end
 if self.phase=='unlock' and inside({x=1190,y=450,w=60,h=130},x,y) then
  self.phase='clear'; self.hasKey=false; return 'clear'
 end
end
function Puzzle:update(dt)
 self.noticeTime=math.max(0,self.noticeTime-dt)
 local active=self.phase=='build'
 for _,a in ipairs(self.gears) do
  if active then a.angle=(a.angle+a.speed*dt)%(2*math.pi) end
 end
 if active and self.target.powered and not self.jammed then
  -- A ratchet keeps already lifted height; either target direction drives the winch.
  self.progress=math.min(1,self.progress+math.abs(self.target.speed)*dt/(math.pi*4))
  self.beltOffset=(self.beltOffset+math.abs(self.target.speed)*dt*35)%24
  if self.progress>=1 then self:cancelDrag(); self.phase='raised'; return 'raised' end
 end
end
function Puzzle:next()
 if self.phase=='clear' and self.level<Stages.count then self:load(self.level+1); return true end
 return false
end
function Puzzle:guide()
 if self.phase=='raised' then return 'Chest is up! Click the CLOSED CHEST to open it.' end
 if self.phase=='collect' then return 'Click the golden KEY inside the open chest.' end
 if self.phase=='unlock' then return 'Key collected. Click the door at the far right.' end
 if self.phase=='clear' then return self.level==5 and 'All stages cleared! ENTER: play again.' or 'Room complete! SPACE: next stage.' end
 if self.jammed then return 'Gears are JAMMED. Remove a gear from the conflicting loop.' end
 if self.target.powered then return 'Power connected! The winch is raising the chest.' end
 return 'Drag gears from TOOLBOX. Connect the moving green source to the GOLD gear.'
end
return Puzzle
