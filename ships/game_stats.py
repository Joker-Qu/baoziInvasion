class GameStats():
  def __init__(self,ai_settings):
    self.ai_settings = ai_settings
    self.game_active = False
    self.reset_status()
  def reset_status(self):
    self.ships_left = self.ai_settings.ships_limit
    self.score = 0