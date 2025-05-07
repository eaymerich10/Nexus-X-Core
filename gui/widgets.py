from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

class FancyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = kwargs.get('color', (0.3, 0.8, 1, 1))
        self.font_size = 14  # valor inicial, luego se ajusta dinámicamente
        self.radius = [12]

        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=self.radius)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(size=self.update_font_size)  # nuevo: ajusta el texto al tamaño del botón

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_font_size(self, *args):
        # Ajusta la fuente proporcionalmente al alto del botón, con límites mínimos y máximos
        base_size = self.height * 0.4  # ajusta el factor según lo que te guste visualmente
        self.font_size = max(14, min(base_size, 28))  # mínimo 14, máximo 28 (ajústalo si quieres)
