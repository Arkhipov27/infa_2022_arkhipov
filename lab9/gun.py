import math
import numpy as np
import pygame
from pygame.draw import *

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[np.random.randint(1, len(GAME_COLORS))]
        self.t = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.t += 1
        self.x += self.vx
        self.y += self.vy + 9.8 * self.t
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def draw(self):
        '''Рисует снаряд'''
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def hit_test1(self, obj):
        """Функция проверяет, сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

    def hit_test2(self, obj):
        """Функция проверяет, сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (obj.length / 2 + self.r) ** 2:
            return True
        else:
            return False


class Square:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса Square

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.length = 20
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[np.random.randint(1, len(GAME_COLORS))]
        self.t = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.t += 1
        self.x += self.vx
        self.y += self.vy + 9.8 * self.t
        rect(self.screen, self.color, (self.x - self.length // 2, self.y - self.length // 2,
                                       self.length, self.length))

    def draw(self):
        '''Рисует снаряд'''
        rect(self.screen, self.color, (self.x - self.length // 2, self.y - self.length // 2,
                                       self.length, self.length))

    def hit_test1(self, obj):
        """Функция проверяет, сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.length / 2 + obj.r) ** 2:
            return True
        else:
            return False

    def hit_test2(self, obj):
        """Функция проверяет, сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= self.length ** 2 / 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen, x, speed):
        '''
        Конструктор класса Gun

        Args:
            screen: экран
            x: начальное положение пушки
        '''
        self.screen = screen
        self.f_power = 50
        self.f_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.coord = x
        self.speed = speed

    def fire_start(self, event):
        '''
        Подготовка к выстрелу (происходит при нажатии кнопки мыши)

        Args:
            event: событие, связанное с мышью
        '''
        self.f_on = 1
        self.power_up()

    def fire1_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen, x=self.coord+35)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f_power * math.cos(self.an)
        new_ball.vy = self.f_power * math.sin(self.an)
        balls.append(new_ball)
        self.f_on = 0
        self.f_power = 50

    def fire3_end(self, event):
        """Выстрел квадратом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global squares
        new_square = Square(self.screen, x=self.coord+35)
        new_square.length += 5
        self.an = math.atan2((event.pos[1] - new_square.y), (event.pos[0] - new_square.x))
        new_square.vx = self.f_power * math.cos(self.an)
        new_square.vy = self.f_power * math.sin(self.an)
        squares.append(new_square)
        self.f_on = 0
        self.f_power = 50

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and event.pos[0] != 20:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        '''Рисует пушку'''
        rect(screen, self.color, (self.x, 465, 40, 20))
        rect(screen, self.color, (self.x + 20, 460, 10, 5))
        rect(screen, self.color, (self.x + 15, 450, 30, 10))

    def power_up(self):
        '''Увеличение силы пушки'''
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
            self.color = RED
        else:
            self.color = GREY

    def motion(self):
        '''Описывает движение пушки'''
        self.x += self.speed
        if self.x >= self.coord + 50:
            self.speed -= np.abs(2 * self.speed)
        if self.x <= self.coord:
            self.speed += np.abs(2 * self.speed)


class Target1:
    def __init__(self, max_speed=10):
        '''
        Конструктор класса Target1

        Args:
            max_speed: максимальная скорость мишени
        '''
        self.points = 0
        self.x = np.random.randint(600, 780)
        self.y = np.random.randint(300, 550)
        self.r = np.random.randint(2, 50)
        self.max_speed = max_speed
        self.speed_x = np.random.randint(-self.max_speed, self.max_speed)
        self.speed_y = np.random.randint(-self.max_speed, self.max_speed)

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = np.random.randint(600, 780)
        self.y = np.random.randint(300, 550)
        self.r = np.random.randint(2, 50)
        circle(screen, RED, (self.x, self.y), self.r)
        self.speed_x = np.random.randint(-self.max_speed, self.max_speed)
        self.speed_y = np.random.randint(-self.max_speed, self.max_speed)

    def hit(self, points=1):
        """Попадание снаряда в цель."""
        self.points += points
        circle(screen, WHITE, (self.x, self.y), self.r)

    def draw(self):
        '''Рисует мишень'''
        circle(screen, RED, (self.x, self.y), self.r)

    def motion(self):
        '''Описывает движение мишени'''
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.r >= 780:
            self.speed_x -= np.abs(2 * self.speed_x)
        if self.y + self.r >= 550:
            self.speed_y -= np.abs(2 * self.speed_y)
        if self.x - self.r <= 600:
            self.speed_x += np.abs(2 * self.speed_x)
        if self.y - self.r <= 300:
            self.speed_y += np.abs(2 * self.speed_y)

    def get_points(self):
        '''
        Доступ к переменной points

        Returns:
            self.points: количество попаданий
        '''
        return self.points


class Target2:
    def __init__(self, max_speed=10):
        '''
        Конструктор класса Target2

        Args:
            max_speed: максимальная скорость мишени
        '''
        self.points = 0
        self.x = np.random.randint(600, 780)
        self.y = np.random.randint(300, 550)
        self.length = np.random.randint(2, 50)
        self.max_speed = max_speed
        self.speed_x = np.random.randint(-self.max_speed, self.max_speed)
        self.speed_y = np.random.randint(-self.max_speed, self.max_speed)

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = np.random.randint(600, 780)
        self.y = np.random.randint(300, 550)
        self.length = np.random.randint(2, 50)
        rect(screen, RED, (self.x - self.length // 2, self.y - self.length // 2,
                           self.length, self.length))
        self.speed_x = np.random.randint(-self.max_speed, self.max_speed)
        self.speed_y = np.random.randint(-self.max_speed, self.max_speed)

    def hit(self, points=1):
        """Попадание снаряда в цель."""
        self.points += points
        rect(screen, WHITE, (self.x - self.length // 2, self.y - self.length // 2,
                             self.length, self.length))

    def draw(self):
        '''Рисует мишень'''
        rect(screen, RED, (self.x - self.length // 2, self.y - self.length // 2,
                           self.length, self.length))

    def motion(self):
        '''Описывает движение мишени'''
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x + self.length / 2 >= 780:
            self.speed_x -= 2 * np.abs(self.speed_x)
        if self.y + self.length / 2 >= 550:
            self.speed_y -= 4 * np.abs(self.speed_y)
        if self.x - self.length / 2 <= 600:
            self.speed_x += 2 * np.abs(self.speed_x)
        if self.y - self.length / 2 <= 300:
            self.speed_y += 4 * np.abs(self.speed_y)

        if self.speed_x > 10:
            self.speed_x = 10
        if self.speed_y > 10:
            self.speed_y = 10

    def get_points(self):
        '''
        Доступ к переменной points

        Returns:
            self.points: количество попаданий
        '''
        return self.points


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
balls = []
squares = []
a = 0

clock = pygame.time.Clock()
gun1 = Gun(screen, 5, 3)
gun2 = Gun(screen, 150, 2)
target1 = Target1()
target2 = Target1()

target_sq1 = Target2()
target_sq2 = Target2()
finished = False

while not finished:
    screen.fill(WHITE)
    gun1.draw()
    gun2.draw()
    target1.draw()
    target2.draw()
    target_sq1.draw()
    target_sq2.draw()
    for b in balls:
        b.draw()
    for s in squares:
        s.draw()
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print('Количество снарядов', len(balls) + len(squares))
            print('Количество попаданий', target1.get_points() + target2.get_points() +
                  target_sq1.get_points() + target_sq2.get_points())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                a = 0
            if event.key == pygame.K_RIGHT:
                a = 1

        if a == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun1.fire_start(event)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gun1.fire1_end(event)
                elif event.button == 3:
                    gun1.fire3_end(event)
            if event.type == pygame.MOUSEMOTION:
                gun1.targetting(event)

        if a == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun2.fire_start(event)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gun2.fire1_end(event)
                elif event.button == 3:
                    gun2.fire3_end(event)
            if event.type == pygame.MOUSEMOTION:
                gun2.targetting(event)

    gun1.motion()
    gun2.motion()
    target1.motion()
    target2.motion()
    target_sq1.motion()
    target_sq2.motion()
    for b in balls:
        b.move()
        if b.hit_test1(target1):
            target1.hit()
            target1.new_target()
        if b.hit_test1(target2):
            target2.hit()
            target2.new_target()
        if b.hit_test2(target_sq1):
            target_sq1.hit()
            target_sq1.new_target()
        if b.hit_test2(target_sq2):
            target_sq2.hit()
            target_sq2.new_target()
    for s in squares:
        s.move()
        if s.hit_test1(target1):
            target1.hit()
            target1.new_target()
        if s.hit_test1(target2):
            target2.hit()
            target2.new_target()
        if s.hit_test2(target_sq1):
            target_sq1.hit()
            target_sq1.new_target()
        if s.hit_test2(target_sq2):
            target_sq2.hit()
            target_sq2.new_target()
    gun1.power_up()
    gun2.power_up()

pygame.quit()
