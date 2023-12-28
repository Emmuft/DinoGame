import pygame
import os
import time
import random
import math

# Инициализация Pygame
pygame.init()

# Установка дисплея
width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moon Dino")

# Загрузка изображений ракеты

rocket_images = [pygame.image.load(os.path.join("data", "angara_1.jpg")),
                 pygame.image.load(os.path.join("data", "angara_2.jpg")),
                 pygame.image.load(os.path.join("data", "angara_3.jpg"))]

# Установка начального изображения ракеты и позиции
rocket_img = rocket_images[0]
rocket_x = width // 2 - rocket_img.get_width() // 2
rocket_y = height // 2 - rocket_img.get_height() // 2

buster_image = [pygame.image.load(os.path.join("data", "angara_bostersep_left.jpg")), ]

buster_img = buster_image[0]
buster_x = width // 2 - buster_img.get_width() // 2
buster_y = height // 2 - buster_img.get_height() // 2

buster_image_right = [pygame.image.load(os.path.join("data", "angara_bostersep_right.jpg")), ]

buster_img_right = buster_image_right[0]
buster_x_right = width // 2 - buster_img_right.get_width() // 2
buster_y_right = height // 2 - buster_img_right.get_height() // 2


# Настройка часов
clock = pygame.time.Clock()

# Настройка переменных для анимации
animation_time = 0.02
last_time = 0
buster_angle_yaw = 0
buster_angle_yaw_right = 0
flag_buster = False
buster_angle_variable = 0
buster_angle_variable_right = 0

# Настройка переменных для вращения
angle_yaw = 0  # Начальный угол
font = pygame.font.SysFont(None, 36)

# Настройка переменных для скорости и цвета фона
velocity = 0  # Начальная скорость
background_color = (173, 216, 230)  # светло-голубой цвет

# Воспроизведение музыки на фоне
pygame.mixer.music.load(os.path.join("data_music", "rocket.mp3"))
pygame.mixer.music.play(-1)  # -1 для зацикливания воспроизведения

# Основной цикл
running = True
music_playing = True  # Добавляем флаг для отслеживания воспроизведения музыки
buster_offset = 0  # Начальное смещение бустера
buster_offset_right = 0  # Начальное смещение правого бустера
while running:
    win.fill(background_color)

    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление изображения ракеты каждые 0.5 секунды
    if time.time() - last_time > animation_time:
        if 3 <= velocity < 4.8:
            rocket_img = random.choice([pygame.image.load(os.path.join("data", "angara_sep_1.jpg")),
                                        pygame.image.load(os.path.join("data", "angara_sep_2.jpg")),
                                        pygame.image.load(os.path.join("data", "angara_sep_3.jpg"))])
            flag_buster = True
        elif velocity > 4.8:
            rocket_img = random.choice([pygame.image.load(os.path.join("data", "angara_three_stage_1.jpg")),
                                        pygame.image.load(os.path.join("data", "angara_three_stage_2.jpg")),
                                        pygame.image.load(os.path.join("data", "angara_three_stage_3.jpg"))])
        else:
            rocket_img = random.choice(rocket_images)
        last_time = time.time()

    # Отображение изображения ракеты с вращением
    rotated_rocket = pygame.transform.rotate(rocket_img, angle_yaw)
    rocket_rect = rotated_rocket.get_rect(
        center=(rocket_x + rocket_img.get_width() // 2, rocket_y + rocket_img.get_height() // 2))
    win.blit(rotated_rocket, rocket_rect.topleft)

    # Отображение угла вверху экрана
    angle_text = font.render(f"Угол: {int(-angle_yaw)} градусов", True, (255, 255, 255))
    win.blit(angle_text, (10, 10))

    # Отображение скорости в верхнем правом углу
    velocity_text = font.render(f"Скорость: {velocity:.2f}", True, (255, 255, 255))
    win.blit(velocity_text, (width - velocity_text.get_width() - 10, 10))

    if flag_buster:
        buster_sep = pygame.transform.rotate(buster_img, buster_angle_yaw)
        buster_rect = buster_sep.get_rect(
            center=(buster_x + buster_img.get_width() // 2, buster_y + buster_img.get_height() // 2))
        win.blit(buster_sep, buster_rect.topleft)
        buster_angle_yaw = angle_yaw + buster_angle_variable
        buster_angle_variable += 1

        buster_sep_right = pygame.transform.rotate(buster_img_right, buster_angle_yaw_right)
        buster_rect_right = buster_sep_right.get_rect(
            center=(
                buster_x_right + buster_img_right.get_width() // 2,
                buster_y_right + buster_img_right.get_height() // 2))
        win.blit(buster_sep_right, buster_rect_right.topleft)
        buster_angle_yaw_right = angle_yaw + buster_angle_variable_right
        buster_angle_variable_right -= 1

        if buster_y < height:
            buster_y += 1  # Движение бустера вниз
        if buster_y_right < height:
            buster_y_right += 1  # Движение правого бустера вниз

        # Плавный отлет бустера и правого бустера в противоположные стороны
        if buster_x > 0:
            buster_x -= 1  # Движение бустера влево
            buster_offset += 1  # Увеличение смещения бустера
        if buster_x_right < width - buster_img_right.get_width():
            buster_x_right += 1  # Движение правого бустера вправо
            buster_offset_right += 1  # Увеличение смещения правого бустера
    # Обновление дисплея
    pygame.display.update()

    # Проверка, закончилась ли музыка
    if not pygame.mixer.music.get_busy() and music_playing:
        pygame.mixer.music.stop()  # Остановить воспроизведение музыки
        music_playing = False  # Установить флаг в False, чтобы не пытаться остановить музыку снова

    # Управление вращением ракеты
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        angle_yaw += 0.15
    if keys[pygame.K_d]:
        angle_yaw -= 0.15

    # Обновление скорости с ускорением
    if velocity < 11:
        velocity += 0.002

    clock.tick(60)

pygame.quit()
