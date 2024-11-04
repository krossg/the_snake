"""Код проекта - Изгиб питона."""
from random import randint
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Экран объекта."""

    def __init__(self):
        """Инициализация объекта."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экран."""
        pass


class Apple(GameObject):
    """Яблоко."""

    def __init__(self):
        """Инициализация яблока на экране."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Рандомизация положения яблока на экране."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return self.position

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        """Инициализация начального состояния змейки на экране."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position, self.position]
        self.lenght = 1
        self.next_direction = None
        self.direction = RIGHT
        self.last = None
        self.speed = SPEED

    def get_head_position(self):
        """Получение текущих координат головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновление позиции змейки и её скорости.

        Добавление координат новой головы
        в начало списка и удаление последнего элемента
        если длина змейки не увеличилась.

        Скорость меняется с помощью метода, изменяющего скорость
        в зависимости от длины змейки.
        """
        self.speed_snake()
        head_position = self.get_head_position()
        x, y = self.direction
        self.next_move = ((head_position[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                          (head_position[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and self.next_move in self.positions:
            self.reset()
        else:
            self.positions.insert(0, self.next_move)

            if len(self.positions) > self.lenght:
                self.last = self.positions.pop()

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сброс змейки в начальное состояние после столкновения с собой."""
        self.positions = [(self.position), (self.position)]
        self.lenght = 1
        self.next_direction = None
        self.direction = RIGHT
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Отрисовка змейки на экране с затиранием следа."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def speed_snake(self):
        """Изменение скорости змейки в зависимости от её длины."""
        global SPEED
        if len(self.positions) <= 5:
            SPEED = 10
        elif len(self.positions) > 5 and len(self.positions) <= 50:
            SPEED = 20
        else:
            SPEED = 30


def handle_keys(game_object):
    """Обработка нажатия клавиш для смены направления движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция выполнения основного цикла игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        # Тут опишите основную логику игры.
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
