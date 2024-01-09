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

bennu_image = [pygame.image.load(os.path.join("data", "bennu.png")), ]

bennu_img = bennu_image[0]
bennu_x = 800
bennu_y = 800

dino_image = [pygame.image.load(os.path.join("data", "dino_rip.png")), ]

dino_img = dino_image[0]
dino_x = 450
dino_y = 250

# Настройка часов
clock = pygame.time.Clock()

# Настройка переменных
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
rocket_scale = 1.0
moon_button_visible = True
asteroid_button_visible = True
angle_text_visible = True
velocity_text_visible = True
check_text_visible = True
rocket_visible = True
moon_next = False
asteroid_next = False
flag_time = True
flag_time_2 = True
seconds_2 = 0
red_asteroid = 0
blue_asteroid = 255
red_moon = 0
blue_moon = 255
angle_switch = True
engine_button_visible = True
red_engine = 0
blue_engine = 255
engine_ignition = False
asteroid_velocity_text_visible = True
asteroid_velocity = 1
flag_impulse = False
approach_asteroid = False
flag_hz_chto_eto = False
impact_visible = True
flag_time_impact = True
flag_back = True
asteroid_visible = True

# Настройка переменных для вращения
angle_yaw = 0  # Начальный угол
font = pygame.font.SysFont(None, 36)

# Настройка переменных для скорости и цвета фона
velocity = 0  # Начальная скорость
background_color = (255, 255, 255)  # white color

# Воспроизведение музыки на фоне
pygame.mixer.music.load(os.path.join("data_sound", "music.mp3"))  # music of misha lexperience
pygame.mixer.music.play(1)

# Основной цикл
running = True
music_playing = True  # Добавляем флаг для отслеживания воспроизведения музыки
buster_offset = 0  # Начальное смещение бустера
stage_offset = 0  # Начальное смещение ступени
buster_offset_right = 0  # Начальное смещение правого бустера
bennu_offset = 0  # Начальное смещение астероида
while running:

    if color_value > 0 and asteroid_visible:
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
        elif ((4.8 < velocity) and check_end == False) or engine_ignition:
            rocket_img = random.choice([pygame.image.load(os.path.join("data", "angara_three_stage_1.png")),
                                        pygame.image.load(os.path.join("data", "angara_three_stage_2.png")),
                                        pygame.image.load(os.path.join("data", "angara_three_stage_3.png"))])

            flag_stage = True
        elif not rocket_visible:
            rocket_img = pygame.image.load(os.path.join("data", "angara.png"))
        elif check_end and len(angle_rocket_checklist) != 9:
            if rocket_scale > 0:  # Пока размер больше нуля
                rocket_img = pygame.image.load(os.path.join("data", "angara_three_stage.png"))
                rocket_scale -= 0.01  # Уменьшаем размер спрайта на каждой итерации
                rocket_img = pygame.transform.scale(rocket_img, (
                    int(rocket_img.get_width() * rocket_scale), int(rocket_img.get_height() * rocket_scale)))
            else:
                rocket_img = pygame.image.load(os.path.join("data", "angara.png"))
        elif (check_end and len(angle_rocket_checklist) == 9) and not engine_ignition:
            rocket_img = pygame.image.load(os.path.join("data", "angara_three_stage.png"))
        elif velocity < 3:
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
    if angle_text_visible:
        # Отображение угла вверху экрана
        angle_text = font.render(f"Угол: {int(-angle_yaw)} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (10, 10))
    if velocity_text_visible:
        # Отображение скорости в верхнем правом углу
        velocity_text = font.render(f"Скорость: {velocity:.2f}", True,
                                    (color_text_value, color_text_value, color_text_value))
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
        stage_sep = pygame.transform.rotate(stage_img, stage_angle_yaw)
        stage_rect = stage_sep.get_rect(
            center=(stage_x + stage_img.get_width() // 2, stage_y + stage_img.get_height() // 2))
        win.blit(stage_sep, stage_rect.topleft)
        if stage_y < height:
            stage_y += 1
        if stage_x > 0:
            stage_x -= 1  # Движение бустера влево
            stage_offset += 1  # Увеличение смещения бустера
    if 0 < velocity < 1:
        angle_text = font.render(f"Требуемый угол: {0} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == 0 and len(angle_rocket_checklist) == 0:
            angle_rocket_checklist.append("checkmark_1")

    if 1 < velocity < 2:
        angle_text = font.render(f"Требуемый угол: {15} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -15 and len(angle_rocket_checklist) == 1:
            angle_rocket_checklist.append("checkmark_2")

    if 2 < velocity < 3:
        angle_text = font.render(f"Требуемый угол: {30} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -30 and len(angle_rocket_checklist) == 2:
            angle_rocket_checklist.append("checkmark_3")

    if 3 < velocity < 4:
        angle_text = font.render(f"Требуемый угол: {45} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -45 and len(angle_rocket_checklist) == 3:
            angle_rocket_checklist.append("checkmark_4")

    if 4 < velocity < 5:
        angle_text = font.render(f"Требуемый угол: {60} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -60 and len(angle_rocket_checklist) == 4:
            angle_rocket_checklist.append("checkmark_5")

    if 5 < velocity < 6:
        angle_text = font.render(f"Требуемый угол: {75} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -75 and len(angle_rocket_checklist) == 5:
            angle_rocket_checklist.append("checkmark_6")

    if 6 < velocity < 7:
        angle_text = font.render(f"Требуемый угол: {80} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -80 and len(angle_rocket_checklist) == 6:
            angle_rocket_checklist.append("checkmark_7")

    if 7 < velocity < 8:
        angle_text = font.render(f"Требуемый угол: {85} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -85 and len(angle_rocket_checklist) == 7:
            angle_rocket_checklist.append("checkmark_8")

    if 8 < velocity < 11:
        angle_text = font.render(f"Требуемый угол: {90} градусов", True,
                                 (color_text_value, color_text_value, color_text_value))
        win.blit(angle_text, (275, 10))
        if int(angle_yaw) == -90 and len(angle_rocket_checklist) == 8:
            angle_rocket_checklist.append("checkmark_9")
    if check_end:
        if len(angle_rocket_checklist) == 9:
            if check_text_visible:
                angle_text = font.render(f"Ракета вышла на целевую орбиту!", True, (0, 255, 0))
                win.blit(angle_text, (250, 10))
            if moon_button_visible:
                # Создание кнопки "Эвакуироваться на луну"
                moon_button = pygame.Rect(245, 150, 410, 50)  # Создание прямоугольника для кнопки
                pygame.draw.rect(win, (red_moon, 0, blue_moon), moon_button)  # Отрисовка кнопки
                font = pygame.font.SysFont(None, 36)
                moon_text = font.render("Эвакуироваться на луну", True, (255, 255, 255))  # Создание текста кнопки
                win.blit(moon_text, (300, 160))  # Отображение текста кнопки

            if asteroid_button_visible:
                # Создание кнопки "Изменить траекторию астероида"
                asteroid_button = pygame.Rect(245, 300, 410, 50)  # Создание прямоугольника для кнопки
                pygame.draw.rect(win, (red_asteroid, 0, blue_asteroid), asteroid_button)  # Отрисовка кнопки
                asteroid_text = font.render("Изменить траекторию астероида", True,
                                            (255, 255, 255))  # Создание текста кнопки
                win.blit(asteroid_text, (255, 310))  # Отображение текста кнопки

            # Обработка нажатий кнопок
            mouse_pos = pygame.mouse.get_pos()
            if moon_button.collidepoint(mouse_pos):
                red_moon = 255
                blue_moon = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    moon_next = True
            else:
                red_moon = 0
                blue_moon = 255

            if asteroid_button.collidepoint(mouse_pos):
                red_asteroid = 255
                blue_asteroid = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    asteroid_next = True
            else:
                red_asteroid = 0
                blue_asteroid = 255

            if moon_next:
                moon_button_visible = False
                asteroid_button_visible = False
                angle_text_visible = False
                check_text_visible = False
                velocity_text_visible = False
                rocket_visible = False
                pass  # луна от Вики

            elif asteroid_next:
                if flag_time:
                    seconds = time.time()
                    flag_time = False
                if time.time() - seconds < 1.5:
                    moon_button_visible = False
                    asteroid_button_visible = False
                    angle_text_visible = False
                    check_text_visible = False
                    velocity_text_visible = False
                    rocket_visible = False
                    skip_text = font.render(f"спустя одну неделю...", True,
                                            (color_text_value, color_text_value, color_text_value))
                    win.blit(skip_text, (295, 240))
                    text_skip_visible = False
                else:
                    if int(angle_yaw) != -145:
                        rocket_visible = True
                        angle_text_visible = True
                        angle_text = font.render(f"Встаньте по  вектору движения(145°)", True, (255, 50, 50))
                        win.blit(angle_text, (425, 10))
                    else:
                        angle_switch = False
                        if engine_button_visible:
                            engine_button = pygame.Rect(50, 150, 800, 50)  # Создание прямоугольника для кнопки
                            pygame.draw.rect(win, (red_engine, 0, blue_engine), engine_button)  # Отрисовка кнопки
                            font = pygame.font.SysFont(None, 36)
                            engine_text = font.render('Нажмите клавишу "i" что бы выдать импульс на ускорение!', True,
                                                      (255, 255, 255))  # Создание текста кнопки
                            win.blit(engine_text, (75, 160))  # Отображение текста кнопки
                            angle_text_visible = False

                        key_ignition = pygame.key.get_pressed()
                        if key_ignition[pygame.K_i]:
                            flag_impulse = True
                            engine_button_visible = False
                            engine_ignition = True

                        if flag_impulse:
                            if asteroid_velocity_text_visible:
                                # Отображение скорости в верхнем правом углу
                                asteroid_velocity_text = font.render(
                                    f"Скорость относительно астероида: {asteroid_velocity:.2f}", True,
                                    (color_text_value, color_text_value, color_text_value))
                                win.blit(asteroid_velocity_text, (width - asteroid_velocity_text.get_width() - 10, 10))
                            if asteroid_velocity > 3:
                                asteroid_velocity_text_visible = False
                                approach_asteroid = True
                                flag_impulse = False
                                engine_ignition = False

                        if approach_asteroid:
                            if flag_time_2:
                                seconds_2 = time.time()
                                flag_time_2 = False
                            if time.time() - seconds_2 < 3:
                                rocket_visible = False
                                skip_text = font.render(f"Столкновение через три... два... один...", True,
                                                        (color_text_value, color_text_value, color_text_value))
                                win.blit(skip_text, (225, 240))
                            else:
                                rocket_visible = True
                                rocket_x = 0
                                rocket_y = 0
                                if asteroid_visible:
                                    bennu = pygame.transform.rotate(bennu_img, 0)
                                    bennu_rect = bennu.get_rect(
                                        center=(
                                        bennu_x + bennu_img.get_width() // 4, bennu_y + bennu_img.get_height() // 4))
                                    win.blit(bennu, bennu_rect.topleft)
                                    bennu_y -= 3
                                    bennu_x -= 3
                                    bennu_offset += 4
                                    if rocket_rect.colliderect(bennu_rect):
                                        if flag_time_impact:
                                            seconds_impact = time.time()
                                            flag_time_impact = False
                                        if time.time() - seconds_impact > 0.8:
                                            asteroid_visible = False
                                else:
                                    dino = pygame.transform.rotate(dino_img, 0)
                                    dino_rect = dino.get_rect(center=(
                                    dino_x + dino_img.get_width() // 4, dino_y + dino_img.get_height() // 4))
                                    win.blit(dino, dino_rect.topleft)
                                    engine_text = font.render('Press "F" to Pay Respects',
                                                              True,
                                                              (255, 255, 255))  # Создание текста кнопки
                                    win.blit(engine_text, (75, 160))  # Отображение текста кнопки
                                    rocket_visible = False
                                    if key_ignition[pygame.K_f]:
                                        quit()
                                    if flag_back:
                                        color_value = 255
                                        flag_back = False
                                    if color_value > 1:
                                        color_value -= 1




        else:
            skip_text = font.render(f"Ракета не вышла на целевую орбиту!", True, (255, 0, 0))
            win.blit(skip_text, (235, 10))
    pygame.display.update()

    # Проверка, закончилась ли музыка
    if not pygame.mixer.music.get_busy() and music_playing:
        pygame.mixer.music.stop()  # Остановить воспроизведение музыки
        music_playing = False  # Установить флаг в False, чтобы не пытаться остановить музыку снова

    # Управление вращением ракеты
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and angle_switch:
        if angle_yaw < 90:
            angle_yaw += 0.15
    if keys[pygame.K_d] and angle_switch:
        if angle_yaw > -145:
            angle_yaw -= 0.15
    if keys[pygame.K_c] and keys[pygame.K_h]:
        velocity = 10.99
        angle_rocket_checklist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        angle_yaw = -90
        color_value = 0

    # Обновление скорости с ускорением
    if velocity < 11:
        velocity += 0.002

    if velocity > 10.99:  # проверка на скорость
        check_end = True

    if flag_impulse:
        asteroid_velocity += 0.001

    clock.tick(60)

pygame.quit()
