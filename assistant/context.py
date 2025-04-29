from assistant.utils.settings_manager import save_mode_to_config, save_lang_to_config, save_provider_to_config, load_settings
from datetime import datetime, timedelta

MAX_HISTORY_MINUTES = 10  # duración máxima del historial en minutos

class ContextManager:
    def __init__(self):
        """
        Initializes the Context Manager for NEXUS-X Core.
        """
        self.history = []
        self.mode = "default"
        self.lang = "es"
        self.provider = "openai"
        self.emotion = "neutral"  # Placeholder for future emotion simulation
        self.energy_level = 100   # Placeholder for future energy simulation (0-100)
        self.reminders_index = {}  # Mapping from number to reminder UUID
        self.pending_action = None  # Pending action confirmation (e.g., delete reminder)
        self.pending_description = None  # Description of what is pending

    # ====== HISTORY MANAGEMENT ======
    def get_history(self):
        visible_history = [{"role": m["role"], "content": m["content"]} for m in self.history]
        print(f"📚 [DEBUG] Mensajes enviados a OpenAI ({len(visible_history)}):")
        for i, m in enumerate(visible_history):
            print(f"  [{i}] {m['role']}: {m['content'][:60]}...")
        return visible_history


    def add_message(self, role, content):
        """Añade un mensaje con marca temporal y recorta automáticamente."""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })
        self.trim_history_by_time()

    def trim_history_by_time(self):
        """Elimina mensajes del historial que sean más antiguos de X minutos."""
        cutoff = datetime.utcnow() - timedelta(minutes=MAX_HISTORY_MINUTES)
        self.history = [m for m in self.history if m.get("timestamp", cutoff) >= cutoff]

    def clear_history(self):
        self.history = []

    # ====== CONFIGURATION MANAGEMENT ======

    def get_mode(self):
        return self.mode

    def set_mode(self, new_mode):
        self.mode = new_mode
        save_mode_to_config(new_mode)

    def get_lang(self):
        return self.lang

    def set_lang(self, new_lang):
        self.lang = new_lang
        save_lang_to_config(new_lang)

    def get_provider(self):
        return self.provider

    def set_provider(self, new_provider):
        self.provider = new_provider
        save_provider_to_config(new_provider)

    # ====== SYSTEM STATE MANAGEMENT ======

    def get_emotion(self):
        return self.emotion

    def set_emotion(self, new_emotion):
        self.emotion = new_emotion

    def get_energy_level(self):
        return self.energy_level

    def set_energy_level(self, new_level):
        self.energy_level = max(0, min(100, new_level))  # Always between 0 and 100

    # ====== REMINDERS INDEX MANAGEMENT ======

    def set_reminders_index(self, reminders):
        self.reminders_index = {str(i + 1): reminder["id"] for i, reminder in enumerate(reminders)}

    def get_reminder_uuid(self, index):
        return self.reminders_index.get(str(index))

    # ====== PENDING ACTION MANAGEMENT ======

    def set_pending_action(self, action_type, reminder_id, description):
        self.pending_action = {"type": action_type, "reminder_id": reminder_id}
        self.pending_description = description

    def get_pending_action(self):
        return self.pending_action

    def get_pending_description(self):
        return self.pending_description

    def clear_pending_action(self):
        self.pending_action = None
        self.pending_description = None

    # ====== RESET METHOD ======

    def reset(self):
        self.clear_history()
        mode, lang, provider = load_settings()
        self.mode = mode
        self.lang = lang
        self.provider = provider
        self.emotion = "neutral"
        self.energy_level = 100
        self.reminders_index = {}
        self.pending_action = None
        self.pending_description = None
