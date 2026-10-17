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
