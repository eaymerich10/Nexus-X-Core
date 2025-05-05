from .config import THEMES

def apply_theme(gui, theme_name):
    color = THEMES.get(theme_name, THEMES["azul"])
    gui.current_theme = theme_name
    gui.system_label.color = color
    gui.time_label.color = color
    gui.chat_area.foreground_color = color

def switch_theme(gui):
    import random
    themes = list(THEMES.keys())
    next_theme = random.choice(themes)
    apply_theme(gui, next_theme)
