local Puzzle=require('src.puzzle')
local Player=require('src.player')
local Audio=require('src.audio')
local View=require('src.view')
local I18n=require('src.i18n')
local puzzle,player,audio,font,titleFont
local screen='language'
local fontReady=false
local fontPath='assets/font/SLEIGothicOTF.otf'
local buttons={
 {language='ko',x=390,y=275,w=500,h=85},
 {language='en',x=390,y=390,w=500,h=85}
}
local function contains(button,x,y)
 return x>=button.x and x<=button.x+button.w and y>=button.y and y<=button.y+button.h
end
function love.load()
 love.graphics.setBackgroundColor(0.06,0.08,0.12)
 local ok,normal,heading=pcall(function()
  return love.graphics.newFont(fontPath,15),love.graphics.newFont(fontPath,25)
 end)
 fontReady=ok
 if ok then font=normal;titleFont=heading
 else
  font=love.graphics.newFont(15);titleFont=love.graphics.newFont(25)
  print('Font could not be loaded: '..fontPath..' / '..tostring(normal))
 end
 -- No game objects or background music are started before language selection.
 screen='language';puzzle=nil;player=nil;audio=nil
end
local function startGame(language)
 -- Default fonts cannot display Korean reliably. Keep the menu visible if missing.
 if language=='ko' and not fontReady then return end
 I18n.set(language)
 puzzle=Puzzle.new();player=Player.new();audio=Audio.new()
 screen='game';audio:playBgm()
end
local function soundFor(event)
 if event=='clear' then audio:stageClear()
 elseif event then audio:effect() end
end
function love.update(dt)
 if screen~='game' then return end
 local x,y=love.mouse.getPosition();puzzle:moveDrag(x,y)
 soundFor(puzzle:update(math.min(dt,0.1)));player:update(dt)
end
