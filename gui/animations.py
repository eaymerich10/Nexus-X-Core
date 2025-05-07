from kivy.animation import Animation
from kivy.graphics import Color, Ellipse
import random

def animate_cursor(gui, dt):
    if hasattr(gui, 'input_field') and gui.input_field.focus:
        gui.input_field.cursor_color = (0.7, 1, 0.7, 1)
    else:
        gui.input_field.cursor_color = (0.5, 0.5, 0.5, 1)

def fade_in(widget):
    anim = Animation(opacity=1, duration=0.5)
    anim.start(widget)

def update_particles(gui):
    gui.canvas.before.clear()
    with gui.canvas.before:
        Color(0.08, 0.08, 0.08, 1)  # fondo oscuro
        gui.bg_rect = gui.bg_rect  # mantiene fondo

        Color(0.3, 0.8, 1, 0.3)  # color azul translúcido

        for particle in gui.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']

            # rebote en los bordes
            if particle['x'] < 0 or particle['x'] > gui.width:
                particle['dx'] *= -1
            if particle['y'] < 0 or particle['y'] > gui.height:
                particle['dy'] *= -1

            Ellipse(pos=(particle['x'], particle['y']), size=(particle['size'], particle['size']))
