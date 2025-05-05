from services.supabase.supabase_reminders import add_reminder, list_reminders, delete_reminder
from core.texts import get_text

def handle_intelligent_command(cmd, args, ctx):
    """
    Handles intelligent commands for managing reminders.

    Args:
        cmd (str): The command to execute.
        args (list): A list of arguments associated with the command.
        ctx (ContextManager): Contextual manager object for session data.

    Returns:
        str: A response message indicating the result of the command execution.
    """
    user_id = 1  # Asumimos usuario ID 1 por ahora
    lang = ctx.get_lang() if ctx else "es"

    # Manejar respuestas a preguntas pendientes (yes/no)
    if ctx and ctx.get_pending_action():
        if cmd.lower() in ["yes", "sí", "si"]:
            pending = ctx.get_pending_action()
            if pending["type"] == "delete_reminder":
                reminder_id = pending["reminder_id"]
                success = delete_reminder(reminder_id)
                ctx.clear_pending_action()
                return "Reminder deleted." if success else "Failed to delete reminder."
        elif cmd.lower() == "no":
            ctx.clear_pending_action()
            return get_text("deletion_cancelled", lang)
        else:
            return get_text("confirm_yes_no", lang)

    # --- Comandos normales ---
    if cmd == "/recordar":
        if not args:
            return "Please provide a reminder text."
        message = " ".join(args)
        success = add_reminder(user_id, message)
        return "Reminder saved." if success else "Failed to save reminder."

    elif cmd == "/ver":
        reminders = list_reminders(user_id)
        if not reminders:
            return "📭 No pending reminders."

        if ctx:
            ctx.set_reminders_index(reminders)

        result = "\n".join([f"[{i+1}] {r['message']}" for i, r in enumerate(reminders)])
        return f"Pending Reminders:\n{result}"

    elif cmd == "/borrar":
        if not args:
            return "Please provide the number of the reminder to delete."

        reminder_number = args[0]

        if ctx:
            reminder_uuid = ctx.get_reminder_uuid(reminder_number)
            if reminder_uuid:
                # Buscar el mensaje para mostrarlo en la confirmación
                reminders = list_reminders(user_id)
                if 0 < int(reminder_number) <= len(reminders):
                    reminder_text = reminders[int(reminder_number)-1]['message']
                    ctx.set_pending_action("delete_reminder", reminder_uuid, reminder_text)
                    question = get_text("confirm_delete", lang).format(reminder=reminder_text)
                    return f"{question}"
                else:
                    return "Invalid reminder number."

        return "Error: context not available."

    return None
