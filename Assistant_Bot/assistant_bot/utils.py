import re
import difflib

def normalize_name(name):
    def fix_part(part):
        return "-".join(subpart.capitalize() for subpart in part.split("-"))
    return " ".join(fix_part(word) for word in name.strip().split())

def format_address(address: str) -> str:
    parts = address.split()
    formatted = []

    for word in parts:
        if word.lower().endswith('.') and len(word) <= 4:
            formatted.append(word.lower())
        else:
            formatted.append(word.capitalize())

    return " ".join(formatted)

def suggest_command(input_cmd, valid_commands):
        
    prefix_matches = [cmd for cmd in valid_commands if cmd.startswith(input_cmd)]

    if prefix_matches:
        return f"🤔 Did you mean one of these commands: {', '.join(f'\'{cmd}\'' for cmd in prefix_matches)}? Please try again!"

    fuzzy_matches = difflib.get_close_matches(input_cmd, valid_commands, n=5, cutoff=0.6)

    if fuzzy_matches:
        if len(fuzzy_matches) == 1:
            return f"🤔 Did you mean '{fuzzy_matches[0]}'? Please try again!"
        else:
            return f"🤔 Did you mean one of these commands: {', '.join(f'\'{cmd}\'' for cmd in fuzzy_matches)}? Please try again!"

    return "😓 Sorry, that command doesn’t exist. Type 'help' to see available commands."

def extract_tags_from_text(text):
    return [tag[1:].lower() for tag in re.findall(r"#\w+", text)]

def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.strip().lower(), args


