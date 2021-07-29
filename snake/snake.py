import pygame
import pygame as pg
import sys
import random
import time
import pickle

pygame.init()

W = 800
H = 600

sc = pg.display.set_mode((W, H))
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

yellow = (255, 255, 102)


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    sc.blit(value, [0, 0])


def ending(score):
    game_over = pg.font.SysFont("game over", 50).render(
        "GAME OVER!", True, (0, 0, 0))
    sc.fill((255, 255, 255))
    show_score = pg.font.SysFont('score', 50).render(
        f'Your score is {score}', True, (0, 0, 0)
    )
    sc.blit(game_over, (100, 100))
    sc.blit(show_score, (200, 200))
    pg.display.update()
    time.sleep(3)
    pygame.quit()
    exit()


class Wall(pygame.sprite.Sprite):
    def init(self, params):
        pg.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(params[0])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=params[1])


class Walls:
    def init(self, lev=0):
        self.walls_group = pygame.sprite.Group()
        self.walls_group.add(Wall(((20, 600), (5, 300))))
        self.walls_group.add(Wall(((20, 800), (795, 300))))
        self.walls_group.add(Wall(((800, 20), (400, 5))))
        self.walls_group.add(Wall(((800, 20), (400, 595))))
        if lev == 2:
            self.walls_group.add(Wall(((20, 100), (200, 60))))
            self.walls_group.add(Wall(((20, 100), (400, 540))))
            self.walls_group.add(Wall(((20, 100), (500, 60))))

    def draw(self):
        self.walls_group.draw(sc)

    # def check(self):
    # if pg.sprite.spritecollideany()


class Food(pygame.sprite.Sprite):
    def init(self):
        super(Food, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(random.randint(100, 500), random.randint(100, 500)))


class Block(pygame.sprite.Sprite):
    def init(self, x, y):
        super(Block, self).__init__()
        self.image = pygame.image.load('snake.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )


class Snake:
    def init(self):
        self.body = [Block(50, 50)]
        self.headx = 50
        self.heady = 50
        self.len = 1

    def move(self, dx, dy):
        self.headx += dx
        self.heady += dy
        self.body.append(Block(self.headx, self.heady))
        if len(self.body) > self.len:
            del self.body[0]

    def draw(self):
        for block in self.body:
            sc.blit(block.image, block.rect)


def game_loop(mod, saved=None):
    level = Walls(mod)
    food = Food()
    snake = Snake()
    if saved is not None:
        with open('saved_game.pickle', 'rb') as f:
            arr = pickle.load(f)
            print(arr)
            del snake.body[0]
            for pos in arr:
                snake.body.append(Block(pos[0], pos[1]))

    score = len(snake.body)
    speed = 5
    dxy = [0, 0]
    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and dxy != [speed, 0]:
            dxy = [-speed, 0]
        if keys[pygame.K_RIGHT] and dxy != [-speed, 0]:
            dxy = [speed, 0]
        if keys[pygame.K_UP] and dxy != [0, speed]:
            dxy = [0, -speed]
        if keys[pygame.K_DOWN] and dxy != [0, -speed]:
            dxy = [0, speed]
        if keys[pygame.K_q]:
            with open('saved_game.pickle', 'wb') as f:
                arr = []
                for it in snake.body:
                    arr.append(it.rect.center)
                pickle.dump(arr, f)