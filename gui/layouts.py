from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
import sys

from .config import FONT_PATH, THEMES
from .popups import show_command_popup, confirm_shutdown
from .themes import switch_theme
from .animations import animate_cursor, blink_status
from .widgets import FancyButton

class NexusGUI(BoxLayout):
    def __init__(self, input_method="text", **kwargs):
        super().__init__(**kwargs)
        self.chat_log = ""
        self.status = "Esperando..."
        self.current_theme = "azul"
        self.user_input_callback = None  # ← importante para el callback

        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_graphics, pos=self.update_graphics)

        with self.canvas:
            Color(0.3, 0.8, 1, 1)
            self.top_line = Line(points=[self.x, self.top, self.right, self.top], width=1.2)

        self.build_top_bar()
        self.build_chat_area()
        if input_method == "text":
            self.build_input_field()
        self.build_bottom_bar()

        Clock.schedule_interval(lambda dt: blink_status(self, dt), 0.5)
        Clock.schedule_interval(self.update_time, 1)

    def set_user_input_callback(self, callback):
        self.user_input_callback = callback

    def update_graphics(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.top_line.points = [self.x, self.top, self.right, self.top]

    def build_top_bar(self):
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.05))
        self.system_label = Label(
            text="NEXUS-X SYSTEM", font_size=16, font_name=FONT_PATH,
            color=THEMES[self.current_theme], halign='left', valign='middle'
        )
        self.time_label = Label(
            text=self.get_current_time(), font_size=16, font_name=FONT_PATH,
            color=THEMES[self.current_theme], halign='right', valign='middle'
        )
        top_bar.add_widget(self.system_label)
        top_bar.add_widget(self.time_label)
        self.add_widget(top_bar)

    def build_chat_area(self):
        self.chat_area = TextInput(
            text=self.chat_log, readonly=True, font_size=16, font_name=FONT_PATH,
            foreground_color=THEMES[self.current_theme], background_color=(0, 0, 0, 1),
            size_hint=(1, 0.7), padding=[10, 10, 10, 10], cursor_blink=False
        )
        self.add_widget(self.chat_area)

    def build_input_field(self):
        self.input_field = TextInput(
            hint_text="Escribe tu comando aquí...", multiline=False, font_size=16,
            font_name=FONT_PATH, foreground_color=(0.7, 1, 0.7, 1), background_color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, 0.08), padding=[10, 10, 10, 10], cursor_blink=True
        )
        self.input_field.bind(on_text_validate=self.on_enter_pressed)
        self.add_widget(self.input_field)
        Clock.schedule_interval(lambda dt: animate_cursor(self, dt), 0.5)

    def build_bottom_bar(self):
        bottom_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        cmd_btn = FancyButton(text="Comandos")
        cmd_btn.bind(on_release=lambda x: show_command_popup(self))

        theme_btn = FancyButton(text="Tema")
        theme_btn.bind(on_release=lambda x: switch_theme(self))

        self.status_label = Label(
            text=f"Estado: {self.status}",
            font_size=14,
            font_name=FONT_PATH,
            color=(1, 0.4, 0.4, 1),
            halign='center', valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))

        shutdown_btn = FancyButton(
            text="Apagar",
            color=(1, 0, 0, 1),  # texto rojo fuerte
            background_color=(0, 0, 0, 1)  # fondo negro
        )
        shutdown_btn.bind(on_release=lambda x: confirm_shutdown(self))

        bottom_bar.add_widget(cmd_btn)
        bottom_bar.add_widget(theme_btn)
        bottom_bar.add_widget(self.status_label)
        bottom_bar.add_widget(shutdown_btn)

        self.add_widget(bottom_bar)

    def get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def update_time(self, dt):
        self.time_label.text = self.get_current_time()

    def add_message(self, sender, message):
        self.chat_log += f"{sender}: {message}\n"
        self.chat_area.text = self.chat_log
        self.chat_area.cursor = (0, len(self.chat_area.text))

    def set_status(self, new_status):
        self.status = new_status
        self.status_label.text = f"Estado: {self.status}"
    
    def on_enter_pressed(self, instance):
        user_input = instance.text.strip()
        if user_input and self.user_input_callback:
            instance.text = ""
            self.user_input_callback(user_input)
    
    def start_shutdown_sequence(self, popup):
        popup.dismiss()
        self.disable_interface()
        self.run_countdown(3)

    def disable_interface(self):
        self.chat_area.disabled = True
        if hasattr(self, 'input_field'):
            self.input_field.disabled = True
        self.status_label.text = "Apagando..."

    def run_countdown(self, seconds):
        if seconds > 0:
            self.set_status(f"Apagando en {seconds}...")
            Clock.schedule_once(lambda dt: self.run_countdown(seconds - 1), 1)
        else:
            Clock.schedule_once(lambda dt: sys.exit(), 1)
