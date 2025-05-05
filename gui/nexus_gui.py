# import platform
# import random
# import sys
# from datetime import datetime

# from kivy.app import App
# from kivy.clock import Clock
# from kivy.core.window import Window
# from kivy.graphics import Color, Rectangle, Line
# from kivy.properties import StringProperty
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.popup import Popup
# from kivy.uix.textinput import TextInput

# # GLOBAL
# gui_instance = None
# process_user_input_callback = None  # este será enganchado por core.py

# if platform.machine() == 'x86_64':
#     FONT_PATH = '/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf'
# elif platform.machine() == 'aarch64':
#     FONT_PATH = '/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf'

# class NexusGUI(BoxLayout):
#     chat_log = StringProperty("")
#     status = StringProperty("Esperando...")

#     def __init__(self, input_method="text", **kwargs):
#         super().__init__(**kwargs)
#         self.orientation = 'vertical'
#         self.padding = 20
#         self.spacing = 10

#         Window.clearcolor = (0.03, 0.03, 0.03, 1)

#         with self.canvas.before:
#             Color(0.08, 0.08, 0.08, 1)
#             self.rect = Rectangle(size=self.size, pos=self.pos)
#             self.bind(size=self.update_graphics, pos=self.update_graphics)

#         with self.canvas:
#             Color(0.3, 0.8, 1, 1)
#             self.top_line = Line(points=[self.x, self.top, self.right, self.top], width=1.2)

#         # Define themes
#         self.themes = {
#             "azul": (0.3, 0.8, 1, 1),
#             "verde": (0.4, 1, 0.4, 1),
#             "purpura": (0.8, 0.3, 1, 1),
#             "rojo": (1, 0.4, 0.4, 1)
#         }
#         self.current_theme = "azul"
#         self.apply_theme(self.current_theme)

#         # Top bar
#         top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.05))
#         self.system_label = Label(
#             text="NEXUS-X SYSTEM",
#             font_size=14,
#             font_name=FONT_PATH,
#             color=self.themes[self.current_theme],
#             halign='left', valign='middle'
#         )
#         self.time_label = Label(
#             text=self.get_current_time(),
#             font_size=14,
#             font_name=FONT_PATH,
#             color=self.themes[self.current_theme],
#             halign='right', valign='middle'
#         )
#         top_bar.add_widget(self.system_label)
#         top_bar.add_widget(self.time_label)
#         self.add_widget(top_bar)

#         # Chat display
#         self.chat_area = TextInput(
#             text=self.chat_log,
#             readonly=True,
#             font_size=14,
#             font_name=FONT_PATH,
#             foreground_color=self.themes[self.current_theme],
#             background_color=(0, 0, 0, 1),
#             size_hint=(1, 0.7),
#             padding=[10, 10, 10, 10],
#             cursor_blink=False
#         )
#         self.add_widget(self.chat_area)

#         # Optional text input if in text mode
#         if input_method == "text":
#             self.input_field = TextInput(
#                 hint_text="Escribe tu comando aquí...",
#                 multiline=False,
#                 font_size=14,
#                 font_name=FONT_PATH,
#                 foreground_color=(0.7, 1, 0.7, 1),
#                 background_color=(0.1, 0.1, 0.1, 1),
#                 size_hint=(1, 0.08),
#                 padding=[10, 10, 10, 10],
#                 cursor_blink=True
#             )
#             self.input_field.bind(on_text_validate=self.on_enter_pressed)
#             self.add_widget(self.input_field)
#             Clock.schedule_interval(self.animate_cursor, 0.5)

#         # Bottom bar
#         self.bottom_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

#         command_button = Button(
#             text="Comandos",
#             font_size=12,
#             font_name=FONT_PATH,
#             background_normal='',
#             background_color=(0, 0, 0, 1),
#             color=self.themes[self.current_theme],
#             size_hint=(0.2, 1),
#             border=(10, 10, 10, 10)
#         )
#         command_button.bind(on_release=self.show_command_popup)

#         theme_button = Button(
#             text="Tema",
#             font_size=12,
#             font_name=FONT_PATH,
#             background_normal='',
#             background_color=(0, 0, 0, 1),
#             color=self.themes[self.current_theme],
#             size_hint=(0.2, 1),
#             border=(10, 10, 10, 10)
#         )
#         theme_button.bind(on_release=lambda x: self.switch_theme())

#         self.status_label = Label(
#             text=f"Estado: {self.status}",
#             font_size=14,
#             font_name=FONT_PATH,
#             color=(1, 0.4, 0.4, 1),
#             halign='center', valign='middle',
#             size_hint=(0.4, 1)
#         )
#         self.status_label.bind(size=self.status_label.setter('text_size'))

#         shutdown_btn = Button(
#             text="Apagar",
#             font_size=12,
#             font_name=FONT_PATH,
#             background_normal='',
#             background_color=(0, 0, 0, 1),
#             color=(1, 0.4, 0.4, 1),
#             size_hint=(0.2, 1),
#             border=(10, 10, 10, 10)
#         )
#         shutdown_btn.bind(on_release=self.confirm_shutdown)

#         self.bottom_bar.add_widget(command_button)
#         self.bottom_bar.add_widget(theme_button)
#         self.bottom_bar.add_widget(self.status_label)
#         self.bottom_bar.add_widget(shutdown_btn)
#         self.add_widget(self.bottom_bar)

#         Clock.schedule_interval(self.blink_status, 0.5)
#         Clock.schedule_interval(self.update_time, 1)

#     def update_graphics(self, *args):
#         self.rect.size = self.size
#         self.rect.pos = self.pos
#         self.top_line.points = [self.x, self.top, self.right, self.top]

#     def get_current_time(self):
#         return datetime.now().strftime("%H:%M:%S")

#     def update_time(self, dt):
#         self.time_label.text = self.get_current_time()

#     def add_message(self, sender, message):
#         self.chat_log += f"{sender}: {message}\n"
#         self.chat_area.text = self.chat_log
#         self.chat_area.cursor = (0, len(self.chat_area.text))

#     def set_status(self, new_status):
#         self.status = new_status
#         self.status_label.text = f"Estado: {self.status}"

#     def blink_status(self, dt):
#         if random.random() < 0.1:  # 10% glitch
#             glitch_text = list(self.status_label.text)
#             if len(glitch_text) > 0:
#                 glitch_index = random.randint(0, len(glitch_text) - 1)
#                 glitch_text[glitch_index] = random.choice(['▒', '▓', '█'])
#                 self.status_label.text = ''.join(glitch_text)
#         else:
#             self.status_label.text = f"Estado: {self.status}"

#         if self.status_label.color[3] == 1:
#             self.status_label.color = (1, 0.4, 0.4, 0.6)
#         else:
#             self.status_label.color = (1, 0.4, 0.4, 1)

#     def show_command_popup(self, instance):
#         content = BoxLayout(orientation='vertical', padding=10, spacing=5)
#         commands = ["/start", "/help", "/status", "/mode", "/exit"]
#         for cmd in commands:
#             btn = Button(
#                 text=cmd,
#                 font_size=12,
#                 font_name=FONT_PATH,
#                 background_normal='',
#                 background_color=(0, 0, 0, 1),
#                 color=self.themes[self.current_theme],
#                 size_hint_y=None, height=30,
#                 border=(10, 10, 10, 10)
#             )
#             btn.bind(on_release=lambda btn: self.add_message("Comando", btn.text))
#             content.add_widget(btn)

#         popup = Popup(
#             title='Comandos Disponibles',
#             content=content,
#             size_hint=(0.4, 0.6),
#             background_color=(0, 0, 0, 1),
#             separator_color=self.themes[self.current_theme],
#         )
#         popup.open()

#     def confirm_shutdown(self, instance):
#         content = BoxLayout(orientation='vertical', padding=10, spacing=10)
#         label = Label(
#             text="¿Estás seguro de apagar el asistente?",
#             font_size=14,
#             font_name=FONT_PATH,
#             color=(1, 0.4, 0.4, 1)
#         )
#         button_bar = BoxLayout(orientation='horizontal', spacing=10)
#         yes_btn = Button(
#             text="Sí",
#             font_size=12,
#             font_name=FONT_PATH,
#             background_normal='',
#             background_color=(0, 0, 0, 1),
#             color=(1, 0.4, 0.4, 1)
#         )
#         no_btn = Button(
#             text="No",
#             font_size=12,
#             font_name=FONT_PATH,
#             background_normal='',
#             background_color=(0, 0, 0, 1),
#             color=self.themes[self.current_theme]
#         )
#         button_bar.add_widget(yes_btn)
#         button_bar.add_widget(no_btn)
#         content.add_widget(label)
#         content.add_widget(button_bar)

#         popup = Popup(
#             title='Confirmar Apagado',
#             content=content,
#             size_hint=(0.4, 0.3),
#             background_color=(0, 0, 0, 1),
#             separator_color=(1, 0.4, 0.4, 1),
#         )

#         yes_btn.bind(on_release=lambda x: self.start_shutdown_sequence(popup))
#         no_btn.bind(on_release=popup.dismiss)
#         popup.open()

#     def start_shutdown_sequence(self, popup):
#         popup.dismiss()
#         self.disable_interface()
#         self.run_countdown(3)

#     def disable_interface(self):
#         self.bottom_bar.disabled = True
#         self.chat_area.disabled = True
#         if hasattr(self, 'input_field'):
#             self.input_field.disabled = True

#     def run_countdown(self, seconds):
#         if seconds > 0:
#             self.set_status(f"Apagando en {seconds}...")
#             Clock.schedule_once(lambda dt: self.run_countdown(seconds - 1), 1)
#         else:
#             Clock.schedule_once(lambda dt: sys.exit(), 1)

#     def on_enter_pressed(self, instance):
#         user_input = instance.text.strip()
#         if user_input and process_user_input_callback:
#             instance.text = ""
#             process_user_input_callback(user_input)

#     def animate_cursor(self, dt):
#         if hasattr(self, 'input_field'):
#             current_color = self.input_field.cursor_color
#             if current_color == [1, 1, 1, 1]:
#                 self.input_field.cursor_color = [0.3, 0.8, 1, 1]
#             else:
#                 self.input_field.cursor_color = [1, 1, 1, 1]
                
#     def apply_theme(self, theme_name):
#         color = self.themes.get(theme_name, (0.3, 0.8, 1, 1))
#         if hasattr(self, 'system_label'):
#             self.system_label.color = color
#         if hasattr(self, 'time_label'):
#             self.time_label.color = color
#         if hasattr(self, 'chat_area'):
#             self.chat_area.foreground_color = color

#     def switch_theme(self):
#         next_theme = random.choice(list(self.themes.keys()))
#         self.apply_theme(next_theme)

# class NexusApp(App):
#     def __init__(self, input_method="text", **kwargs):
#         super().__init__(**kwargs)
#         self.input_method = input_method

#     def build(self):
#         global gui_instance
#         gui_instance = NexusGUI(input_method=self.input_method)
#         return gui_instance

# def start_gui(input_method="text"):
#     app = NexusApp(input_method=input_method)
#     app.run()

# def update_gui_chat(sender, message):
#     if gui_instance:
#         Clock.schedule_once(lambda dt: gui_instance.add_message(sender, message))

# def update_gui_status(new_status):
#     if gui_instance:
#         Clock.schedule_once(lambda dt: gui_instance.set_status(new_status))

# def set_user_input_callback(callback):
#     global process_user_input_callback
#     process_user_input_callback = callback
