import math
from numpy import random
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
        """ Конструктор класса ball

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
        self.color = GAME_COLORS[random.randint(1, len(GAME_COLORS))]
        self.live = 30
        self.t = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.t += 1
        self.x += self.vx
        self.y += self.vy + 9.8 * self.t
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def draw(self):
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def hit_test(self, obj):
        """Функция проверяет, сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f_power = 50
        self.f_on = 0
        self.an = 1
        self.color = GREY

    def fire_start(self, event):
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
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXME don't know how to do it
        circle(screen, self.color, (40, 450), 50)

    def power_up(self):
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # FIXME: don't work!!! How to call this functions when object is created?
    def __init__(self):
        self.points = 0
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        circle(screen, RED, (self.x, self.y), self.r)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        circle(screen, WHITE, (self.x, self.y), self.r)

    def draw(self):
        circle(screen, RED, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print(target.points)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hit_test(target):
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
