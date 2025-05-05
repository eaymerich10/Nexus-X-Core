import random

def animate_cursor(gui, dt):
    if hasattr(gui, 'input_field'):
        current_color = gui.input_field.cursor_color
        gui.input_field.cursor_color = [0.3, 0.8, 1, 1] if current_color == [1, 1, 1, 1] else [1, 1, 1, 1]

def blink_status(gui, dt):
    if random.random() < 0.1:  # 10% glitch chance
        glitch_text = list(gui.status_label.text)
        if glitch_text:
            glitch_index = random.randint(0, len(glitch_text) - 1)
            glitch_text[glitch_index] = random.choice(['▒', '▓', '█'])
            gui.status_label.text = ''.join(glitch_text)
    else:
        gui.status_label.text = f"Estado: {gui.status}"

    if gui.status_label.color[3] == 1:
        gui.status_label.color = (1, 0.4, 0.4, 0.6)
    else:
        gui.status_label.color = (1, 0.4, 0.4, 1)
