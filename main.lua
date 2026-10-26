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
function love.mousepressed(x,y,button)
 if screen=='language' then
  if button==1 then
   for _,b in ipairs(buttons) do
    if contains(b,x,y) then startGame(b.language);return end
   end
  end
  return
 end
 if button==1 then
  if puzzle.phase=='build' then puzzle:beginDrag(x,y) else soundFor(puzzle:click(x,y)) end
 elseif button==2 then soundFor(puzzle:removeAt(x,y)) end
end
function love.mousereleased(x,y,button)
 if screen=='game' and button==1 then soundFor(puzzle:endDrag(x,y)) end
end
function love.focus(focused)
 if screen=='game' and not focused then puzzle:cancelDrag() end
end
function love.keypressed(key)
 if screen=='language' then
  if key=='escape' then love.event.quit() end
  return
 end
 if key=='escape' then
  if puzzle.drag then puzzle:cancelDrag() else love.event.quit() end
 elseif key=='r' then puzzle:load(puzzle.level);audio:playBgm()
 elseif key=='h' then puzzle.hint=not puzzle.hint
 elseif key=='m' then audio:toggleMute()
 elseif key=='space' then if puzzle:next() then audio:playBgm() end
 elseif key=='return' and puzzle.phase=='clear' and puzzle.level==5 then puzzle:load(1);audio:playBgm() end
end
local function drawLanguageMenu()
 local g=love.graphics
 local x,y=love.mouse.getPosition()
 g.setFont(titleFont);g.setColor(0.90,0.94,1)
 g.printf('THE GEAR : THE PUZZLER',0,130,1280,'center')
 g.setFont(font);g.setColor(0.57,0.77,0.86)
 g.printf(fontReady and '언어를 선택하세요 / Choose your language' or 'Choose your language',0,205,1280,'center')
 for _,b in ipairs(buttons) do
  local enabled=b.language=='en' or fontReady
  local hovered=enabled and contains(b,x,y)
  g.setColor(hovered and {0.16,0.36,0.38} or {0.10,0.16,0.23})
  g.rectangle('fill',b.x,b.y,b.w,b.h,12)
  g.setColor(enabled and (hovered and {0.40,0.95,0.78} or {0.30,0.52,0.64}) or {0.30,0.30,0.33})
  g.setLineWidth(2);g.rectangle('line',b.x,b.y,b.w,b.h,12)
  g.setFont(titleFont);g.setColor(enabled and {0.93,0.96,1} or {0.50,0.50,0.53})
  g.printf(b.language=='ko' and (fontReady and '한국어' or 'Korean (font required)') or 'English',b.x,b.y+25,b.w,'center')
 end
 g.setFont(font);g.setColor(0.72,0.77,0.83)
 g.printf(fontReady and '원하는 언어를 마우스로 클릭하세요. / Click a language to begin.' or 'Add assets/font/SLEIGothicOTF.otf and restart to enable Korean.',100,525,1080,'center')
 g.printf('ESC: '..(fontReady and '종료 / Quit' or 'Quit'),0,610,1280,'center')
end
function love.draw()
 if screen=='language' then drawLanguageMenu();return end
 View.draw(puzzle,font,titleFont)
 love.graphics.setFont(font);player:draw(puzzle.hasKey)
end
