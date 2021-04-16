import pygame
from pygame.sprite import Sprite

class Dropping(Sprite):
	"""A class to manage droppings fired from the pigeon."""
	
	def __init__(self, pd_game):
		"""Create a dropping object at the pigeon's current position."""
		super().__init__()
		self.screen = pd_game.screen
		self.settings = pd_game.settings
		self.color = self.settings.dropping_color

		# Create a dropping at (0, 0) and then set the correct position.
		self.rect = pygame.Rect(0, 0, self.settings.dropping_width,
			self.settings.dropping_height)
		self.rect.midbottom = pd_game.pigeon.rect.midbottom

		# Store the dropping's position as a decimal value.
		self.y = float(self.rect.y)

	def update(self):
		"""Move the dropping down the screen."""
		# Update the decimal position of the dropping.
		self.y += self.settings.dropping_speed
		#Update the rect position
		self.rect.y = self.y

	def draw_dropping(self):
		"""Draw the dropping to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)