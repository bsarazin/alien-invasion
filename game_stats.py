class GameStats():
    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.game_active = False
        self.ai_settings = ai_settings
        self.reset_stats()
        self.score = 0
        self.level = 1
        # High score should never be reset
        self.high_score = 0

    def reset_stats(self) -> None:
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
