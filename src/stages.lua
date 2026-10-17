-- Each stage has a verified example route, but placements are free-form.
local M={count=5}
local definitions={
 {title='First connection',x=340,y=300,radii={36,36,36,36,36},directions={0,0,0,0,0,0}},
 {title='Mix the sizes',x=340,y=230,radii={48,24,36,48,24},directions={0,0,0,0,0,0}},
 {title='Turn the corner',x=340,y=200,radii={36,36,36,36,36},directions={0,0,45,45,0,0}},
 {title='Climb the chain',x=340,y=440,radii={24,48,36,24,48},directions={0,-45,0,-45,0,0}},
 {title='The final workshop',x=340,y=190,radii={48,36,24,48,36,24},directions={45,0,45,0,-45,0,0}}
}
function M.create(index)
 local d=assert(definitions[index],'Unknown stage')
 local result={title=d.title,source={x=d.x,y=d.y,radius=36},stock={[24]=0,[36]=0,[48]=0},solution={}}
 local x,y,r=d.x,d.y,36
 for i=1,#d.radii+1 do
  local nextR=d.radii[i] or 36
  local a=math.rad(d.directions[i])
  x=x+(r+nextR)*math.cos(a); y=y+(r+nextR)*math.sin(a)
  if i<=#d.radii then
   result.solution[i]={x=x,y=y,radius=nextR}
   result.stock[nextR]=result.stock[nextR]+1
  else result.target={x=x,y=y,radius=nextR} end
  r=nextR
 end
 -- One optional spare; stocks are reset for every room.
 result.stock[24]=result.stock[24]+1
 return result
end
return M
