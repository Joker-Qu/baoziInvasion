class Settings():
  def __init__(self):
    self.screen_width = 1200
    self.screen_height = 800
    self.bg_color = (230,230,230)
    self.ship_speed = 2
    self.bullet_speed = 5
    self.bullet_width = 3
    self.bullet_height = 15
    self.bullet_color = (60,60,60)
    self.bullet_allowd = 3
    self.alien_speed = 2
    self.fleet_drop_speed = 20
    # 1 右移 -1 左移
    self.fleet_direction = 1
    self.ships_limit = 3