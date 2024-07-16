import game

class Brain(game.Game):
	def get_action(self, event):
		pass
		
	def post_run(self, action):
			reward, done = self.step(action)
			return done

if __name__ == '__main__':
		game = Brain()
		game.run()
		print('Game ended with score: ', game.score)

