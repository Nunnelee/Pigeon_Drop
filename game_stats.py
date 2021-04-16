class GameStats:
	"""Track the statistics for Pigeon Drop."""

	def __init__(self, pd_game):
		"""Initialize statistics."""
		self.settings = pd_game.settings
		self.reset_stats()
		# Start Pigeon Drop in an inactive state.
		self.game_active = False

		# High score should never be reset.
		self.high_score = 0

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.pigeons_left = self.settings.pigeons_limit
		self.score = 0