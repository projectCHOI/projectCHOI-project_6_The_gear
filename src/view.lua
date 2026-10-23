local Gear=require('src.gear')
local I18n=require('src.i18n')
local t=I18n.t
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
 text(t('heading',p.level),25,22)
 g.setFont(font); text(t('stage'..p.level),27,65,{0.45,0.82,0.76})
 text(t('shortcuts'),720,36)
 panel(25,110,230,470); panel(275,110,580,470); panel(875,110,385,490)
 text(t('toolbox'),45,133,{1,0.80,0.36})
 text(t('drag'),45,159)
 text(t('zone'),295,120)
 text(t('winch'),895,130,{1,0.80,0.36})
 -- Workshop peg-board grid.
 g.setColor(0.18,0.23,0.30)
 for x=295,840,24 do for y=155,555,24 do g.circle('fill',x,y,1) end end
 for i,r in ipairs({24,36,48}) do
  local box=p:slot(i)
  g.setColor(0.14,0.19,0.27); g.rectangle('fill',box.x,box.y,box.w,box.h,9)
  local icon=Gear.new(103,box.y+53,r); icon:draw(p.stock[r]>0 and 1 or 0.25)
  text(t(({[24]='small',[36]='medium',[48]='large'})[r]),163,box.y+23)
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
