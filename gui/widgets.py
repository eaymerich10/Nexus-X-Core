from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty


class FancyButton(Button):
    base_color = ListProperty([0.1, 0.1, 0.1, 1])          # color fondo normal
    hover_color = ListProperty([0.2, 0.2, 0.2, 1])         # color fondo al pasar
    text_color = ListProperty([0.3, 0.8, 1, 1])           # color texto normal
    text_hover_color = ListProperty([1, 1, 1, 1])         # color texto al pasar
    shadow_color = ListProperty([0, 0, 0, 0.3])           # sombra suave
    border_radius = NumericProperty(15)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # quitar fondo por defecto
        self.color = self.text_color
        self.font_size = 16
        self.border = (0, 0, 0, 0)
        self.hover = False

        with self.canvas.before:
            # Sombra ligera (más difusa, menos marcada)
            Color(*self.shadow_color)
            self.shadow_rect = RoundedRectangle(
                size=(self.size[0] + 8, self.size[1] + 8),
                pos=(self.pos[0] - 4, self.pos[1] - 4),
                radius=[self.border_radius]
            )
            # Botón principal
            Color(*self.base_color)
            self.rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[self.border_radius]
            )

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(base_color=self.update_graphics)

        self.bind(on_touch_move=self.on_hover, on_touch_up=self.on_leave)

    def update_graphics(self, *args):
        self.shadow_rect.pos = (self.pos[0] - 4, self.pos[1] - 4)
        self.shadow_rect.size = (self.size[0] + 8, self.size[1] + 8)
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_hover(self, instance, touch):
        if self.collide_point(*touch.pos):
            if not self.hover:
                self.hover = True
                self.animate_hover_in()
        else:
            self.on_leave(instance, touch)

    def on_leave(self, instance, touch):
        if self.hover:
            self.hover = False
            self.animate_hover_out()

    def animate_hover_in(self):
        Animation.cancel_all(self)
        anim = Animation(d=0.2)
        anim.bind(on_progress=lambda *_: self.apply_hover_style())
        anim.start(self)

    def animate_hover_out(self):
        Animation.cancel_all(self)
        anim = Animation(d=0.2)
        anim.bind(on_progress=lambda *_: self.apply_normal_style())
        anim.start(self)

    def apply_hover_style(self):
        self.base_color = self.hover_color
        self.color = self.text_hover_color

    def apply_normal_style(self):
        self.base_color = [0.1, 0.1, 0.1, 1]
        self.color = self.text_color
