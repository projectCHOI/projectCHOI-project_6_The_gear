local Puzzle=require("src.puzzle")
local Player=require("src.player")
local Audio=require("src.audio")
local puzzle,player,audio,font,titleFont

function love.load()
    love.graphics.setBackgroundColor(0.09,0.10,0.13)
    font=love.graphics.newFont(17)
    titleFont=love.graphics.newFont(26)
    love.graphics.setFont(font)
    puzzle=Puzzle.new()
    player=Player.new()
    audio=Audio.new()
    audio:playBgm()
end
function love.update(dt)
    if puzzle.phase=="rotate" then
        local x,y=love.mouse.getPosition()
        player:update(dt,x,y)
        if puzzle:update()=="box" then
            player:release()
            audio:effect()
        end
    else
        player:update(dt,0,0)
    end
end
function love.mousepressed(x,y,button)
    if button~=1 then return end
    if puzzle.phase=="rotate" then
        if player:press(x,y,puzzle.stage.gears) then audio:effect() end
    else
        local result=puzzle:click(x,y)
        if result=="key" then player.hasKey=true; audio:effect() end
        if result=="clear" then player.hasKey=false; audio:stageClear() end
    end
end
function love.mousereleased(_,_,button)
    if button==1 then player:release() end
end
function love.focus(focused)
    if not focused then player:release() end
end
function love.keypressed(key)
    if key=="escape" then love.event.quit()
    elseif key=="m" then audio:toggleMute()
    elseif key=="r" then puzzle:load(puzzle.level); player:reset(); audio:playBgm()
    elseif key=="space" then
        if puzzle:next() then player:reset(); audio:playBgm() end
    elseif key=="return" and puzzle.phase=="clear" and puzzle.level==5 then
        puzzle:load(1); player:reset(); audio:playBgm()
    end
end
function love.draw()
    local g=love.graphics
    g.setFont(font)
    puzzle:draw()
    player:draw()
    g.setFont(titleFont)
    g.setColor(0.90,0.93,0.98)
    g.print("STAGE " .. puzzle.level .. " / 5",30,25)
    g.setFont(font)
    g.print(puzzle.stage.title,30,62)
    g.setColor(0.38,0.87,0.71)
    local progress=math.min(1,math.abs(puzzle.stage.target.angle)/360)
    g.rectangle("fill",780,100,progress*370,12,4)
    g.setColor(0.86,0.90,0.95)
    g.print(string.format("TARGET: %.0f / 360 degrees",math.abs(puzzle.stage.target.angle)),780,75)
    g.setColor(0.14,0.17,0.22)
    g.rectangle("fill",0,680,1280,40)
    g.setColor(1,0.91,0.60)
    g.print(puzzle:guide(),30,690)
    g.setColor(0.70,0.76,0.85)
    g.print("R: retry   M: " .. (audio.muted and "sound ON" or "mute") .. "   ESC: quit",840,630)
    if puzzle.phase=="clear" then
        g.setFont(titleFont)
        g.setColor(0.45,1,0.65)
        g.printf(puzzle.level==5 and "ALL STAGES CLEARED!" or "STAGE CLEAR!",740,510,480,"center")
    end
end
