import numpy as np
import pygame
from pygame.draw import *
pygame.init()


class Ball:
    '''
    Класс, создающий мячик и обрабатывающий клики мышки
    '''
    def __init__(self, screen_color, color_1, color_2, color_3, color_4, color_5, color_6, fps, screen_width,
                 screen_height, max_speed, frequency):
        '''
        Инициализация класса Ball
        screen_color: цвет экрана
        color_1: первый цвет
        color_2: второй цвет
        color_3: третий цвет
        color_4: четвертый цвет
        color_5: пятый цвет
        color_6: шестой цвет
        fps: количество кадров в секунду
        screen_width: ширина экрана
        screen_height: высота экрана
        max_speed: максимальная скорость мячика
        frequency: частота смены мячиков
        '''
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))  # экран
        self.x = 0
        self.y = 0
        self.r = 0
        self.COLORS = [color_1, color_2, color_3, color_4, color_5, color_6]
        self.color = self.COLORS[np.random.randint(0, 5)]
        self.FPS = fps
        self.finished = False
        self.click_amount = 0  # количество попыток
        self.get_amount = 0  # количество попаданий
        self.attempt_amount = 0  # количество кликов
        self.clock = pygame.time.Clock()
        self.screen_color = screen_color
        self.frequency = frequency
        self.max_speed = max_speed
        self.coord_list = []  # список координат для функции создания мячика

        # параметры (флаги) для отражения от стен
        self.fl1, self.fl2, self.fl3, self.fl4, self.fl5, self.fl6, self.fl7, self.fl8 = 0, 0, 0, 0, 0, 0, 0, 0
        self.f1, self.f2, self.f3, self.f4 = 0, 0, 0, 0
        pygame.display.update()

    def new_ball(self, ball_amount):
        '''
        Создает новый мячик
        ball_amount: количество мячиков
        '''
        for i in range(ball_amount):
            self.x = np.random.randint(100, self.screen_width - 100)
            self.y = np.random.randint(100, self.screen_height - 100)
            self.r = np.random.randint(10, 100)
            self.color = self.COLORS[np.random.randint(0, 5)]
            circle(self.screen, self.color, (self.x, self.y), self.r)
            self.coord_list.append(self.x)
            self.coord_list.append(self.y)
            self.coord_list.append(self.r)

    def wall_reflection(self, speed_x, speed_y):
        '''
        Описывает отражение мячиков от стен
        speed_x: скорость мячика по оси x
        speed_y: скорость мячика по оси y
        '''
        if speed_x > 0 and speed_y > 0:
            if self.x + self.r <= self.screen_width and self.y + self.r <= self.screen_height and self.fl1 == 0:
                self.x += speed_x
                self.y += speed_y
            elif self.x + self.r >= self.screen_width and self.y + self.r <= self.screen_height and self.fl2 == 0:
                self.fl1 = 1
                self.f1 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x + self.r <= self.screen_width and self.y + self.r >= self.screen_height and self.fl2 == 0:
                self.fl1 = 1
                self.f1 = 2
                self.x += speed_x
                self.y -= speed_y
            elif self.x + self.r >= self.screen_width and self.y + self.r >= self.screen_height and self.fl2 == 0:
                self.fl1 = 1
                self.f1 = 3
                self.x -= speed_x
                self.y -= speed_y
            elif self.x + self.r <= self.screen_width and self.y + self.r <= self.screen_height and self.f1 == 1:
                self.fl2 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x + self.r <= self.screen_width and self.y + self.r <= self.screen_height and self.f1 == 2:
                self.fl2 = 1
                self.x += speed_x
                self.y -= speed_y
            elif self.x + self.r <= self.screen_width and self.y + self.r <= self.screen_height and self.f1 == 3:
                self.fl2 = 1
                self.x -= speed_x
                self.y -= speed_y
        if speed_x > 0 and speed_y < 0:
            if self.x + self.r <= self.screen_width and self.y - self.r >= 0 and self.fl3 == 0:
                self.x += speed_x
                self.y += speed_y
            elif self.x + self.r >= self.screen_width and self.y - self.r >= 0 and self.fl4 == 0:
                self.fl3 = 1
                self.f2 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x + self.r <= self.screen_width and self.y - self.r <= 0 and self.fl4 == 0:
                self.fl3 = 1
                self.f2 = 2
                self.x += speed_x
                self.y -= speed_y
            elif self.x + self.r >= self.screen_width and self.y - self.r <= 0 and self.fl4 == 0:
                self.fl3 = 1
                self.f2 = 3
                self.x -= speed_x
                self.y -= speed_y
            elif self.x + self.r <= self.screen_width and self.y - self.r >= 0 and self.f2 == 1:
                self.fl4 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x + self.r <= self.screen_width and self.y - self.r >= 0 and self.f2 == 2:
                self.fl4 = 1
                self.x += speed_x
                self.y -= speed_y
            elif self.x + self.r <= self.screen_width and self.y - self.r >= 0 and self.f2 == 3:
                self.fl4 = 1
                self.x -= speed_x
                self.y -= speed_y
        if speed_x < 0 and speed_y > 0:
            if self.x - self.r >= 0 and self.y + self.r <= self.screen_height and self.fl5 == 0:
                self.x += speed_x
                self.y += speed_y
            elif self.x - self.r <= 0 and self.y + self.r <= self.screen_height and self.fl6 == 0:
                self.fl5 = 1
                self.f3 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x - self.r >= 0 and self.y + self.r >= self.screen_height and self.fl6 == 0:
                self.fl5 = 1
                self.f3 = 2
                self.x += speed_x
                self.y -= speed_y
            elif self.x - self.r <= 0 and self.y + self.r >= self.screen_height and self.fl6 == 0:
                self.fl5 = 1
                self.f3 = 3
                self.x -= speed_x
                self.y -= speed_y
            elif self.x - self.r >= 0 and self.y + self.r <= self.screen_height and self.f3 == 1:
                self.fl6 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x - self.r >= 0 and self.y + self.r <= self.screen_height and self.f3 == 2:
                self.fl6 = 1
                self.x += speed_x
                self.y -= speed_y
            elif self.x - self.r >= 0 and self.y + self.r <= self.screen_height and self.f3 == 3:
                self.fl6 = 1
                self.x -= speed_x
                self.y -= speed_y
        if speed_x < 0 and speed_y < 0:
            if self.x - self.r >= 0 and self.y - self.r >= 0 and self.fl7 == 0:
                self.x += speed_x
                self.y += speed_y
            elif self.x - self.r <= 0 and self.y - self.r >= 0 and self.fl8 == 0:
                self.fl7 = 1
                self.f4 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x - self.r >= 0 and self.y - self.r <= 0 and self.fl8 == 0:
                self.fl7 = 1
                self.f4 = 2
                self.x += speed_x
                self.y -= speed_y
            elif self.x - self.r <= 0 and self.y - self.r <= 0 and self.fl8 == 0:
                self.fl7 = 1
                self.f4 = 3
                self.x -= speed_x
                self.y -= speed_y
            elif self.x - self.r >= 0 and self.y - self.r >= 0 and self.f4 == 1:
                self.fl8 = 1
                self.x -= speed_x
                self.y += speed_y
            elif self.x - self.r >= 0 and self.y - self.r >= 0 and self.f4 == 2:
                self.fl8 = 1
                self.x += speed_x
                self.y -= speed_y
            elif self.x - self.r >= 0 and self.y - self.r >= 0 and self.f4 == 3:
                self.fl8 = 1
                self.x -= speed_x
                self.y -= speed_y
        if self.x + self.r >= self.screen_width or self.y + self.r >= self.screen_height or self.x - self.r <= 0 \
                or self.x - self.r <= 0:
            self.fl1, self.fl2, self.fl3, self.fl4, self.fl5, self.fl6, self.fl7, self.fl8 = 0, 0, 0, 0, 0, 0, 0, 0
            self.f1, self.f2, self.f3, self.f4 = 0, 0, 0, 0

    def click(self):
        '''
        Обрабатывает клики мышки
        '''
        while not self.finished:
            speed_x = np.random.randint(-self.max_speed, self.max_speed)
            speed_y = np.random.randint(-self.max_speed, self.max_speed)
            self.attempt_amount += 1
            self.new_ball(np.random.randint(1, 5))
            for i in range(self.FPS//self.frequency):
                self.clock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.finished = True
                        print('Количество попыток: ', self.attempt_amount)
                        print('Количество кликов: ', self.click_amount)
                        print('Количество попаданий: ', self.get_amount)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_amount += 1
                        if (self.x - pygame.mouse.get_pos()[0]) ** 2 + (self.y - pygame.mouse.get_pos()[1]) ** 2\
                                <= self.r ** 2:
                            self.get_amount += 1
                            print('Goal!')
                self.wall_reflection(speed_x, speed_y)
                circle(self.screen, self.color, (self.x, self.y), self.r)
                pygame.display.update()
                self.screen.fill(self.screen_color)


def main():
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    BLACK = (0, 0, 0)
    ball = Ball(BLACK, RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, 60, 1200, 800, 20, 1)
    ball.click()


if __name__ == '__main__':
    main()
pygame.quit()