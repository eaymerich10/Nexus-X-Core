from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty


class FancyButton(Button):
    base_color = ListProperty([0.1, 0.1, 0.1, 1])  # fondo normal
    hover_color = ListProperty([0.2, 0.2, 0.2, 1])  # fondo al pasar el ratón
    text_color = ListProperty([0.3, 0.8, 1, 1])  # color del texto normal
    text_hover_color = ListProperty([1, 1, 1, 1])  # texto al pasar el ratón

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # desactiva fondo default
        self.color = self.text_color
        self.font_size = 16
        self.border = (0, 0, 0, 0)
        self.hover = False

        with self.canvas.before:
            Color(*self.base_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(base_color=self.update_graphics)

        # Eventos de hover
        self.bind(on_touch_move=self.on_hover, on_touch_up=self.on_leave)

    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.base_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

    def on_hover(self, instance, touch):
        if self.collide_point(*touch.pos):
            if not self.hover:
                self.hover = True
                self.base_color = self.hover_color
                self.color = self.text_hover_color
        else:
            self.on_leave(instance, touch)

    def on_leave(self, instance, touch):
        if self.hover:
            self.hover = False
            self.base_color = [0.1, 0.1, 0.1, 1]
            self.color = self.text_color
