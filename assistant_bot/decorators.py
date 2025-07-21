def input_error(func):
    error_messages = {
        "addcontact": (
    "😓 The 'addcontact' command requires at least a name and a 10-digit phone number.\n"
    "👉 You can also optionally add more phone numbers, an email and an address.\n"
    "🔹 Examples:\n"
    "   'addcontact Ivan 0987654321'\n"
    "   'addcontact Ivan Petrov 0981112222 0663334444'\n"
    "   'addcontact Ivan 0987654321 ivan@example.com'\n"
    "   'addcontact Ivan 0987654321 ivan@gmail.com vul. Parkova 12, Kyiv'\n"
),
        "editname": "😓 The 'editname' command requires the old and new name. For example: 'editname Ivan Petro'",
        "removecontact": "😓 The 'removecontact' command requires a name. For example: 'removecontact Ivan'",
        "addphone": "😓 The 'addphone' command requires a name and a phone number. For example: 'addphone Ivan 0661234567'",
        "changephone": "😓 The 'changephone' command requires a name, the old number and the new number. For example: 'changephone Ivan 0661234567 0961234567'",
        "removephone": "😓 The 'removephone' command requires a name and a phone number to remove. For example: 'removephone Ivan 0661234567'",
        "showphone": "😓 The 'showphone' command requires only a name. For example: 'showphone Ivan'",
        "addbday": "😓 The 'addbday' command requires a name and a date (DD.MM.YYYY). For example: 'addbday Ivan 15.05.1990'",
        "showbday": "😓 The 'showbday' command requires only a name. For example: 'showbday Ivan'",
        "editbday": "😓 The 'editbday' command requires a name and a new date (DD.MM.YYYY). For example: 'editbday Ivan 16.05.1990'",
        "removebday": "😓 The 'removebday' command requires a name. For example: 'removebday Ivan'",
        "upcomingbdays": "😓 The 'upcomingbdays' command doesn’t require any arguments. Just type 'upcomingbdays'.",
        "search": "😓 The 'search' command requires a query like name, phone, birthday, email or address. For example: 'search Ivan' or 'search 0661234567' or search '15.05.1990' or search 'ivan@example.com' or search 'vul. 3, Kyiv'",
        "all": "😓 The 'all' command doesn’t require any arguments. Just type 'all'.",
        "addemail": "😓 The 'addemail' command requires a name and an email. For example: 'addemail Ivan ivan@example.com'",
        "editemail": "😓 The 'editemail' command requires a name and a new email. For example: 'editemail Ivan new@example.com'",
        "removeemail": "😓 The 'removeemail' command requires a name. For example: 'removeemail Ivan'",
        "addaddress": "😓 The 'addaddress' command requires a name and an address. For example: 'addaddress Ivan vul. Vilna 1, Kyiv'",
        "editaddress": "😓 The 'editaddress' command requires a name and a new address. For example: 'editaddress Ivan vul. New 2, Kyiv'",
        "removeaddress": "😓 The 'removeaddress' command requires a name. For example: 'removeaddress Ivan'",
        "addnote": "😓 The 'addnote' command requires a name and a note text. You can optionally include tags using #. For example: 'addnote Ivan Meeting at 3:00 PM #urgent'",
        "editnote": "😓 The 'editnote' command requires a name, the old note and the new note. You can also include tags. For example: 'editnote Ivan Meeting at 3:00 PM Meeting rescheduled to 4:00 PM #urgent'",
        "removenote": (
    "😓 The 'removenote' command requires a name and optionally the note text.\n"
    "🔹 Example 1 (remove specific note): 'removenote Ivan Meeting at 3:00 PM'\n"
    "🔹 Example 2 (remove all notes): 'removenote Ivan'"
),
        "searchnote": "😓 The 'searchnote' command requires a keyword query. For example: 'searchnote Meeting'",
        "searchtag": "😓 The 'searchtag' command requires a tag. For example: 'searchtag #urgent'",
        "addtag": "😓 The 'addtag' command requires a name, the note text and the tag. For example: 'addtag Ivan Project planning #meeting'",
        "removetag": (
    "😓 The 'removetag' command requires a name, the note text and a tag to remove.\n"
    "🔹 Example 1 (remove specific tag): 'removetag Ivan Meeting at 3:00 PM #urgent'\n"
    "🔹 Example 2 (remove all tags from note): 'removetag Ivan Meeting at 3:00 PM'"
),
        "default": "😓 Invalid command or arguments. Type 'help' to see available commands."
    }

    def inner(*args, **kwargs):
        command = kwargs.get('command', 'default')
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError as e:
            return str(e) or error_messages.get(command, error_messages["default"])
        except KeyError:
            return "😓 Contact not found."
        except IndexError:
            return error_messages.get(command, error_messages["default"])
        except Exception as e:
            return f"😓 Something went wrong: {str(e)}"
    return inner

