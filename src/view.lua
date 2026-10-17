local Gear=require('src.gear')
local View={}
local function text(s,x,y,color)
 love.graphics.setColor(color or {0.86,0.90,0.95}); love.graphics.print(s,x,y)
end
local function panel(x,y,w,h)
 local g=love.graphics
 g.setColor(0.10,0.14,0.20); g.rectangle('fill',x,y,w,h,14)
 g.setColor(0.23,0.30,0.40); g.setLineWidth(1); g.rectangle('line',x,y,w,h,14)
end
local function pulley(x,y,angle)
 local p=Gear.new(x,y,22,'placed'); p.angle=angle; p.powered=true; p:draw()
end
function View.draw(p,font,titleFont)
 local g=love.graphics
 g.setFont(titleFont)
 text('THE GEAR / STAGE '..p.level..' OF 5',25,22)
 g.setFont(font); text(p.data.title,27,65,{0.45,0.82,0.76})
 text('R: retry   H: placement hint   M: mute   ESC: quit',720,36)
 panel(25,110,230,470); panel(275,110,580,470); panel(875,110,385,490)
 text('TOOLBOX',45,133,{1,0.80,0.36})
 text('Drag a gear into the zone',45,159)
 text('GAME ZONE',295,120)
 text('WINCH / WELL',895,130,{1,0.80,0.36})
 -- Workshop peg-board grid.
 g.setColor(0.18,0.23,0.30)
 for x=295,840,24 do for y=155,555,24 do g.circle('fill',x,y,1) end end
 for i,r in ipairs({24,36,48}) do
  local box=p:slot(i)
  g.setColor(0.14,0.19,0.27); g.rectangle('fill',box.x,box.y,box.w,box.h,9)
  local icon=Gear.new(103,box.y+53,r); icon:draw(p.stock[r]>0 and 1 or 0.25)
  text(({[24]='SMALL',[36]='MEDIUM',[48]='LARGE'})[r],163,box.y+23)
  text('x '..p.stock[r],170,box.y+54,{1,0.83,0.42})
 end
 -- Fixed frame and orange drive belt around the three pulleys.
 g.setColor(0.43,0.30,0.67)
 g.rectangle('fill',965,160,10,355); g.rectangle('fill',1140,160,10,355)
 g.rectangle('fill',965,157,185,10)
 local path={913,430,913,190,935,168,1105,168,1127,190,1105,212,957,212,957,430,935,452,913,430}
 g.setColor(0.95,0.58,0.19); g.setLineWidth(6); g.line(path)
 -- Moving belt marks make transmission visible even on a symmetric wheel.
 local travelled=0
 for i=1,#path-2,2 do
  local x,y,xx,yy=path[i],path[i+1],path[i+2],path[i+3]
  local len=math.sqrt((xx-x)^2+(yy-y)^2)
  local t=(p.beltOffset-travelled)%24
  while t<len do
   g.setColor(1,0.84,0.48); g.circle('fill',x+(xx-x)*t/len,y+(yy-y)*t/len,2)
   t=t+24
  end
  travelled=travelled+len
 end
 -- Gold gear shaft / coupling transmits into the lower winch pulley.
 g.setColor(p.target.powered and {0.90,0.69,0.22} or {0.30,0.34,0.40})
 g.setLineWidth(3); g.line(p.target.x+p.target.radius+5,p.target.y,885,p.target.y,900,430,913,430)
 pulley(935,430,p.progress*math.pi*4); pulley(935,190,p.progress*math.pi*4)
 pulley(1105,190,p.progress*math.pi*4)
 local chest=p:chestRect()
 g.setScissor(990,150,195,370)
 g.setColor(0.33,0.67,1); g.setLineWidth(3); g.line(1105,190,1105,chest.y)
 local opened=p.phase=='collect' or p.phase=='unlock' or p.phase=='clear'
 g.setColor(0.53,0.30,0.14); g.rectangle('fill',chest.x,chest.y,chest.w,chest.h,5)
 g.setColor(0.93,0.66,0.25); g.setLineWidth(3); g.rectangle('line',chest.x,chest.y,chest.w,chest.h,5)
 if opened then
  g.setColor(0.12,0.09,0.07); g.rectangle('fill',chest.x+7,chest.y+7,chest.w-14,chest.h-14,3)
  g.setColor(0.69,0.41,0.21); g.rectangle('fill',chest.x,chest.y-22,chest.w,20,4)
 else
  g.setColor(0.92,0.67,0.27); g.rectangle('fill',chest.x,chest.y+21,chest.w,6)
  g.rectangle('fill',chest.x+39,chest.y+26,14,17,2)
 end
 if p.phase=='collect' then
  local k=p:keyRect(); g.setColor(1,0.84,0.19)
  g.setLineWidth(4); g.circle('line',k.x+11,k.y+12,8); g.line(k.x+19,k.y+12,k.x+44,k.y+12,k.x+44,k.y+21)
  g.line(k.x+36,k.y+12,k.x+36,k.y+19)
 end
 g.setScissor()
 -- Opaque well front hides the chest when it is below the rim.
 g.setColor(0.15,0.20,0.27); g.rectangle('fill',1000,520,175,80,5)
 g.setColor(0.38,0.46,0.56); g.rectangle('fill',994,513,187,14,3)
 text('WELL',1060,554)
 if p.phase=='raised' then text('CLICK CHEST',1050,chest.y-28,{1,0.84,0.40}) end
 -- Door stays locked until the key is collected.
 g.setColor(p.phase=='clear' and {0.28,0.72,0.63} or {0.44,0.29,0.20})
 g.rectangle('fill',1190,450,60,130,5)
 g.setColor(0.95,0.78,0.33); g.circle('fill',1237,520,4)
 text(p.phase=='clear' and 'OPEN' or 'DOOR',1194,425)
 text(string.format('LIFT: %d%%',math.floor(p.progress*100)),895,620,{0.40,0.86,0.74})
 g.setColor(0.19,0.26,0.34); g.rectangle('fill',1020,620,230,12,4)
 g.setColor(0.35,0.80,0.65); g.rectangle('fill',1020,620,230*p.progress,12,4)
 if p.hint and p.phase=='build' then
  for i,s in ipairs(p.data.solution) do
   g.setColor(0.72,0.84,1,0.35); g.setLineWidth(1)
   g.circle('line',s.x,s.y,s.radius); g.print(tostring(i),s.x-4,s.y-8)
  end
 end
 for _,edge in ipairs(p.edges) do
  local a,b=edge[1],edge[2]
  g.setColor(a.powered and {0.25,0.55,0.49,0.5} or {0.25,0.30,0.37,0.5})
  g.setLineWidth(2); g.line(a.x,a.y,b.x,b.y)
 end
 for _,a in ipairs(p.gears) do a:draw() end
 text('AUTO',p.source.x-22,p.source.y-p.source.radius-26,{0.37,0.95,0.78})
 text('GOAL',p.target.x-23,p.target.y+p.target.radius+12,{1,0.83,0.36})
 if p.drag then
  local preview=p.drag.preview
  local ghost=Gear.new(preview.x,preview.y,p.drag.radius)
  ghost:draw(0.70)
  g.setColor(preview.valid and {0.35,1,0.60,0.8} or {1,0.30,0.30,0.8})
  g.setLineWidth(2); g.circle('line',preview.x,preview.y,p.drag.radius+7)
 end
 if p.jammed then text('JAMMED: remove a gear',475,550,{1,0.43,0.35}) end
 if p.noticeTime>0 then text(p.notice,280,650,{1,0.73,0.40})
 else text('Move placed gears by dragging. Right-click returns a gear. H shows a possible route.',280,650) end
 g.setColor(0.12,0.17,0.23); g.rectangle('fill',0,682,1280,38)
 text(p:guide(),25,691,{1,0.88,0.53})
 if p.phase=='clear' then
  g.setFont(titleFont); text(p.level==5 and 'ALL STAGES CLEAR!' or 'STAGE CLEAR!',878,76,{0.41,0.95,0.71})
 end
end
return View
