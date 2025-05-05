from kivy.app import App
from kivy.clock import Clock
from .layouts import NexusGUI

# Variables internas del módulo
gui_instance = None
process_user_input_callback = None

class NexusApp(App):
    def __init__(self, input_method="text", **kwargs):
        super().__init__(**kwargs)
        self.input_method = input_method

    def build(self):
        global gui_instance
        gui_instance = NexusGUI(input_method=self.input_method)
        return gui_instance

def start_gui(input_method="text"):
    app = NexusApp(input_method=input_method)
    app.run()

def update_gui_chat(sender, message):
    if gui_instance:
        Clock.schedule_once(lambda dt: gui_instance.add_message(sender, message))

def update_gui_status(new_status):
    if gui_instance:
        Clock.schedule_once(lambda dt: gui_instance.set_status(new_status))

def set_user_input_callback(callback):
    global process_user_input_callback
    process_user_input_callback = callback
