from random import randint

import pygame as pg

# Константа для часто используемого числа
const = 2

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=(255, 255, 0)):
        """Инициализация объекта."""
        self.position = ((SCREEN_WIDTH // const), (SCREEN_HEIGHT // const))
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Отрисовывает одну заданную ячейку поля."""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экран."""


class Apple(GameObject):
    """Класс игровых объектов - Яблоко."""

    def __init__(self, busy_position=list()):
        """Инициализация яблока на экране."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(busy_position)

    def randomize_position(self, positions):
        """Рандомизация положения яблока на экране."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in positions:
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс игровых объектов - Змейка."""

    def __init__(self):
        """Инициализация начального состояния змейки на экране."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Получение текущих координат головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновление позиции змейки.

        Добавление координат новой головы
        в начало списка и удаление последнего элемента
        если длина змейки не увеличилась.

        """
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        next_move = ((head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
                     (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT)

        length_snake = len(self.positions)
        self.positions.insert(0, next_move)

        if length_snake == self.lenght:
            self.last = self.positions.pop()
        elif length_snake > self.lenght:
            self.last = self.positions.pop()
            self.draw_cell(self.position)
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, direction):
        """Обновление направления движения змейки."""
        self.direction = direction

    def reset(self):
        """Сброс змейки в начальное состояние после столкновения с собой."""
        self.positions = [self.position]
        self.lenght = 1
        self.direction = RIGHT

    def draw(self):
        """Отрисовка змейки."""
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def speed_snake(func):
    """Изменение скорости змейки в зависимости от её длины."""
    global SPEED
    len_snake = len(func.positions)
    if len_snake <= 40:
        SPEED = 10 + len_snake


def handle_keys(game_object):
    """Обработка нажатия клавиш для смены направления движения змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Функция выполнения основного цикла игры."""
    # Инициализация PyGame:
    pg.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()
        speed_snake(snake)
        if (len(snake.positions) > 2
           and snake.get_head_position() in snake.positions[1:]):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
