local function parse_input_part1(path)
  local f = io.open(path, "r")
  if not f then error("file not found " .. path) end

  local time_in = f:read("*l")
  local dist_in = f:read("*l")

  local races = {}
  for t in time_in:gmatch("%d+") do
    table.insert(races, {time=tonumber(t), dist=nil})
  end

  local i = 1;
  for d in dist_in:gmatch("%d+") do
    races[i].dist = tonumber(d)
    i = i + 1
  end

  return races
end

local function parse_input_part2(path)
  local f = io.open(path, "r")
  if not f then error("file not found " .. path) end

  local time_in = f:read("*l")
  local dist_in = f:read("*l")

  local time_str = time_in:gsub("Time:", ""):gsub(" ", "")
  local dist_str = dist_in:gsub("Distance:", ""):gsub(" ", "")

  return {time=tonumber(time_str), dist=tonumber(dist_str)}
end

local function count_winning(game)
  local time = game.time
  local dist = game.dist

  local count = 0

  for hold=0, time do
    if (hold * (time - hold)) > dist then
      count = count + 1
    end
  end

  return count
end

local function part1(path)
  local races = parse_input_part1(path)

  local product = 1

  for _,v in ipairs(races) do
    product = product * count_winning(v)
  end

  print("Product: " .. product)
end

local function part2(path)
  local race = parse_input_part2(path)

  print("Count: " .. count_winning(race))
end

local function main()
  local f = nil
  if arg[1] == "part1" then
    f = part1
  elseif arg[1] == "part2" then
    f = part2
  else
    error("requred first arg: part1 or part2")
  end
  local path = arg[2]
  if path == nil then
    error("requred second arg: input text path")
  end
  f(path)
end

main()
