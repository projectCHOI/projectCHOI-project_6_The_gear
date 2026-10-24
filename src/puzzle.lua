local Gear=require('src.gear')
local Stages=require('src.stages')
local t=require('src.i18n').t
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
