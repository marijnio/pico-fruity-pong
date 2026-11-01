-- player.lua
-- modular player table with update and draw hooks

player = {
  x = 52,
  y = 114,
  w = 24,
  h = 4,
  speed = 2,
  col = 7
}

function player.init()
  player.x = 52
  player.y = 114
  player.w = 24
  player.h = 4
  player.speed = 2
  player.col = 7
end

function player.update()
  -- left / right input
  if btn(0) then
    player.x -= player.speed
  end
  if btn(1) then
    player.x += player.speed
  end

  -- clamp paddle within screen boundaries (128x128)
  player.x = mid(0, player.x, 128 - player.w)
end

function player.draw()
  rectfill(player.x, player.y, player.x + player.w - 1, player.y + player.h - 1, player.col)
end

