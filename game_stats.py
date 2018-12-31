class GameStats():
    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.game_active = False
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self) -> None:
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
