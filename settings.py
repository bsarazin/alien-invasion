class Settings():
    """a class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Ship Settings
        self.ship_speed_factor = 10
        # Bullet Settings
        self.bullet_speed_factor = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien Settings
        self.alien_speed_factor = 10
        # Fleet Settings
        self.fleet_drop_speed = 10
        # fleet_direction : 1 -> right, -1 -> left
        self.fleet_direction = 1
