import pygame
from pygame.sprite import Sprite

class Auto(Sprite):
	"""A class to represent a single auto in the fleet."""

	def __init__(self, pd_game):
		"""Initialize the auto and set its starting position."""
		super().__init__()
		self.screen = pd_game.screen
		self.settings = pd_game.settings
		
		# Load the auto image and set its rect attribute.
		self.image = pygame.image.load('images/auto.bmp')
		self.rect = self.image.get_rect()

		# Start each new auto near the bottom left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height + 850

		# Store the auto's exact horizontal position.
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Return True if auto is at the edge of screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		"""Move the auto to the right."""
		self.x += (self.settings.auto_speed *
					self.settings.fleet_direction)
		self.rect.x = self.x
