local I18n=require('src.i18n')
local Player={}; Player.__index=Player
function Player.new()
 local self=setmetatable({timer=0},Player)
 local ok,img=pcall(love.graphics.newImage,'assets/images/player.png')
 if ok then self.image=img end
 return self
end
function Player:update(dt) self.timer=self.timer+dt end
function Player:draw(hasKey)
 local g=love.graphics; g.setColor(1,1,1)
 if self.image then g.draw(self.image,32,592,0,64/self.image:getWidth(),64/self.image:getHeight()) end
 g.setColor(0.94,0.83,0.52); g.print(hasKey and I18n.t('bagKey') or I18n.t('bagEmpty'),114,618)
end
return Player
