from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# GLOBAL
gui_instance = None

class NexusGUI(BoxLayout):
    chat_log = StringProperty("")
    status = StringProperty("Esperando...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Fondo general oscuro
        Window.clearcolor = (0.03, 0.03, 0.03, 1)

        # Fondo gráfico sólido
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)  # gris oscuro casi negro
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_graphics, pos=self.update_graphics)

        # Área de chat
        self.chat_area = TextInput(
            text=self.chat_log,
            readonly=True,
            font_size=16,
            font_name='/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf',
            foreground_color=(0.4, 1, 0.4, 1),  # verde neón intenso
            background_color=(0, 0, 0, 1),  # negro profundo
            size_hint=(1, 0.85),
            padding=[10, 10, 10, 10],
            cursor_blink=False
        )
        self.add_widget(self.chat_area)

        # Barra de estado con animación simulada
        self.status_label = Label(
            text=f"Estado: {self.status}",
            font_size=18,
            font_name='/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf',
            color=(1, 0.4, 0.4, 1),  # rojo neón
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        # Animación de estado
        Clock.schedule_interval(self.blink_status, 0.5)

    def update_graphics(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def add_message(self, sender, message):
        self.chat_log += f"{sender}: {message}\n"
        self.chat_area.text = self.chat_log
        self.chat_area.cursor = (0, len(self.chat_area.text))

    def set_status(self, new_status):
        self.status = new_status
        self.status_label.text = f"Estado: {self.status}"

    def blink_status(self, dt):
        # Parpadeo sci-fi en la barra de estado
        if self.status_label.color[3] == 1:
            self.status_label.color = (1, 0.4, 0.4, 0.6)
        else:
            self.status_label.color = (1, 0.4, 0.4, 1)

class NexusApp(App):
    def build(self):
        global gui_instance
        gui_instance = NexusGUI()
        return gui_instance

def start_gui():
    app = NexusApp()
    app.run()

def update_gui_chat(sender, message):
    if gui_instance:
        Clock.schedule_once(lambda dt: gui_instance.add_message(sender, message))

def update_gui_status(new_status):
    if gui_instance:
        Clock.schedule_once(lambda dt: gui_instance.set_status(new_status))
