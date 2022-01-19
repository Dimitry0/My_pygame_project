import pygame

# from pygame.locals import *

pygame.init()


clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('nazvanie ne pridumal')

# размер одного блока(клетки)
tile_size = 25


gameover = 0

bg_img = pygame.image.load('img/bg_shroom.png')
bush = pygame.image.load('img/bush.png')


class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load('img/p1_stand.png')
            img_right = pygame.transform.scale(img_right, (17.5, 27.5))
            # задаем изображение которое будет выводиться при ходьбе налево
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost_dead.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (20, 30))
        self.climb_image = pygame.image.load('img/alienGreen_climb1.png')
        self.climb_image = pygame.transform.scale(self.climb_image, (17.5, 27.5))

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        # направление
        self.direction = 0

    def update(self, gameover):
        dx = 0
        dy = 0

        # скорость ходьбы
        walk = 3

        if gameover == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.vel_y == 0:
                # задаем высоту прыжка
                self.vel_y = -11
                self.jumped = True
            if not key[pygame.K_SPACE] and self.vel_y == 0:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 3
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # типа анимация:
            if self.counter > walk:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # гравитация:
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            for tile in world.tile_list:

                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            if pygame.sprite.spritecollide(self, snail_group, False):
                gameover = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                gameover = -1
            if pygame.sprite.spritecollide(self, ladder_group, False):
                self.jumped = False
                self.vel_y = 0
                self.direction = 0
                dy = 0
                key = pygame.key.get_pressed()
                if key[pygame.K_UP]:
                    dy = -5
                if key[pygame.K_DOWN]:
                    dy = 5
                self.image = self.climb_image


            self.rect.x += dx
            self.rect.y += dy

        elif gameover == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # вывод изображения игрока на экран
        screen.blit(self.image, self.rect)

        return gameover



class World:
    def __init__(self, world_data):
        self.tile_list = []
        self.i_list = []
        # загрузка изображений
        dirt_img = pygame.image.load('img/grassCenter.png')
        grass_img = pygame.image.load('img/grassMid.png')
        grassCliffRight = pygame.image.load('img/grassCliffRight.png')
        grassCliffLeft = pygame.image.load('img/grassCliffLeft.png')
        grassHillRight = pygame.image.load('img/grassHillRight.png')
        grassHalf = pygame.image.load('img/grassHalf.png')
        grassHalfLeft = pygame.image.load('img/grassHalfLeft.png')
        grassHalfMid = pygame.image.load('img/grassHalfMid.png')
        grassHalfRight = pygame.image.load('img/grassHalfRight.png')
        dirtCaveUR = pygame.image.load('img/dirtCaveUR.png')
        dirtCaveUL = pygame.image.load('img/dirtCaveUL.png').convert_alpha()

        row_count = 0
        for row in world_data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))

                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 78:
                    img = pygame.transform.scale(dirtCaveUL, (tile_size, tile_size))

                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 77:
                    img = pygame.transform.scale(dirtCaveUR, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 76:
                    img = pygame.transform.scale(grassHalfRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 75:
                    img = pygame.transform.scale(grassHalfMid, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 74:
                    img = pygame.transform.scale(grassHalfLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 73:
                    img = pygame.transform.scale(grassHalf, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 72:
                    img = pygame.transform.scale(grassHillRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 71:
                    img = pygame.transform.scale(grassCliffRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 70:
                    img = pygame.transform.scale(grassCliffLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    snail = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    snail_group.add(snail)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 9:
                    ladder = Ladder(col_count * tile_size, row_count * tile_size)
                    ladder_group.add(ladder)
                if tile == 7:
                    door = Door_Mid(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)
                if tile == 8:
                    door = Door_Top(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)
                col_count += 1
            for i in row:
                if i == 51:
                    img = pygame.transform.scale(bush, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.i_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        for i in self.i_list:
            screen.blit(i[0], i[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        pygame.sprite.Sprite.__init__(self)
        self.imageLEFT = pygame.image.load('img/snailWalk1.png')
        self.imageRIGHT = pygame.transform.scale(self.imageLEFT, (27.5, 13))
        self.imageRIGHT = pygame.transform.flip(self.imageLEFT, True, False)
        self.images_right.append(self.imageRIGHT)
        self.images_left.append(self.imageLEFT)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.direction
        self.move_counter += 1
        if abs(self.move_counter) > 25:
            self.direction *= -1
            self.move_counter *= -1
        if self.direction == 1:
            self.image = self.images_right[self.index]
            self.image = pygame.transform.scale(self.image, (27.5, 13))
        if self.direction == -1:
            self.image = self.images_left[self.index]
            self.image = pygame.transform.scale(self.image, (27.5, 13))


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/ladder_mid.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door_Mid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door_openMid.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door_Top(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door_openTop.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 1.6))
        # img_right = pygame.transform.scale(img_right, (17.5, 27.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1],
    [1, 0, 9, 70, 2, 2, 6, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 71, 0, 0, 74, 76, 0, 0, 0, 0, 75, 0, 70, 2, 2, 2, 2, 2, 1],
    [1, 0, 9, 0, 77, 1, 1, 1, 1, 1, 1, 1, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 1, 1, 1, 1, 1],
    [1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 1, 1, 1],
    [1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 1, 1],
    [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 1],
    [1, 1, 1, 2, 71, 0, 0, 73, 0, 74, 76, 0, 0, 70, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 74, 76, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 77, 71, 0, 0, 74, 76, 0, 0, 73, 0, 0, 0, 0, 0, 0, 70, 2, 71, 9, 0, 1],
    [1, 1, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 1],
    [1, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 73, 0, 73, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 74, 76, 0, 0, 73, 0, 0, 2, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 73, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130)

snail_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
world = World(world_data)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))

    world.draw()

    if gameover == 0:
        snail_group.update()

    snail_group.draw(screen)
    lava_group.draw(screen)
    ladder_group.draw(screen)
    door_group.draw(screen)

    gameover = player.update(gameover)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
