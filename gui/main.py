from kivy.app import App
from .layouts import NexusGUI

_gui_instance = None
_process_user_input_callback = None

def get_gui_instance():
    global _gui_instance
    return _gui_instance

def set_user_input_callback(callback):
    global _process_user_input_callback
    _process_user_input_callback = callback
    if _gui_instance:
        _gui_instance.process_user_input_callback = callback

class NexusApp(App):
    def __init__(self, input_method="text", **kwargs):
        super().__init__(**kwargs)
        self.input_method = input_method

    def build(self):
        global _gui_instance
        _gui_instance = NexusGUI(input_method=self.input_method)
        _gui_instance.process_user_input_callback = _process_user_input_callback
        return _gui_instance
