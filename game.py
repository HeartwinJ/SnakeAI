import random
import pygame # type: ignore

# Game Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Snake Game')

		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(None, 36)
		self.reset()

	def reset(self):
		self.snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
		self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
		self.food = self.place_food()
		self.score = 0

	def place_food(self):
		while True:
			x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
			y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
			if (x, y) not in self.snake:
				return (x, y)
			
	def get_action(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and self.direction != DOWN:
				return UP
			elif event.key == pygame.K_DOWN and self.direction != UP:
				return DOWN
			elif event.key == pygame.K_LEFT and self.direction != RIGHT:
				return LEFT
			elif event.key == pygame.K_RIGHT and self.direction != LEFT:
				return RIGHT
			
	def step(self, action):
		if action is not None:
			new_direction = action
			if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
				self.direction = new_direction

		head_x, head_y = self.snake[0]
		new_head = (head_x + self.direction[0] * CELL_SIZE, head_y + self.direction[1] * CELL_SIZE)

		if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
			new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
			new_head in self.snake):
			return -10, True

		if new_head == self.food:
			self.snake.insert(0, new_head)
			self.food = self.place_food()
			self.score += 1
			return 5, False
		else:
			self.snake.insert(0, new_head)
			self.snake.pop()
			return 1, False
	
	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				else:
					action = self.get_action(event)

			done = self.post_run(action)
			self.render()
			self.clock.tick(10)
			if done:
				running = False
		
		pygame.quit()
	
	def post_run(self, action):
		_, done = self.step(action)
		return done

	def render(self):
		self.screen.fill(BLACK)
		for (x, y) in self.snake:
			pygame.draw.rect(self.screen, GREEN, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
		pygame.draw.rect(self.screen, RED, pygame.Rect(self.food[0], self.food[1], CELL_SIZE, CELL_SIZE))

		score_text = self.font.render(f'Score: {self.score}', True, WHITE)
		self.screen.blit(score_text, (10, 10))

		pygame.display.flip()

	def get_state(self):
		pass

if __name__ == "__main__":
	game = Game()
	game.run()
	print("Game ended with score: ", game.score)