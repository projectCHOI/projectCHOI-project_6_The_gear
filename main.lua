local Puzzle=require('src.puzzle')
local Player=require('src.player')
local Audio=require('src.audio')
local View=require('src.view')
local puzzle,player,audio,font,titleFont
function love.load()
 love.graphics.setBackgroundColor(0.06,0.08,0.12)
 font=love.graphics.newFont(15); titleFont=love.graphics.newFont(25)
 puzzle=Puzzle.new(); player=Player.new(); audio=Audio.new(); audio:playBgm()
end
local function soundFor(event)
 if event=='clear' then audio:stageClear()
 elseif event then audio:effect() end
end
function love.update(dt)
 local x,y=love.mouse.getPosition(); puzzle:moveDrag(x,y)
 soundFor(puzzle:update(math.min(dt,0.1))); player:update(dt)
end
function love.mousepressed(x,y,button)
 if button==1 then
  if puzzle.phase=='build' then puzzle:beginDrag(x,y) else soundFor(puzzle:click(x,y)) end
 elseif button==2 then soundFor(puzzle:removeAt(x,y)) end
end
function love.mousereleased(x,y,button)
 if button==1 then soundFor(puzzle:endDrag(x,y)) end
end
function love.focus(focused) if not focused then puzzle:cancelDrag() end end
function love.keypressed(key)
 if key=='escape' then
  if puzzle.drag then puzzle:cancelDrag() else love.event.quit() end
 elseif key=='r' then puzzle:load(puzzle.level); audio:playBgm()
 elseif key=='h' then puzzle.hint=not puzzle.hint
 elseif key=='m' then audio:toggleMute()
 elseif key=='space' then if puzzle:next() then audio:playBgm() end
 elseif key=='return' and puzzle.phase=='clear' and puzzle.level==5 then puzzle:load(1); audio:playBgm() end
end
function love.draw()
 View.draw(puzzle,font,titleFont)
 love.graphics.setFont(font); player:draw(puzzle.hasKey)
end
