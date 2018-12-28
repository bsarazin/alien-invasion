class Settings():
    """a class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 10
