from pygame.math import Vector2
import math
from particle import Particle


class JetEngine:

    def __init__(self, space_pos, space_size, space_head, display):
        self._display = display
        self._space_size = space_size

        self._pos = self._update_pos(space_pos, space_head)

        self._particles = []
        self._frequency = 15
        self._started = False

    def _update_pos(self, space_pos, space_head):
        return space_pos - Vector2(0, self._space_size[1] / 2).rotate((space_head + 180) % 360)

    def started(self):
        return self._started

    def start(self):
        self._started = True

    def stop(self):
        self._started = False

    def update(self, space_pos, space_head):
        if self._started:
            pos = self._update_pos(space_pos, space_head)
            if self._pos.distance_to(pos) > self._frequency:
                speed = -1 * Vector2(math.sin(math.radians(space_head)), -math.cos(math.radians(space_head)))
                self._particles.append(Particle(pos, speed, display=self._display))
                self._pos = pos

        for p in self._particles:
            p.update()

            if p.done():
                self._particles.remove(p)

    def draw(self):
        for p in self._particles:
            p.draw(self._display)
