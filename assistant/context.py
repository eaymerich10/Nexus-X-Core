from assistant.utils.settings_manager import save_mode_to_config, save_lang_to_config, save_provider_to_config, load_settings

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
        return self.history.copy()

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

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
        """
        Sets the mapping of reminder numbers to their UUIDs for easy deletion by number.
        """
        self.reminders_index = {str(i + 1): reminder["id"] for i, reminder in enumerate(reminders)}

    def get_reminder_uuid(self, index):
        """
        Returns the UUID of a reminder given its number as a string.
        """
        return self.reminders_index.get(str(index))

    # ====== PENDING ACTION MANAGEMENT ======

    def set_pending_action(self, action_type, reminder_id, description):
        """
        Sets a pending action that requires confirmation.
        """
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
        """
        Resets context: clears history, reloads configuration from settings,
        and resets internal emotional and energy states.
        """
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
