import pygame
import os
import random
from pyvidplayer import Video
import sys

pygame.init()

HEIGHT = 500
WIDTH = 900
FPS = 90
running = True
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Динозаврик')
ICON = pygame.image.load(os.path.join("data/Icon and font", "icon.png"))
pygame.display.set_icon(ICON)
RUNNING = [pygame.image.load("data/Dino/DinoRun1.png"),
           pygame.image.load("data/Dino/DinoRun2.png")]
JUMPING = pygame.image.load("data/Dino/DinoJump.png")
DUCKING = [pygame.image.load("data/Dino/DinoDuck1.png"),
           pygame.image.load("data/Dino/DinoDuck2.png")]
DEATH = pygame.image.load("data/Dino/DinoDead.png")
SMALL_CACTUS = [pygame.image.load("data/Cactus/SmallCactus1.png"),
                pygame.image.load("data/Cactus/SmallCactus2.png"),
                pygame.image.load("data/Cactus/SmallCactus3.png")]
BIG_CACTUS = [pygame.image.load("data/Cactus/LargeCactus1.png"),
              pygame.image.load("data/Cactus/LargeCactus2.png"),
              pygame.image.load("data/Cactus/LargeCactus3.png")]
BIRD = [pygame.image.load("data/Bird/Bird1.png"),
        pygame.image.load("data/Bird/Bird2.png")]
CLOUD = pygame.image.load("data/Other/Cloud.png")
ROAD = pygame.image.load("data/Other/Track.png")
ROCKET = pygame.image.load("data/angara_1.png")
music_jump = pygame.mixer.Sound("music/jump.mp3")
music_hundred = pygame.mixer.Sound("music/hundredpoints.mp3")
music_dead = pygame.mixer.Sound("music/dead.mp3")
background_music = pygame.mixer.Sound("music/backgroundmusic.mp3")

while running:
    class Dinosaur:
        X_POS = 80
        Y_POS = 305
        Y_POS_DUCK = 340
        JUMP_VEL = 8.5

        def __init__(self):
            self.duck_img = DUCKING
            self.run_img = RUNNING
            self.jump_img = JUMPING

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

            self.step_index = 0
            self.jump_vel = self.JUMP_VEL
            self.image = self.run_img[0]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS

        def update(self, userInput):
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index >= 10:
                self.step_index = 0

            if (userInput[pygame.K_UP] or userInput[pygame.K_w]) and not self.dino_jump:
                music_jump.play()
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

        def duck(self):
            self.image = self.duck_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.step_index += 1

        def run(self):
            self.image = self.run_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS
            self.step_index += 1

        def jump(self):
            self.image = self.jump_img
            if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
            if self.jump_vel < - self.JUMP_VEL:
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


    class Rocket:
        def __init__(self):
            self.image = ROCKET
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.y = 135

        def update(self):
            self.rect.x -= game_speed

        def draw(self, SCREEN):
            SCREEN.blit(self.image, self.rect)


    class Cloud:
        def __init__(self):
            self.x = WIDTH + random.randint(300, 500)
            self.y = random.randint(50, 300)
            self.image = CLOUD
            self.width = self.image.get_width()

        def update(self):
            self.x -= game_speed
            if self.x < -self.width:
                self.x = WIDTH + random.randint(300, 500)
                self.y = random.randint(50, 300)

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.x, self.y))


    class Obstacle:
        def __init__(self, image, type):
            self.image = image
            self.type = type
            self.rect = self.image[self.type].get_rect()
            self.rect.x = WIDTH

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], self.rect)


    class SmallCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 325


    class LargeCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 300


    class Bird(Obstacle):
        def __init__(self, image):
            self.type = 0
            super().__init__(image, self.type)
            self.rect.y = 250
            self.index = 0

        def draw(self, SCREEN):
            if self.index >= 9:
                self.index = 0
            SCREEN.blit(self.image[self.index // 5], self.rect)
            self.index += 1


    def main():
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles, count_points
        run = True
        clock = pygame.time.Clock()
        player = Dinosaur()
        rocket = Rocket()
        cloud = Cloud()
        background_music.play(-1)
        game_speed = 15
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        count_points = 0
        font = pygame.font.Font("data/Icon and font/EpilepsySans.ttf", 30)
        obstacles = []
        death_count = 0

        def score():
            global points, game_speed, count_points
            count_points += 1
            if count_points % 2 == 0:
                points += 1
            if points % 100 == 0 and points != 0:
                music_hundred.play()
                game_speed += 0.5
            text = font.render("Очки: " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (780, 40)
            SCREEN.blit(text, textRect)

        def background():
            global x_pos_bg, y_pos_bg
            image_width = ROAD.get_width()
            SCREEN.blit(ROAD, (x_pos_bg, y_pos_bg))
            SCREEN.blit(ROAD, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(ROAD, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            SCREEN.fill((255, 255, 255))
            pygame.draw.rect(SCREEN, (252, 221, 118), pygame.Rect(0, 390, 900, 150))
            userInput = pygame.key.get_pressed()

            player.draw(SCREEN)
            player.update(userInput)
            cloud.draw(SCREEN)
            cloud.update()

            if points < 100:
                if len(obstacles) == 0:
                    if random.randint(0, 2) == 0:
                        obstacles.append(SmallCactus(SMALL_CACTUS))
                    elif random.randint(0, 2) == 1:
                        obstacles.append(LargeCactus(BIG_CACTUS))
                    elif random.randint(0, 2) == 2:
                        obstacles.append(Bird(BIRD))
            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    background_music.stop()
                    music_dead.play()
                    pygame.time.delay(100)
                    death_count += 1
                    menu(death_count)

            if points >= 120:
                rocket.draw(SCREEN)
                rocket.update()
                if player.dino_rect.colliderect(rocket.rect):
                    background_music.stop()
                    pygame.time.delay(150)
                    vid = Video("data/Prehistory.mp4")
                    vid.set_size((900, 500))
                    while True:
                        vid.draw(SCREEN, (0, 0))
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                vid.close()
                                import rocket
                                rocket.win()

            background()

            score()

            clock.tick(30)
            pygame.display.update()


    def get_max_points():
        f = open('data/max_points.txt', 'r')
        point = f.readline().strip()
        f.close()
        return point


    def write_max_points(point):
        f = open('data/max_points.txt', 'w+')
        f.write(str(point))
        f.close()


    write_max_points(0)


    def menu(death_count):
        global points
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font("data/Icon and font/EpilepsySans.ttf", 45)

            if death_count == 0:
                text = font.render("Нажмите на любую кнопку", True, (0, 0, 0))
            elif death_count > 0:
                max_points = get_max_points()
                if not max_points:
                    write_max_points(points)
                    max_points = points
                elif int(max_points) < points:
                    write_max_points(points)
                    max_points = points

                text = font.render("Нажмите на любую кнопку", True, (0, 0, 0))
                score = font.render("Ваш результат: " + str(points), True, (0, 0, 0))
                max_score = font.render('Лучший результат: ' + str(max_points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                max_score_rect = max_score.get_rect()
                scoreRect.center = (WIDTH // 2, HEIGHT // 2 + 10)
                max_score_rect.center = (WIDTH // 2, HEIGHT // 2 + 75)
                SCREEN.blit(score, scoreRect)
                SCREEN.blit(max_score, max_score_rect)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2 - 30)
            SCREEN.blit(text, textRect)
            SCREEN.blit(DEATH, (WIDTH // 2 - 86, HEIGHT // 2 - 131))
            SCREEN.blit(BIG_CACTUS[0], (WIDTH // 2 - 300, HEIGHT // 2 + 153))
            SCREEN.blit(BIG_CACTUS[1], (WIDTH // 2 + 200, HEIGHT // 2 + 153))
            SCREEN.blit(BIG_CACTUS[2], (WIDTH // 2 + 20, HEIGHT // 2 + 153))
            SCREEN.blit(SMALL_CACTUS[0], (WIDTH // 2 - 130, HEIGHT // 2 + 177))
            SCREEN.blit(BIRD[0], (WIDTH // 2 + 200, HEIGHT // 2 - 190))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    main()


    menu(death_count=0)
    clock.tick(FPS)
