import sys
from time import sleep
import pygame

from settings import Settings 
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from pigeon import Pigeon 
from dropping import Dropping
from auto import Auto

class PigeonDrop:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Pigeon Drop!")

		# Create an instance to store game statistics,
		# and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.pigeon = Pigeon(self)
		self.droppings = pygame.sprite.Group()
		self.autos = pygame.sprite.Group()

		self._create_fleet()

		# Make the Play button.
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			
			if self.stats.game_active:
				self.pigeon.update()
				self._update_droppings()
				self._update_autos()

			self._update_screen()

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		# Watch for keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Reset the game settings.
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_pigeons()
			# Hide the cursor.
			pygame.mouse.set_visible(False)

		# Get rid of any remaining autos and droppings.
		self.autos.empty()
		self.droppings.empty()

		# Create a new fleet and center the pigeon
		self._create_fleet()
		self.pigeon.center_pigeon()

	def _check_keydown_events(self, event):
		"""Respond to keypresses."""
		if event.key == pygame.K_RIGHT:
			self.pigeon.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.pigeon.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_dropping()

	def _check_keyup_events(self, event):
		"""Respond to key releases."""	
		if event.key == pygame.K_RIGHT:
			self.pigeon.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.pigeon.moving_left = False

	def _pigeon_hit(self):
		"""Respond to the pigeon being hit by an auto."""
		if self.stats.pigeons_left > 0:
			# Decrement pigeons_left and update scoreboard.
			self.stats.pigeons_left -= 1
			self.sb.prep_pigeons()

			# Get rid of any remaining autos and droppings.
			self.autos.empty()
			self.droppings.empty()

			# Create a new fleet and center the pigeon.
			self._create_fleet()
			self.pigeon.center_pigeon()

			# Pause.
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _create_fleet(self):
		"""Create a fleet of autos."""
		# Create an auto and find the number of autos in a row.
		# Spacing between each auto is equal to one auto width.
		auto = Auto(self)
		auto_width, auto_height = auto.rect.size
		available_space_x = self.settings.screen_width - (2 * auto_width)
		number_autos_x = available_space_x // (2 * auto_width)

		# Determine the number of rows of autos that fit on the screen.
		pigeon_height = self.pigeon.rect.height
		available_space_y = (self.settings.screen_height -
						(3 * auto_height) - pigeon_height)
		number_rows = available_space_y // (2 * auto_height)

		# Create the full fleet of autos.
		for row_number in range(number_rows):
			for auto_number in range(number_autos_x):
				self._create_auto(auto_number, row_number)

	def _create_auto(self, auto_number, row_number):
		"""Create an auto and place it in the row."""
		auto = Auto(self)
		auto_width, auto_height = auto.rect.size
		auto.x = auto_width + 2 * auto_width * auto_number
		auto.rect.x = auto.x 
		auto.rect.y = auto_height + 2 * auto.rect.height * row_number + 450
		self.autos.add(auto)	

	
	def _fire_dropping(self):
		"""Create a new dropping and add it to the droppings group."""
		if len(self.droppings) < self.settings.droppings_allowed:
			new_dropping = Dropping(self)
			self.droppings.add(new_dropping)

	def _update_droppings(self):
		"""Update the position of droppings and get rid of the droppings."""
		# Update dropping positions.
		self.droppings.update()

		# Get rid of the droppings that have disappeared.
		for dropping in self.droppings.copy():
			if dropping.rect.top >= 1050:
				self.droppings.remove(dropping)

		self._check_dropping_auto_collisions()

	def _check_dropping_auto_collisions(self):
		"""Respond to dropping-auto collisions."""
		# Remove any droppings and autos that have collided.
		collisions = pygame.sprite.groupcollide(
		self.droppings, self.autos, True, True)

		if collisions:
			for autos in collisions.values():
				self.stats.score += self.settings.auto_points * len(autos)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.autos:
			# Destroy existing droppings and create new fleet.
			self.droppings.empty()
			self._create_fleet()
			self.settings.increase_speed()

	def _update_autos(self):
		"""
		Check if the fleet is at an edge
			then update the positions of all autos in the fleet.
		"""
		self._check_fleet_edges()
		self.autos.update()

		# Look for auto-pigeon collisions.
		if pygame.sprite.spritecollideany(self.pigeon, self.autos):
			self._pigeon_hit()

		# Look for autos hitting the top of the screen.
		self._check_autos_top()

	def _check_fleet_edges(self):
		"""Respond appropiately if any autos have reached an edge."""
		for auto in self.autos.sprites():
			if auto.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Raise the entire fleet and change the fleet's direction."""
		for auto in self.autos.sprites():
			auto.rect.y -= self.settings.fleet_rise_speed
		self.settings.fleet_direction *= -1

	def _check_autos_top(self):
		"""Check if any autos have reached the top of the screen."""
		screen_rect = self.screen.get_rect()
		for auto in self.autos.sprites():
			if auto.rect.top <= screen_rect.top:
				# Treat this the same as if the pigeon got hit.
				self._pigeon_hit()
				break

	def _update_screen(self):
		"""Update the images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.pigeon.blitme()
		for dropping in self.droppings.sprites():
			dropping.draw_dropping()
		self.autos.draw(self.screen)

		# Draw the score information.
		self.sb.show_score()

		# Draw the play button if the game is inactive.
		if not self.stats.game_active:
			self.play_button.draw_button()

		# Make the most recently drawn screen visible.
		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance, and run the game.
	pd = PigeonDrop()
	pd.run_game()
