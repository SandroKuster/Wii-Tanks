import pygame as pg

width, height = 800, 800
screen = pg.display.set_mode((width, height))
run = True
clock = pg.time.Clock()


def draw_window():
    screen.fill((255, 255, 255))

    pg.display.update()


while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    draw_window()
    clock.tick(60)
