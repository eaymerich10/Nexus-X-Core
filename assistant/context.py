class ContextManager:
    def __init__(self):
        self.history = []

    def get_history(self):
        return self.history.copy()

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
