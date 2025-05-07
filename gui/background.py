from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
import random

class ParticleBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self.num_particles = 50

        with self.canvas:
            for _ in range(self.num_particles):
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
                size = random.uniform(2, 5)
                color = Color(0.3, 0.8, 1, 0.5)
                ellipse = Ellipse(pos=(x, y), size=(size, size))
                self.particles.append((ellipse, size, color))

        Clock.schedule_interval(self.update_particles, 1 / 30)

    def update_particles(self, dt):
        for ellipse, size, color in self.particles:
            x, y = ellipse.pos
            y += 0.5
            if y > self.height:
                y = 0
                x = random.uniform(0, self.width)
            ellipse.pos = (x, y)
