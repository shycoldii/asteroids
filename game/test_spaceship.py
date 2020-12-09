import pygame as pg

from spaceship import Spaceship

WIDTH = HEIGHT = 800
FPS = 60

pg.init()
display = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


# ========== setup ========== #
spaceship = Spaceship()
# =========================== #


def on_execute():
    while True:
        display.fill((10, 10, 10))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)

            if event.type == pg.KEYDOWN:
                # if event.key == pg.K_UP:
                spaceship.on_key_press(event.key)

            if event.type == pg.KEYUP:
                spaceship.on_key_release(event.key)

        on_loop()
        on_render()

        pg.display.flip()
        clock.tick(FPS)


def on_loop():
    spaceship.update()


def on_render():
    spaceship.draw(display)


if __name__ == '__main__':
    on_execute()
