local Gear = require("src.gear")
local stages = {
    {title="Power transmission", specs={{400,360,80,24,true},{540,360,60,18}},
        links={{1,2}}, target=2},
    {title="Gear ratios", specs={{350,360,100,32,true},{480,360,30,8},{565,360,55,16}},
        links={{1,2},{2,3}}, target=3},
    {title="Rotation direction", specs={{320,360,80,24,true},{445,360,45,12},
        {550,360,60,18},{655,360,45,12}}, links={{1,2},{2,3},{3,4}}, target=4},
    {title="Diagonal transmission", specs={{320,460,60,18,true},{440,360,80,24},
        {555,260,55,16}}, links={{1,2},{2,3}}, target=3},
    {title="Branching power", specs={{480,360,110,36,true},{480,220,40,12},
        {480,100,80,24},{480,520,60,18},{480,625,45,12}},
        links={{1,2},{2,3},{1,4},{4,5}}, target=3}
}

local M = {count=#stages}
function M.create(index)
    local data = assert(stages[index], "Unknown stage")
    local gears = {}
    for _, s in ipairs(data.specs) do
        gears[#gears+1] = Gear.new(s[1],s[2],s[3],s[4],s[5])
    end
    for _, link in ipairs(data.links) do gears[link[1]]:connect(gears[link[2]]) end
    return {gears=gears, target=gears[data.target], requiredAngle=360, title=data.title}
end
return M
