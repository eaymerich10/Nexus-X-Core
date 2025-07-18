from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import sys

from .config import FONT_PATH, THEMES
from .popups import show_command_popup, confirm_shutdown
from .themes import switch_theme
from .animations import animate_cursor, fade_in, update_particles
from .widgets import FancyButton

class NexusGUI(BoxLayout):
    def __init__(self, input_method="text", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Fondo de partículas dibujado directamente
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_graphics, pos=self.update_graphics)

        # Inicializa partículas
        self.particles = []
        for _ in range(100):
            self.particles.append({
                'x': self.width * 0.5,
                'y': self.height * 0.5,
                'dx': (0.5 - __import__('random').random()) * 2,
                'dy': (0.5 - __import__('random').random()) * 2,
                'size': 5
            })
        Clock.schedule_interval(lambda dt: update_particles(self), 1 / 30.)

        self.chat_log = ""
        self.status = "Esperando..."
        self.current_theme = "azul"

        self.build_top_bar()
        self.build_chat_area()
        if input_method == "text":
            self.build_input_field()
        self.build_bottom_bar()

        Clock.schedule_interval(lambda dt: animate_cursor(self, dt), 0.5)
        Clock.schedule_interval(self.update_time, 1)

    def update_graphics(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def build_top_bar(self):
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.05))
        self.system_label = Label(
            text="NEXUS-X SYSTEM", font_size=16, font_name=FONT_PATH,
            color=THEMES[self.current_theme], halign='left', valign='middle'
        )
        self.system_label.bind(size=self.system_label.setter('text_size'))

        self.time_label = Label(
            text=self.get_current_time(), font_size=16, font_name=FONT_PATH,
            color=THEMES[self.current_theme], halign='right', valign='middle'
        )
        self.time_label.bind(size=self.time_label.setter('text_size'))

        top_bar.add_widget(self.system_label)
        top_bar.add_widget(self.time_label)
        self.add_widget(top_bar)

    def build_chat_area(self):
        self.chat_area = TextInput(
            text=self.chat_log, readonly=True, font_size=16, font_name=FONT_PATH,
            foreground_color=THEMES[self.current_theme], background_color=(0, 0, 0, 0.6),
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

    def build_bottom_bar(self):
        bottom_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        cmd_btn = FancyButton(text="Comandos")
        cmd_btn.bind(on_release=lambda x: show_command_popup(self))

        theme_btn = FancyButton(text="Tema")
        theme_btn.bind(on_release=lambda x: switch_theme(self))

        self.status_label = Label(
            text=f"Estado: {self.status}",
            font_size=14, font_name=FONT_PATH,
            color=(0.4, 1, 0.4, 1),
            halign='center', valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))

        shutdown_btn = FancyButton(text="Apagar")
        shutdown_btn.color = (1, 0.4, 0.4, 1)
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
        fade_in(self.chat_area)

    def set_status(self, new_status):
        self.status = new_status
        self.status_label.text = f"Estado: {self.status}"
        if "Esperando" in new_status or "activado" in new_status:
            self.status_label.color = (0.4, 1, 0.4, 1)
        elif "Detenido" in new_status:
            self.status_label.color = (1, 0.4, 0.4, 1)
        else:
            self.status_label.color = (1, 1, 1, 1)

    def on_enter_pressed(self, instance):
        from gui import process_user_input_callback
        user_input = instance.text.strip()
        if user_input and process_user_input_callback:
            instance.text = ""
            process_user_input_callback(user_input)

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
