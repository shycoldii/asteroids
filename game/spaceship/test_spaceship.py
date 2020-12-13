import pygame as pg

from game.spaceship.spaceship import Spaceship
from game.score import Score
from game.background import Background
from game.display import Display

WIDTH = 900
HEIGHT = 675
FPS = 60

pg.init()
clock = pg.time.Clock()


# ========== setup ========== #
display = Display(900, 675)
score = Score(display)
spaceship = Spaceship(display)
background = Background(display)
# =========================== #


def on_execute():
    while True:
        background.draw(display)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)

            spaceship.on_event(event)

            if event.type == pg.KEYDOWN:
                score.update()

                if event.key == pg.K_F12:
                    display.toggle_fullscreen()

                if event.key == pg.K_f:
                    spaceship.on_collision()

            if event.type == pg.KEYUP:
                pass

        on_loop()
        on_render()

        pg.display.flip()
        clock.tick(FPS)


def on_loop():
    background.update()
    spaceship.update()


def on_render():
    spaceship.draw()
    score.draw()


if __name__ == '__main__':
    on_execute()
