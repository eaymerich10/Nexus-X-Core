import json
import os

class MemoryManager:
    def __init__(self, memory_file=".nexus_memory.json"):
        self.memory_file = memory_file
        self.data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("⚠️ Error al leer la memoria, iniciando vacía.")
                    return {}
        else:
            return {}

    def save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def set(self, key, value):
        self.data[key] = value
        self.save_memory()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def clear(self):
        self.data = {}
        self.save_memory()
        print("🧹 Memoria limpia.")

    def remove(self, key):
        if key in self.data:
            del self.data[key]
            self.save_memory()
