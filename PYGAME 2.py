import random
import sys
from pathlib import Path
import pygame

# 1. Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Управление персонажем, стрельба и враги в Pygame")

# Задаем частоту кадров (FPS)
clock = pygame.time.Clock()
FPS = 60

# Цвета
BG_COLOR = (30, 30, 40)
BULLET_COLOR = (255, 255, 0)      # Желтый цвет для пуль
ENEMY_COLOR = (230, 50, 50)       # Красный цвет для врагов

# 2. Определение пути к файлу относительно расположения скрипта
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "character.png"

# Загрузка картинки персонажа (с защитой, если картинки нет — нарисуем квадрат)
has_image = True
try:
    player_image = pygame.image.load(IMAGE_PATH).convert_alpha()
    player_image = pygame.transform.scale(player_image, (50, 50))
    player_rect = player_image.get_rect()
except Exception as e:
    print(f"Не удалось загрузить картинку: {e}")
    print("Используем временный прямоугольник вместо картинки персонажа.")
    has_image = False
    player_rect = pygame.Rect(0, 0, 50, 50)

# Ставим персонажа по центру экрана
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Скорость движения персонажа (пикселей за кадр)
player_speed = 5

# --- СИСТЕМА СТРЕЛЬБЫ ---
bullets = []
bullet_speed = 10
# Ограничитель частой стрельбы (кулдаун), чтобы пушки не летели сплошным потоком
shoot_delay = 150  # в миллисекундах
last_shot_time = 0

# --- СИСТЕМА РАНДОМНЫХ ОБЪЕКТОВ (ВРАГОВ) ---
enemies = []
num_enemies = 5

for _ in range(num_enemies):
    enemy_rect = pygame.Rect(
        random.randint(50, SCREEN_WIDTH - 50),
        random.randint(50, SCREEN_HEIGHT - 50),
        40, 40
    )
    # Задаем случайную скорость по X и Y для хаотичного движения
    enemy_vel_x = random.choice([-3, -2, 2, 3])
    enemy_vel_y = random.choice([-3, -2, 2, 3])
    enemies.append({"rect": enemy_rect, "vx": enemy_vel_x, "vy": enemy_vel_y})


# 3. Главный игровой цикл
while True:
    current_time = pygame.time.get_ticks()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получение состояния всех нажатых клавиш
    keys = pygame.key.get_pressed()

    # Управление стрелками ИЛИ клавишами WASD
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += player_speed

    # Действие по кнопке: Стрельба на ПРОБЕЛ (SPACE) с учетом кулдауна
    if keys[pygame.K_SPACE]:
        if current_time - last_shot_time > shoot_delay:
            # Создаем пулю по центру персонажа
            bullet_rect = pygame.Rect(
                player_rect.centerx - 4, 
                player_rect.top, 
                8, 16
            )
            bullets.append(bullet_rect)
            last_shot_time = current_time

    # Ограничение движения персонажа в пределах экрана (рамка)
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT

    # --- ОБНОВЛЕНИЕ ПУЛЬ ---
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        # Удаляем пулю, если она улетела за верх экрана
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # --- ОБНОВЛЕНИЕ ХАОТИЧНЫХ ОБЪЕКТОВ (ВРАГОВ) ---
    for enemy in enemies:
        enemy["rect"].x += enemy["vx"]
        enemy["rect"].y += enemy["vy"]

        # Отскок от границ экрана, чтобы они не улетали
        if enemy["rect"].left < 0 or enemy["rect"].right > SCREEN_WIDTH:
            enemy["vx"] *= -1
            # Меняем скорость случайно при ударе о стену для пущего хаоса
            enemy["vx"] += random.choice([-1, 1]) 
        if enemy["rect"].top < 0 or enemy["rect"].bottom > SCREEN_HEIGHT:
            enemy["vy"] *= -1
            enemy["vy"] += random.choice([-1, 1])

        # Проверка столкновения пули с врагом (бонус: уничтожение врага при попадании!)
        for bullet in bullets[:]:
            if bullet.colliderect(enemy["rect"]):
                bullets.remove(bullet)
                # Переносим врага в случайное место при попадании
                enemy["rect"].x = random.randint(50, SCREEN_WIDTH - 50)
                enemy["rect"].y = random.randint(50, SCREEN_HEIGHT - 50)
                enemy["vx"] = random.choice([-3, -2, 2, 3])
                enemy["vy"] = random.choice([-3, -2, 2, 3])

    # --- ОТРИСОВКА ---
    screen.fill(BG_COLOR)

    # Рисуем персонажа
    if has_image:
        screen.blit(player_image, player_rect)
    else:
        pygame.draw.rect(screen, (0, 200, 255), player_rect)

    # Рисуем пули
    for bullet in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, bullet)

    # Рисуем хаотичные объекты (врагов)
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, enemy["rect"], border_radius=8)

    pygame.display.flip()

    # Ограничиваем FPS
    clock.tick(FPS)
