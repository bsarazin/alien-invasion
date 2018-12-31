class Settings():
    """a class to store all settings for Alien Invasion"""

    def __init__(self) -> None:
        """Initialize the game settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Ship Settings
        self.ship_limit = 3
        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Fleet Settings
        self.fleet_drop_speed = 10
        # Difficulty Settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Initialize settings the change throughout the game"""
        self.ship_speed_factor = 15
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 80
        # fleet_direction : 1 -> right, -1 -> left
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self) -> None:
        """Increase speed settings and alien point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
