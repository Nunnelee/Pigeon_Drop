import pygame.font
from pygame.sprite import Group

from pigeon import Pigeon

class Scoreboard:
	"""A class to report scoring information."""

	def __init__(self, pd_game):
		"""Initialize scorekeeping attributes."""
		self.pd_game = pd_game
		self.screen = pd_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = pd_game.settings
		self.stats = pd_game.stats

		# Font settings foir scoring information.
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		# Prepare the initial score images.
		self.prep_score()
		self.prep_high_score()
		self.prep_pigeons()

	def prep_pigeons(self):
		"""Show how many pigeons are left."""
		self.pigeons = Group()
		for pigeon_number in range(self.stats.pigeons_left):
			pigeon = Pigeon(self.pd_game)
			pigeon.rect.x = 10 + pigeon_number * pigeon.rect.width
			pigeon.rect.y = 1000
			self.pigeons.add(pigeon)


	def prep_score(self):
		"""Turn the score into arendered image."""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True,
				self.text_color, self.settings.bg_color)

		# Display the score at the bottom right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 1000

	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
						self.text_color, self.settings.bg_color)

		# Center the high score at the bottom of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.bottom = self.score_rect.bottom

	def show_score(self):
		"""Draw scores and pigeons to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.pigeons.draw(self.screen)

	def check_high_score(self):
		"""Check to see if there's a new high score."""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()