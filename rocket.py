import pygame
import os
import time
import random
# Инициализация Pygame
pygame.init()

# Установка дисплея
width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DinoGame")
# Загрузка изображений ракеты

rocket_images = [pygame.image.load(os.path.join("data", "angara_1.png")),
                 pygame.image.load(os.path.join("data", "angara_2.png")),
                 pygame.image.load(os.path.join("data", "angara_3.png"))]

# Установка начального изображения ракеты и позиции
rocket_img = rocket_images[0]
rocket_x = width // 2 - rocket_img.get_width() // 2
rocket_y = height // 2 - rocket_img.get_height() // 2

buster_image = [pygame.image.load(os.path.join("data", "angara_bostersep_left.png")), ]

buster_img = buster_image[0]
buster_x = width // 2 - buster_img.get_width() // 2
buster_y = height // 2 - buster_img.get_height() // 2

buster_image_right = [pygame.image.load(os.path.join("data", "angara_bostersep_right.png")), ]

buster_img_right = buster_image_right[0]
buster_x_right = width // 2 - buster_img_right.get_width() // 2
buster_y_right = height // 2 - buster_img_right.get_height() // 2

stage_image = [pygame.image.load(os.path.join("data", "angara_stage_sep.png")), ]

stage_img = stage_image[0]
stage_x = width // 2 - stage_img.get_width() // 2
stage_y = height // 2 - stage_img.get_height() // 2


# Настройка часов
clock = pygame.time.Clock()

# Настройка переменных для анимации
animation_time = 0.02
last_time = 0
buster_angle_yaw = 0
stage_angle_variable = 0
buster_angle_yaw_right = 0
flag_buster = False
flag_stage = False
buster_angle_variable = 0
buster_angle_variable_right = 0
angle_rocket_checklist = list()
check_end = False
color_value = 255
color_text_value = 0

# Настройка переменных для вращения
angle_yaw = 0  # Начальный угол
font = pygame.font.SysFont(None, 36)

# Настройка переменных для скорости и цвета фона
velocity = 0  # Начальная скорость
background_color = (255, 255, 255)  # white color

# Воспроизведение музыки на фоне
pygame.mixer.music.load(os.path.join("data_sound", "music.mp3")) #music of misha lexperience
pygame.mixer.music.play(1)

# Основной цикл
running = True
music_playing = True  # Добавляем флаг для отслеживания воспроизведения музыки
buster_offset = 0  # Начальное смещение бустера
stage_offset = 0  # Начальное смещение ступени
buster_offset_right = 0  # Начальное смещение правого бустера
while running:

    if color_value > 0:
        color_value -= 0.075
    background_color = (color_value, color_value, color_value)

    if color_value < 142:
        color_text_value = 255

    win.fill(background_color)
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление изображения ракеты каждые 0.5 секунды
    if time.time() - last_time > animation_time:
        if 3 <= velocity < 4.8:
            rocket_img = random.choice([pygame.image.load(os.path.join("data", "angara_sep_1.png")),
                                        pygame.image.load(os.path.join("data", "angara_sep_2.png")),
                                        pygame.image.load(os.path.join("data", "angara_sep_3.png"))])
            flag_buster = True
        elif 4.8 < velocity:
            rocket_img = random.choice([pygame.image.load(os.path.join("data", "angara_three_stage_1.png")),
                                        pygame.image.load(os.path.join("data", "angara_three_stage_2.png")),
                                        pygame.image.load(os.path.join("data", "angara_three_stage_3.png"))])

            flag_stage = True
        else:
            rocket_img = random.choice(rocket_images)
        if velocity > 3.6:
            flag_buster = False
        if velocity > 5.4:
            flag_stage = False
        last_time = time.time()

    # Отображение изображения ракеты с вращением
    rotated_rocket = pygame.transform.rotate(rocket_img, angle_yaw)
    rocket_rect = rotated_rocket.get_rect(
        center=(rocket_x + rocket_img.get_width() // 2, rocket_y + rocket_img.get_height() // 2))
    win.blit(rotated_rocket, rocket_rect.topleft)

    # Отображение угла вверху экрана
    angle_text = font.render(f"Угол: {int(-angle_yaw)} градусов", True, (color_text_value, color_text_value, color_text_value))
    win.blit(angle_text, (10, 10))

    # Отображение скорости в верхнем правом углу
    velocity_text = font.render(f"Скорость: {velocity:.2f}", True, (color_text_value, color_text_value, color_text_value))
    win.blit(velocity_text, (width - velocity_text.get_width() - 10, 10))

    if flag_buster:
        buster_angle_yaw = angle_yaw + buster_angle_variable
        buster_angle_variable += 0.5
        buster_sep = pygame.transform.rotate(buster_img, buster_angle_yaw)
        buster_rect = buster_sep.get_rect(
            center=(buster_x + buster_img.get_width() // 2, buster_y + buster_img.get_height() // 2))
        win.blit(buster_sep, buster_rect.topleft)

        buster_angle_yaw_right = angle_yaw + buster_angle_variable_right
        buster_angle_variable_right -= 0.5
        buster_sep_right = pygame.transform.rotate(buster_img_right, buster_angle_yaw_right)
        buster_rect_right = buster_sep_right.get_rect(
            center=(
                buster_x_right + buster_img_right.get_width() // 2,
                buster_y_right + buster_img_right.get_height() // 2))
        win.blit(buster_sep_right, buster_rect_right.topleft)


        if buster_y < height:
            buster_y += 1  # Движение бустера вниз
        if buster_y_right < height:
            buster_y_right += 1  # Движение правого бустера вниз

        # Плавный отлет бустера и правого бустера в противоположные стороны
        if buster_x > 0:
            buster_x -= 1.7  # Движение бустера влево
            buster_offset += 1  # Увеличение смещения бустера
        if buster_x_right < width - buster_img_right.get_width():
            buster_x_right += 0.7  # Движение правого бустера вправо
            buster_offset_right += 0  # Увеличение смещения правого бустера
    if flag_stage:
        stage_angle_yaw = angle_yaw + stage_angle_variable
        stage_angle_variable += 0.2
        stage_sep = pygame.transform.rotate(stage_img,stage_angle_yaw)
        stage_rect = stage_sep.get_rect(
            center=(stage_x + stage_img.get_width() // 2, stage_y + stage_img.get_height() // 2))
        win.blit(stage_sep, stage_rect.topleft)
        if stage_y < height:
            stage_y += 1
        if stage_x > 0:
            stage_x -= 1  # Движение бустера влево
            stage_offset += 1  # Увеличение смещения бустера
    # Обновление дисплея
    if 0 < velocity < 1:
        angle_text = font.render(f"Требуемый угол: {0} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == 0 and len(angle_rocket_checklist) == 0:
            angle_rocket_checklist.append("checkmark_1")

    if 1 < velocity < 2:
        angle_text = font.render(f"Требуемый угол: {15} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -15 and len(angle_rocket_checklist) == 1:
            angle_rocket_checklist.append("checkmark_2")

    if 2 < velocity < 3:
        angle_text = font.render(f"Требуемый угол: {30} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -30 and len(angle_rocket_checklist) == 2:
            angle_rocket_checklist.append("checkmark_3")

    if 3 < velocity < 4:
        angle_text = font.render(f"Требуемый угол: {45} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -45 and len(angle_rocket_checklist) == 3:
            angle_rocket_checklist.append("checkmark_4")

    if 4 < velocity < 5:
        angle_text = font.render(f"Требуемый угол: {60} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -60 and len(angle_rocket_checklist) == 4:
            angle_rocket_checklist.append("checkmark_5")

    if 5 < velocity < 6:
        angle_text = font.render(f"Требуемый угол: {75} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -75 and len(angle_rocket_checklist) == 5:
            angle_rocket_checklist.append("checkmark_6")

    if 6 < velocity < 7:
        angle_text = font.render(f"Требуемый угол: {80} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -80 and len(angle_rocket_checklist) == 6:
            angle_rocket_checklist.append("checkmark_7")

    if 7 < velocity < 8:
        angle_text = font.render(f"Требуемый угол: {85} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -85 and len(angle_rocket_checklist) == 7:
            angle_rocket_checklist.append("checkmark_8")

    if 8 < velocity < 11:
        angle_text = font.render(f"Требуемый угол: {90} градусов", True, (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -90 and len(angle_rocket_checklist) == 8:
            angle_rocket_checklist.append("checkmark_9")
    if check_end:
        if len(angle_rocket_checklist) == 9:
            angle_text = font.render(f"Ракета вышла на целевую орбиту!", True, (0, 255, 0))
            win.blit(angle_text, (250, 10))
        else:
            angle_text = font.render(f"Ракета не вышла на целевую орбиту!", True, (255, 0, 0))
            win.blit(angle_text, (235, 10))

    pygame.display.update()

    # Проверка, закончилась ли музыка
    if not pygame.mixer.music.get_busy() and music_playing:
        pygame.mixer.music.stop()  # Остановить воспроизведение музыки
        music_playing = False  # Установить флаг в False, чтобы не пытаться остановить музыку снова

    # Управление вращением ракеты
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if angle_yaw < 90:
            angle_yaw += 0.15
    if keys[pygame.K_d]:
        if angle_yaw > -90:
            angle_yaw -= 0.15

    # Обновление скорости с ускорением
    if velocity < 11:
        velocity += 0.002

    if velocity > 10.99: # проверка на скорость
        check_end = True


    clock.tick(60)

pygame.quit()