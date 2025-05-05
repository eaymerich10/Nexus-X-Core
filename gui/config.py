import platform

if platform.machine() == 'x86_64':
    FONT_PATH = '/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf'
elif platform.machine() == 'aarch64':
    FONT_PATH = '/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf'
else:
    FONT_PATH = 'Roboto'  # fallback seguro

THEMES = {
    "azul": (0.3, 0.8, 1, 1),
    "verde": (0.4, 1, 0.4, 1),
    "purpura": (0.8, 0.3, 1, 1),
    "rojo": (1, 0.4, 0.4, 1)
}
