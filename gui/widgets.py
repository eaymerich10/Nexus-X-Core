from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

class FancyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Permitir pasar color y background_color personalizados
        self.background_normal = ''
        self.background_color = kwargs.get('background_color', (0, 0, 0, 1))
        self.color = kwargs.get('color', (0.3, 0.8, 1, 1))
        self.font_size = kwargs.get('font_size', 14)
        self.border = (0, 0, 0, 0)
        self.hover = False

        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])

        self.bind(pos=self.update_graphics, size=self.update_graphics)

        # Bind hover events
        self.bind(on_touch_move=self.on_hover, on_touch_up=self.on_leave)

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_hover(self, instance, touch):
        if self.collide_point(*touch.pos):
            if not self.hover:
                self.hover = True
                self.color = (1, 1, 1, 1)  # blanco al pasar el mouse
                with self.canvas.before:
                    Color(0.2, 0.2, 0.2, 1)  # gris más claro en hover
                    self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        else:
            self.on_leave(instance, touch)

    def on_leave(self, instance, touch):
        if self.hover:
            self.hover = False
            with self.canvas.before:
                Color(*self.background_color)
                self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
            # Restaurar color original
            self.color = (0.3, 0.8, 1, 1) if self.text != "Apagar" else (1, 0, 0, 1)
