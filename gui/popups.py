from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from .config import FONT_PATH, THEMES

def show_command_popup(gui):
    content = BoxLayout(orientation='vertical', padding=10, spacing=5)
    commands = ["/start", "/help", "/status", "/mode", "/exit"]
    for cmd in commands:
        btn = Button(
            text=cmd, font_size=12, font_name=FONT_PATH,
            background_normal='', background_color=(0, 0, 0, 1),
            color=THEMES[gui.current_theme], size_hint_y=None, height=30
        )
        btn.bind(on_release=lambda btn: gui.add_message("Comando", btn.text))
        content.add_widget(btn)

    popup = Popup(
        title='Comandos Disponibles', content=content,
        size_hint=(0.4, 0.6), background_color=(0, 0, 0, 1),
        separator_color=THEMES[gui.current_theme]
    )
    popup.open()

def confirm_shutdown(gui):
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    label = Label(
        text="¿Estás seguro de apagar el asistente?",
        font_size=14, font_name=FONT_PATH, color=(1, 0.4, 0.4, 1)
    )
    button_bar = BoxLayout(orientation='horizontal', spacing=10)
    yes_btn = Button(
        text="Sí", font_size=12, font_name=FONT_PATH,
        background_normal='', background_color=(0, 0, 0, 1),
        color=(1, 0.4, 0.4, 1)
    )
    no_btn = Button(
        text="No", font_size=12, font_name=FONT_PATH,
        background_normal='', background_color=(0, 0, 0, 1),
        color=THEMES[gui.current_theme]
    )
    button_bar.add_widget(yes_btn)
    button_bar.add_widget(no_btn)
    content.add_widget(label)
    content.add_widget(button_bar)

    popup = Popup(
        title='Confirmar Apagado', content=content,
        size_hint=(0.4, 0.3), background_color=(0, 0, 0, 1),
        separator_color=(1, 0.4, 0.4, 1)
    )

    yes_btn.bind(on_release=lambda x: gui.start_shutdown_sequence(popup))
    no_btn.bind(on_release=popup.dismiss)
    popup.open()
