class Settings:
	"""A class to store all settings for Pigeon Drop."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings.
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (255, 255, 255)

		# Pigeon settings
		self.pigeon_speed = 3
		self.pigeons_limit = 3

		# Dropping setting
		self.dropping_speed = 2
		self.dropping_width = 20
		self.dropping_height = 30
		self.dropping_color = (150, 75, 0)
		self.droppings_allowed = 3

		# Auto settings
		self.auto_speed = 2
		self.fleet_rise_speed = 20
		

		# How quickly the game speeds up
		self.speedup_scale = 1.2

		# How quickly the auto point values increase.
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.pigeon_speed = 3
		self.dropping_speed = 2
		self.auto_speed = 2

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring
		self.auto_points = 50

	def increase_speed(self):
		"""Increase speed settings and auto point values."""
		self.pigeon_speed *= self.speedup_scale
		self.dropping_speed *= self.speedup_scale
		self.auto_speed *= self.speedup_scale

		self.auto_points = int(self.auto_points * self.score_scale)

