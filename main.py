from random import randint
import pygame as pg
import sys
import pickle
import time

import pygame.sprite

pg.init()

pg.time.set_timer(pg.USEREVENT, 3000)

W = 1200
H = 600
WHITE = (255, 255, 255)
CARS = ('car1.png')

ENEMY_SURF = []

sc = pg.display.set_mode((W, H))

for i in range(len(CARS)):
    ENEMY_SURF.append(
        pg.image.load('enemy.png').convert_alpha())
friend_surf = pg.image.load('friend.png').convert_alpha()


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.or_im = surf
        self.rect = self.image.get_rect(
            center=(x, 0))
        self.add(group)
        self.speed = randint(1, 5)
        self.rot = 0
        self.rot_speed = randint(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.or_im, self.rot)

    def update(self):
        self.rotate()
        if self.rect.y < H:
            self.rect.y += self.speed
        else:
            self.kill()


class Friend(pg.sprite.Sprite):
    def __init__(self, x, y, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.or_im = surf
        self.rect = self.image.get_rect(
            center=(y, x))
        self.add(group)
        self.speed = randint(1, 5)
        self.rot = 0
        self.rot_speed = randint(-3, 3)
        self.last_update = pygame.time.get_ticks()
        self.nap = 3

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.or_im, self.rot)

    def update(self):
        self.nap *= (-1)
        self.rect.move_ip((self.nap, 0))

    # self.rotate()


ens = pg.sprite.Group()
friends = pg.sprite.Group()
points = 0


def show_points():
    p = f'{points}'
    point_surf = pygame.font.SysFont('point', 30).render(p, True, (0, 0, 0))
    sc.blit(point_surf, (1170, 10))


class Player(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect(
            center=(600, 590))

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def draw(self):
        sc.blit(self.image, self.rect)


Enemy(randint(1, W),
      ENEMY_SURF[0], ens)

player = Player()
player_group = pg.sprite.Group(player)
player_group.add(player)
max_point_in_game = 0


def lev1():
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)


def lev2():
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)


def lev3():
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)


def lev4():
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)
    Enemy(randint(1, W),
          ENEMY_SURF[0], ens)


level = 1


def ending():
    with open('best.pickle', 'rb') as f:
        best = pickle.load(f)
        nl = r"\n"
    game_over = pg.font.SysFont("game over", 20).render(
        f"GAME OVER! Your score is:{max_point_in_game},Your best score is {best}", True, (0, 0, 0))
    with open('best.pickle', 'wb') as f:
        pickle.dump(max(max_point_in_game, best), f)
    sc.fill((255, 255, 255))
    sc.blit(game_over, (100, 100))
    pg.display.update()
    time.sleep(3)
    pygame.quit()
    exit()


clock = pygame.time.Clock()

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.USEREVENT:
            if level <= 1: lev1()
            if level == 2: lev2()
            if level == 3: lev3()
            if level == 4: lev4()
            Friend(randint(1, W), randint(10, H),
                   friend_surf, friends)
    keys = pygame.key.get_pressed()
    dxy = [0, 0]
    if keys[pygame.K_LEFT]:
        dxy = [-5, 0]
    if keys[pygame.K_RIGHT]:
        dxy = [5, 0]
    if keys[pygame.K_UP]:
        dxy = [0, -5]
    if keys[pygame.K_DOWN]:
        dxy = [0, 5]
    sc.fill(WHITE)
    player.move(dxy[0], dxy[1])
    player.draw()
    ens.draw(sc)
    # for fr in friends:
    #     fr.rotate()
    friends.update()
    friends.draw(sc)
    for enm in ens:
        if pg.sprite.spritecollide(enm, player_group, False):
            ens.remove(enm)
            points -= 1
    if points < 0:
        ending()
    for enm in friends:
        if pg.sprite.spritecollide(enm, player_group, False):
            friends.remove(enm)
            Friend(randint(1, W), randint(10, H),
                   friend_surf, friends)
            points += 1
    max_point_in_game = max(points, max_point_in_game)
    level = min(4, max_point_in_game // 5)
    show_points()
    pg.time.delay(20)
    # print(points)
    ens.update()
    clock.tick(60)
    pg.display.update()
