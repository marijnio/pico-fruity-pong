-- main.lua
-- pico-fruity-pong entry point

function _init()
  player.init()
end

function _update()
  player.update()
end

function _draw()
  -- clear screen to dark blue
  cls(1)

  -- draw a simple test string
  print("pico-fruity-pong", 32, 28, 7)
  print("arrow keys to move", 28, 40, 6)

  -- draw sprite 0 at (60, 60)
  spr(0, 60, 60)

  -- draw player
  player.draw()
end

