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
