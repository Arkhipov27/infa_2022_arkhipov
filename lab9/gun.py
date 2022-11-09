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
        self.live = 30
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

    def hit_test(self, obj):
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


class Gun:
    def __init__(self, screen):
        '''
        Конструктор класса Gun

        Args:
            screen: экран
        '''
        self.screen = screen
        self.f_power = 50
        self.f_on = 0
        self.an = 1
        self.color = GREY

    def fire_start(self, event):
        '''
        Подготовка к выстрелу (происходит при нажатии кнопки мыши)

        Args:
            event: событие, связанное с мышью
        '''
        self.f_on = 1
        self.power_up()

    def fire_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f_power * math.cos(self.an)
        new_ball.vy = self.f_power * math.sin(self.an)
        balls.append(new_ball)
        self.f_on = 0
        self.f_power = 50

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and event.pos[0] != 20:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        '''Рисует пушку'''
        rect(screen, self.color, (5, 465, 40, 20))
        rect(screen, self.color, (25, 460, 10, 5))
        rect(screen, self.color, (20, 450, 30, 10))

    def power_up(self):
        '''Увеличение силы пушки'''
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, max_speed=10):
        '''
        Конструктор класса Target

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
        """Попадание шарика в цель."""
        self.points += points
        circle(screen, WHITE, (self.x, self.y), self.r)

    def draw(self):
        '''Рисует мишень'''
        circle(screen, RED, (self.x, self.y), self.r)

    def motion(self):
        '''Описывает движение мишени'''
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x >= 780:
            self.speed_x -= np.abs(2 * self.speed_x)
        if self.y >= 550:
            self.speed_y -= np.abs(2 * self.speed_y)
        if self.x <= 600:
            self.speed_x += np.abs(2 * self.speed_x)
        if self.y <= 300:
            self.speed_y += np.abs(2 * self.speed_y)

    def get_points(self):
        '''
        Доступ к переменной points

        Returns:
            self.points: количество попаданий
        '''
        return self.points


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print('Количество снарядов', len(balls))
            print('Количество попаданий', target1.get_points() + target2.get_points())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    target1.motion()
    target2.motion()
    for b in balls:
        b.move()
        if b.hit_test(target1):
            target1.hit()
            target1.new_target()
        if b.hit_test(target2):
            target2.hit()
            target2.new_target()
    gun.power_up()

pygame.quit()
