import sys
from pathlib import Path
import pygame

# 1. Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Управление персонажем в Pygame")

# Задаем частоту кадров (FPS)
clock = pygame.time.Clock()
FPS = 60

# Цвета
BG_COLOR = (30, 30, 40)

# 2. Определение пути к файлы относительного расположения скрипта
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "character.png"

# Загрузка картинки персонажа
try:
    # Загружаем изображение
    player_image = pygame.image.load(IMAGE_PATH).convert_alpha()

    # Изменяем размер картинки (50x50 пикселей)
    player_image = pygame.transform.scale(player_image, (50, 50))
except Exception as e:
    print(f"Не удалось загрузить картинку: {e}")
    print(f"Убедитесь, что файл 'character.png' находится в папке: {BASE_DIR}")
    pygame.quit()
    sys.exit()

# Получаем размеры спрайта для позиционирования и коллизий
player_rect = player_image.get_rect()
# Ставим персонажа по центру экрана
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Скорость движения персонажа (пикселей за кадр)
player_speed = 5

# 3. Главный игровой цикл
while True:
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

    # Ограничение движения в пределах экрана
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT

    # Отрисовка
    screen.fill(BG_COLOR)
    screen.blit(player_image, player_rect)
    pygame.display.flip()

    # Ограничиваем FPS
    clock.tick(FPS)