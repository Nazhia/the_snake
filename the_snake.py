"""Игра змейка.

Суть игры:
    - Игрок управляет змейкой, которая движется по игровому полю, разделённому
    на клетки.
Цель игры:
    - Увеличивать длину змейки, 'съедая'  яблоки .
Правила игры:
    - Змейка движется в одном из направлений - вверх, вниз, влево или вправо.
    - Игрок управляет направлением движения, но змейка не может остановиться
    или двигаться назад.
    - Каждый раз, когда змейка съедает яблоко, она увеличивается в длину на
    один сегмент.
    - Змейка может проходить сквозь одну стену и появляться с противоположной
    стороны поля.
    - Если змейка столкнётся сама с собой — змейка уменьшится до 1 сегмента
    игра начнется заново.
Реализация игры:
    - Игра реализована с помощью библиотеки { pygame }.
"""
from random import randint

import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета объектов и игрового поля.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс от которого наследуются все игровые объекты."""

    def __init__(self) -> None:
        """Инициализирует новый экземпляр класса {GameObject}."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Базовый метод рисования объектов."""


class Apple(GameObject):
    """Класс описывающий игровой объект Яблоко."""

    def __init__(self, positions: list = []) -> None:
        """Инициализирует экземпляр класса {Apple}."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(positions)

    def draw(self):
        """Рисует объект на экране."""
        positon_on_screen = tuple(pos * GRID_SIZE for pos in self.position)
        rect = pygame.Rect(positon_on_screen, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, positions):
        """Задаёт объекту случайные координаты."""
        while (True):
            position_x = randint(0, (GRID_WIDTH - 1))
            position_y = randint(0, (GRID_HEIGHT - 1))
            random_position = (position_x, position_y)
            if random_position not in positions:
                break

        self.position = random_position


class Snake(GameObject):
    """Класс описывающий игровой объект 'Змейка'."""

    def __init__(self) -> None:
        """Инициализирует экземпляр класса {Snake}."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвигает змейку на одну клетку игрового поля."""
        head_pos_x, head_pos_y = self.get_head_position()
        new_pos_x = (head_pos_x + self.direction[0]) % GRID_WIDTH
        new_pos_y = (head_pos_y + self.direction[1]) % GRID_HEIGHT
        new_head_pos = (new_pos_x, new_pos_y)
        self.last = self.positions[-1]

        self.positions.insert(0, new_head_pos)

        if (len(self.positions) > self.length):
            self.positions.pop(-1)
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[1:]:
            positon_on_screen = tuple(pos * GRID_SIZE for pos in (position))
            rect = (pygame.Rect(positon_on_screen, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        positon_on_scrn = tuple(pos * GRID_SIZE for pos in (self.positions[0]))
        head_rect = pygame.Rect(positon_on_scrn, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            positon_on_scrn = tuple(pos * GRID_SIZE for pos in (self.last))
            last_rect = pygame.Rect(positon_on_scrn, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
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
    """Реализует базовую логику игры и инициализацию всех объектов."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            # заливаем экран
            screen.fill(BOARD_BACKGROUND_COLOR)
            # генерируем случайную позицию для яблока
            apple.randomize_position(snake.positions)
        if (apple.position == snake.get_head_position()):
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
