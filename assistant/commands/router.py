from assistant.commands.core_commands import handle_core_command
from assistant.commands.intelligent_commands import handle_intelligent_command

def handle_command(command: str, ctx=None) -> str:
    """
    Processes a given command string and delegates it to the appropriate handler.

    Args:
        command (str): The command string to be processed. The first word is treated as the command,
                       and the subsequent words are treated as arguments.
        ctx (optional): An optional context object that can be passed to the command handlers.

    Returns:
        str: The response from the appropriate command handler, or a default message if the command
             is not recognized.

    Notes:
        - The function first attempts to handle the command using `handle_core_command`.
        - If `handle_core_command` does not return a response, it tries `handle_intelligent_command`.
        - If neither handler recognizes the command, a default "Unknown command" message is returned.
    """
    tokens = command.split()
    cmd = tokens[0]
    args = tokens[1:]

    response = handle_core_command(cmd, args, ctx)
    if response:
        return response

    response = handle_intelligent_command(cmd, args, ctx)
    if response:
        return response

    return "Unknown command. Try /modo, /lang, /proveedor, /estado, /reiniciar, /recordar, /ver, /borrar."
