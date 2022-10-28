import pygame
from pygame.draw import *
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))
x_center = 200
y_center = 200


def body(color, board_color, radius, board_thickness):
    circle(screen, color, (x_center, y_center), radius)
    circle(screen, board_color, (x_center, y_center), radius, board_thickness)


def mouth(color, distance_from_center, height_from_center, height):
    rect(screen, color, (x_center - distance_from_center, y_center + height_from_center, 2*distance_from_center,
                         height))


def eye(color, pupil_color, board_color, distance_from_center, height_from_center, radius, pupil_radius,
        board_thickness):
    circle(screen, color, (x_center + distance_from_center, y_center - height_from_center), radius)
    circle(screen, board_color, (x_center + distance_from_center, y_center - height_from_center), radius,
           board_thickness)
    circle(screen, pupil_color, (x_center + distance_from_center, y_center - height_from_center), pupil_radius)
    circle(screen, board_color, (x_center + distance_from_center, y_center - height_from_center), pupil_radius,
           board_thickness)


def eyebrow(color, x_start, y_start, x_finish, y_finish, thickness):
    line(screen, color, (x_start, y_start), (x_finish, y_finish), thickness)


def main():
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    body(YELLOW, BLACK, 100, 1)
    mouth(BLACK, 50, 50, 20)
    eye(RED, BLACK, BLACK, -40, 30, 20, 9, 1)
    eye(RED, BLACK, BLACK, 40, 30, 14, 7, 1)
    eyebrow(BLACK, 110, 110, 185, 158, 10)
    eyebrow(BLACK, 220, 156, 300, 130, 10)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True


if __name__ == '__main__':
    main()
pygame.quit()
