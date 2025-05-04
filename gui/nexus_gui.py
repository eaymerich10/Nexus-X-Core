from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.core.window import Window

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

        # Fondo general
        Window.clearcolor = (0.05, 0.05, 0.05, 1)  # casi negro

        # Área de chat
        self.chat_area = TextInput(
            text=self.chat_log,
            readonly=True,
            font_size=16,
            font_name='/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf',  # usa una fuente monoespaciada
            foreground_color=(0.7, 1, 0.7, 1),  # verde neón suave
            background_color=(0.1, 0.1, 0.1, 1),  # gris oscuro terminal
            size_hint=(1, 0.85),
            padding=[10, 10, 10, 10],
            cursor_blink=False
        )
        self.add_widget(self.chat_area)

        # Barra de estado
        self.status_label = Label(
            text=f"Estado: {self.status}",
            font_size=18,
            font_name='/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf',  # fuente monoespaciada
            color=(0.4, 0.8, 1, 1),  # azul neón
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

    def add_message(self, sender, message):
        self.chat_log += f"{sender}: {message}\n"
        self.chat_area.text = self.chat_log
        self.chat_area.cursor = (0, len(self.chat_area.text))

    def set_status(self, new_status):
        self.status = new_status
        self.status_label.text = f"Estado: {self.status}"

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
