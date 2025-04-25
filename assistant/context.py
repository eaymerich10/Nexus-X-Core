class ContextManager:
    def __init__(self):
        self.history = []
        self.mode = "default"
        self.lang = "es"
        self.provider = "openai"

    def get_history(self):
        return self.history.copy()

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_mode(self):
        return self.mode

    def set_mode(self, new_mode):
        self.mode = new_mode
        from assistant.core import save_mode_to_config
        save_mode_to_config(new_mode)

    def get_lang(self):
        return self.lang

    def set_lang(self, new_lang):
        self.lang = new_lang
        from assistant.core import save_lang_to_config
        save_lang_to_config(new_lang)

    def get_provider(self):
        return self.provider

    def set_provider(self, new_provider):
        self.provider = new_provider
        from assistant.core import save_provider_to_config
        save_provider_to_config(new_provider)

    def reset(self):
        self.history = []
        from assistant.core import load_settings
        mode, lang, provider = load_settings()
        self.mode = mode
        self.lang = lang
        self.provider = provider
    