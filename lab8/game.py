import numpy as np
import pygame
from pygame.draw import *

pygame.init()
pygame.font.init()


class Game:
    '''
    Класс, создающий мячик и обрабатывающий клики мышки
    '''

    def __init__(self, screen_color, color_1, color_2, color_3, color_4, color_5, color_6, fps, screen_width,
                 screen_height, min_radius, max_radius, max_speed, max_ball, frequency, min_length, max_length):
        '''
        Конструктор класса Ball
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
        min_radius: минимальный радиус мячика
        max_radius: максимальный радиус мячика
        max_speed: максимальная скорость мячика
        max_ball: максимальое количество мячиков на экране
        frequency: частота смены мячиков
        length: длина стороны квадрата
        '''
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))  # экран
        self.x = 0
        self.y = 0
        self.r = 0
        self.square_x = 0
        self.square_y = 0
        self.COLORS = [color_1, color_2, color_3, color_4, color_5, color_6]
        self.color = self.COLORS[np.random.randint(0, 5)]
        self.square_color = self.COLORS[np.random.randint(0, 5)]
        self.FPS = fps
        self.finished = False
        self.click_amount = 0  # количество попыток
        self.get_amount = 0  # количество попаданий по мячикам
        self.attempt_amount = 0  # количество кликов
        self.square_amount = 0  # количество попаданий по квадратам
        self.score = 0  # общий счет
        self.clock = pygame.time.Clock()
        self.screen_color = screen_color
        self.frequency = frequency
        self.min_length = min_length
        self.max_length = max_length
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.max_speed = max_speed
        self.max_ball = max_ball
        self.speed = []  # скорость мячика
        self.square_speed = []
        self.coord_list = []  # список координат для функции создания мячика
        self.square_list = []  # список координат для функции создания квадрата
        self.font = pygame.font.SysFont('Arial', 30)  # шрифт для вывода количества попаданий
        pygame.display.update()

    def new_ball(self, ball_amount):
        '''
        Создает новые мячики
        ball_amount: количество мячиков
        '''
        for k in range(ball_amount):
            self.x = np.random.randint(100, self.screen_width - 100)
            self.y = np.random.randint(100, self.screen_height - 100)
            self.r = np.random.randint(self.min_radius, self.max_radius)
            self.color = self.COLORS[np.random.randint(0, 5)]
            circle(self.screen, self.color, (self.x, self.y), self.r)
            self.coord_list.append([self.x, self.y, self.r, self.color])

    def wall_reflection(self, j):
        '''
        Описывает отражение мячиков от стен
        '''
        self.coord_list[j][0] += self.speed[j][0]
        self.coord_list[j][1] += self.speed[j][1]
        if self.coord_list[j][0] + self.coord_list[j][2] >= self.screen_width:
            self.speed[j][0] -= np.abs(2 * self.speed[j][0])
        if self.coord_list[j][1] + self.coord_list[j][2] >= self.screen_height:
            self.speed[j][1] -= np.abs(2 * self.speed[j][1])
        if self.coord_list[j][0] - self.coord_list[j][2] <= 0:
            self.speed[j][0] += np.abs(2 * self.speed[j][0])
        if self.coord_list[j][1] - self.coord_list[j][2] <= 0:
            self.speed[j][1] += np.abs(2 * self.speed[j][1])

    def square_reflection(self, j):
        self.square_list[j][0] += self.square_speed[j][0] * np.abs(np.sin(self.square_list[j][0]))
        self.square_list[j][1] += self.square_speed[j][1] * np.abs(np.sin(self.square_list[j][1]))
        if self.square_list[j][0] + self.square_list[j][3] >= self.screen_width:
            self.square_speed[j][0] -= np.abs(2 * self.square_speed[j][0])
        if self.square_list[j][1] + self.square_list[j][3] >= self.screen_height:
            self.square_speed[j][1] -= np.abs(2 * self.square_speed[j][1])
        if self.square_list[j][0] - self.square_list[j][3] <= 0:
            self.square_speed[j][0] += np.abs(2 * self.square_speed[j][0])
        if self.square_list[j][1] - self.square_list[j][3] <= 0:
            self.square_speed[j][1] += np.abs(2 * self.square_speed[j][1])

    def new_square(self, ball_amount):
        '''
        Создает новые квадраты
        ball_amount: количество квадратов
        '''
        length = np.random.randint(self.min_length, self.max_length)
        for k in range(ball_amount):
            self.square_x = np.random.randint(100, self.screen_width - 100)
            self.square_y = np.random.randint(100, self.screen_height - 100)
            self.square_color = self.COLORS[np.random.randint(0, 5)]
            rect(self.screen, self.color, (self.square_x - length // 2, self.square_y - length // 2,
                                           length, length))
            self.square_list.append([self.square_x, self.square_y, self.square_color, length])

    def click(self):
        '''
        Обрабатывает клики мышки
        '''
        while not self.finished:
            text = self.font.render('{}'.format(self.score), True, (255, 255, 255))
            self.speed = []
            self.coord_list = []
            self.new_ball(np.random.randint(1, self.max_ball))
            for j in range(len(self.coord_list)):
                self.speed.append([np.random.randint(-self.max_speed, self.max_speed),
                                   np.random.randint(-self.max_speed, self.max_speed)])
            self.square_speed = []
            self.square_list = []
            self.new_square(np.random.randint(1, self.max_ball))
            for j in range(len(self.square_list)):
                self.square_speed.append([np.random.randint(-self.max_speed//5, self.max_speed//5),
                                          np.random.randint(-self.max_speed, self.max_speed)])
            self.attempt_amount += 1
            for i in range(self.FPS // self.frequency):
                self.clock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.finished = True
                        print('Количество попыток: ', self.attempt_amount)
                        print('Количество кликов: ', self.click_amount)
                        print('Количество попаданий в мячики: ', self.get_amount)
                        print('Количество попаданий в квадраты: ', self.square_amount)
                        print('Количество очков: ', self.score)
                        if self.click_amount == 0:
                            print('Счет: 0.0')
                        else:
                            print('Cчет: ', self.score**3 / (self.attempt_amount * self.click_amount))
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_amount += 1
                        for j in range(len(self.coord_list)):
                            if (self.coord_list[j][0] - pygame.mouse.get_pos()[0]) ** 2 \
                                    + (self.coord_list[j][1] - pygame.mouse.get_pos()[1]) ** 2 \
                                    <= self.coord_list[j][2] ** 2:
                                self.score += 1
                                self.get_amount += 1
                                print('Goal!')
                        for t in range(len(self.square_list)):
                            if (self.square_list[t][0] - self.square_list[t][3] <= pygame.mouse.get_pos()[0]) and \
                               (self.square_list[t][0] + self.square_list[t][3] >= pygame.mouse.get_pos()[0]) and \
                                    (self.square_list[t][1] - self.square_list[t][3] <= pygame.mouse.get_pos()[1]) and \
                                    (self.square_list[t][1] + self.square_list[t][3] >= pygame.mouse.get_pos()[1]):
                                self.score += 3
                                self.square_amount += 1
                                print('Goal!')
                for j in range(len(self.coord_list)):
                    self.wall_reflection(j)
                    circle(self.screen, self.coord_list[j][3], (self.coord_list[j][0], self.coord_list[j][1]),
                           self.coord_list[j][2])
                for j in range(len(self.square_list)):
                    self.square_reflection(j)
                    rect(self.screen, self.square_list[j][2],
                         (self.square_list[j][0] - self.square_list[j][3] // 2,
                          self.square_list[j][1] - self.square_list[j][3] // 2,
                          self.square_list[j][3], self.square_list[j][3]))
                pygame.display.update()
                self.screen.fill(self.screen_color)
                self.screen.blit(text, (0, 0))


def main():
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    BLACK = (0, 0, 0)
    game = Game(BLACK, RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, 60, 1200, 800, 10, 100, 20, 5, 1, 20, 50)
    game.click()


if __name__ == '__main__':
    main()
pygame.quit()
