import pygame
from pygame.sprite import Sprite

class Pigeon(Sprite):
	"""A class to manage the pigeon."""

	def __init__(self, pd_game):
		"""Initialize the pigeon and st its starting position."""
		super().__init__()
		self.screen = pd_game.screen
		self.settings = pd_game.settings
		self.screen_rect = pd_game.screen.get_rect()

		# Load the pigeon and get its rect.
		self.image = pygame.image.load('images/pigeon.bmp')
		self.rect = self.image.get_rect()
		# Start each new pigeon at the top center of the screen.
		self.rect.midtop = self.screen_rect.midtop

		# Store a decimal value for the pigeon's horizontal position.
		self.x = float(self.rect.x)

		# Movement flags
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update the pigeon's position based on the movement flags."""
		# Update the pigeon's x value, not the rect.
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.pigeon_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.pigeon_speed

		# Update the rect object from self.x
		self.rect.x = self.x

	def blitme(self):
		# Draw the pigeon at its current location.
		self.screen.blit(self.image, self.rect)

	def center_pigeon(self):
		"""Center the pigeon on the screen."""
		self.rect.midtop = self.screen_rect.midtop
		self.x = float(self.rect.x)