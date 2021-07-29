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
    def __init__(self, params):
        pg.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(params[0])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=params[1])


class Walls:
    def __init__(self, lev=0):
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
    #     if pg.sprite.spritecollideany()


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(random.randint(100, 500), random.randint(100, 500)))


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Block, self).__init__()
        self.image = pygame.image.load('snake.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )


class Snake:
    def __init__(self):
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
                exit()
        sc.fill((255, 255, 255))
        level.draw()
        snake.move(dxy[0], dxy[1])
        snake.draw()
        sc.blit(food.image, food.rect)
        HEAD = pygame.sprite.Group()
        HEAD.add(snake.body[-1])
        if pygame.sprite.spritecollideany(food, level.walls_group):
            food.kill()
            food = Food()
        if pygame.sprite.spritecollideany(food, HEAD):
            snake.len += 1
            food.kill()
            score += 1
            food = Food()
        if pygame.sprite.spritecollideany(snake.body[-1], level.walls_group):
            ending(score)
        Your_score(score)
        pygame.display.update()
        clock.tick(60)


def menu():
    while True:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            game_loop(1)
        if keys[pygame.K_2]:
            game_loop(2)
        if keys[pygame.K_s]:
            game_loop(1, 1)
        sc.fill((255, 255, 255))
        font = pygame.font.SysFont('lev', 50)
        txt = font.render('Choose the level', True, (0, 0, 0))
        sc.blit(txt, (50, 50))
        txt2 = font.render('press 1 to choose 1st level, 2 to 2nd level', True, (0, 0, 0))
        txt3 = font.render('press s to load the saved game', True, (0, 0, 0))
        sc.blit(txt2, (100, 100))
        sc.blit(txt3, (200, 200))
        pygame.display.update()


menu()
