import pygame
import random

pygame.init()

width = 800
height = 600
cell_size = 20

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

clock = pygame.time.Clock()
fps = 15

class Snake:
    def __init__(self):
        self.x = width // 2
        self.y = height // 2
        self.dx = cell_size
        self.dy = 0
        self.body = [(self.x, self.y)]
        self.direction = "RIGHT"

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.body.insert(0, (self.x, self.y))

    def shrink(self):
        self.body.pop()

    def check_collision(self):
        head = (self.x, self.y)
        return (self.x < 0 or self.x >= width or
                self.y < 0 or self.y >= height or
                head in self.body[1:])

class Food:
    def __init__(self):
        self.x = random.randrange(0, width, cell_size)
        self.y = random.randrange(0, height, cell_size)

    def respawn(self):
        self.x = random.randrange(0, width, cell_size)
        self.y = random.randrange(0, height, cell_size)

snake = Snake()
food = Food()
score = 0
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.dy != cell_size:
                snake.dx = 0
                snake.dy = -cell_size
            elif event.key == pygame.K_DOWN and snake.dy != -cell_size:
                snake.dx = 0
                snake.dy = cell_size
            elif event.key == pygame.K_LEFT and snake.dx != cell_size:
                snake.dx = -cell_size
                snake.dy = 0
            elif event.key == pygame.K_RIGHT and snake.dx != -cell_size:
                snake.dx = cell_size
                snake.dy = 0
            elif event.key == pygame.K_r and game_over:
                snake = Snake()
                food = Food()
                score = 0
                game_over = False

    if not game_over:
        snake.move()

        if snake.check_collision():
            game_over = True

        if snake.x == food.x and snake.y == food.y:
            score += 1
            food.respawn()
        else:
            snake.shrink()

    screen.fill(black)

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render(f"Game Over! Score: {score}", True, white)
        screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to restart", True, white)
        screen.blit(text, (width//2 - text.get_width()//2, height//2 + 30))
    else:
        pygame.draw.rect(screen, red, (food.x, food.y, cell_size, cell_size))
        for segment in snake.body:
            pygame.draw.rect(screen, green, (segment[0], segment[1], cell_size, cell_size))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, white)
        screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()