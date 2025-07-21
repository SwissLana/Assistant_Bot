from .book import Field, Record, Phone, Birthday, Email, Address, Name, Note, AddressBook
from .utils import normalize_name, format_address, extract_tags_from_text
from .decorators import input_error
from datetime import datetime
import re

@input_error
def add_contact(args, book, command="addcontact"):
    if len(args) < 2:
        raise IndexError("😓 You must provide at least a name and one valid 10-digit phone number.")

    phone_start_index = None
    for i, arg in enumerate(args):
        if arg.isdigit() and len(arg) == 10:
            phone_start_index = i
            break

    if phone_start_index is None:
        raise ValueError("😓 At least one valid phone number is required (10 digits).")

    name_parts = args[:phone_start_index]
    if not name_parts:
        raise ValueError("😓 Name is missing.")
    name = normalize_name(" ".join(name_parts))
    if book.name_exists(name):
        return f"😓 A contact named '{name}' already exists."

    phones = []
    i = phone_start_index
    while i < len(args) and args[i].isdigit() and len(args[i]) == 10:
        phones.append(args[i])
        i += 1

    record = Record(name)
    for phone in phones:
        result = record.add_phone(phone, book)
        if result:
            return result

    email = None
    address_parts = []

    while i < len(args):
        arg = args[i]
        if "@" in arg:
            email = arg
        else:
            address_parts.append(arg)
        i += 1

    if email:
        record.add_email(email.strip())
    if address_parts:
        raw_address = " ".join(address_parts).strip()
        formatted_address = format_address(raw_address)
        record.add_address(formatted_address)

    book.add_record(record)
    return "✅ Contact added!"

@input_error
def edit_contact_name(args, book, command="editname"):
    if len(args) < 2:
        raise IndexError
    for i in range(1, len(args)):
        old_name_try = normalize_name(" ".join(args[:i]))
        if book.name_exists(old_name_try):
            old_name = old_name_try
            new_name = normalize_name(" ".join(args[i:]))
            break
    else:
        raise KeyError
    record = book.find(old_name)
    book.delete(old_name)
    record.name = Name(new_name)
    book.add_record(record)
    return f"✅ Contact name changed to '{new_name}'!"

@input_error
def change_contact(args, book, command="changephone"):
    if len(args) < 3:
        raise IndexError
    old_phone = args[-2]
    new_phone = args[-1]
    name = normalize_name(" ".join(args[:-2]))
    record = book.find(name)
    if not record:
        raise KeyError
    result = record.edit_phone(old_phone, new_phone, book)
    if result:
        return result
    return "✅ Phone number updated!"

@input_error
def add_phone_to_contact(args, book, command="addphone"):
    if len(args) < 2:
        raise IndexError
    possible_phone = args[-1]
    name = normalize_name(" ".join(args[:-1]))
    record = book.find(name)
    if not record:
        raise KeyError
    result = record.add_phone(possible_phone, book)
    if result:
        return result
    return "✅ Phone number added!"

@input_error
def remove_phone(args, book, command="removephone"):
    if len(args) < 2:
        raise IndexError
    possible_phone = args[-1]
    name = normalize_name(" ".join(args[:-1]))
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.remove_phone(possible_phone):
        return f"😓 Phone number '{possible_phone}' not found."
    return "✅ Phone number removed!"

@input_error
def remove_contact(args, book, command="removecontact"):
    if not args:
        raise IndexError
    name = normalize_name(" ".join(args))
    if not book.delete(name):
        raise KeyError
    return f"✅ Contact '{name}' removed!"

@input_error
def add_birthday(args, book, command="addbday"):
    if len(args) < 2:
        raise IndexError
    name = normalize_name(" ".join(args[:-1]))
    birthday = args[-1]
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        return "😓 Invalid date format. Use DD.MM.YYYY, for example, 15.05.1990."
    record = book.find(name)
    if not record:
        raise KeyError
    if record.birthday:
        return "😓 Birthday is already set. Use ‘editbday’ to change it."
    record.add_birthday(birthday)
    return "🎉 Birthday added!"

@input_error
def show_birthday(args, book, command="showbday"):
    if not args:
        raise IndexError
    name = normalize_name(" ".join(args))
    matches = [record for key, record in book.data.items() if name.lower() in key.lower()]
    if not matches:
        raise KeyError
    if len(matches) == 1:
        record = matches[0]
        if record.birthday:
            return f"🎂 Birthday {record.name.value}: {record.birthday.value}"
        else:
            return "😓 Birthday is not set."
    matches_with_birthday = [r for r in matches if r.birthday]
    if not matches_with_birthday:
        return "😓 None of the contacts have a birthday set."
    result = ["Multiple contacts found:"]
    result += [f"{record.name.value}: {record.birthday.value}" for record in matches]
    result.append("Please provide the full name for an exact match.")
    return "\n".join(result)

@input_error
def edit_birthday(args, book, command="editbday"):
    if len(args) < 2:
        raise IndexError
    name = normalize_name(" ".join(args[:-1]))
    birthday = args[-1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_birthday(birthday)
    return "✅ Birthday updated!"

@input_error
def remove_birthday(args, book, command="removebday"):
    if not args:
        raise IndexError
    name = normalize_name(" ".join(args))
    record = book.find(name)
    if not record:
        raise KeyError
    record.remove_birthday()
    return "✅ Birthday removed!"

@input_error
def show_phone(args, book, command="showphone"):
    if not args:
        raise IndexError
    
    raw_input = " ".join(args)
    digits_only = "".join(filter(str.isdigit, raw_input))
    
    matches = []
    if len(digits_only) == 10:
        matches = [
            record for record in book.data.values()
            if any(phone.value == digits_only for phone in record.phones)
        ]
    else:
        name = normalize_name(" ".join(args))
        matches = [record for key, record in book.data.items() if name.lower() in key.lower()]
    if not matches:
        raise KeyError
    if len(matches) == 1:
        record = matches[0]
        return f"{record.name.value}: {', '.join(p.value for p in record.phones)}"

    result = ["Multiple contacts found:"]
    result += [f"{r.name.value}: {', '.join(p.value for p in r.phones)}" for r in matches]
    return "\n".join(result)

@input_error
def search_contacts(args, book, command="search"):
    if not args:
        raise IndexError
    query = args[0].lower()
    
    if query in ["note", "notes"]:
        return "To search notes, use: searchnote <keyword>"
    if query in ["email"]:
        return "Just type 'search' followed by a valid email like 'search example@example.com' or contact name."
    if query in ["address"]:
        return "Just type 'search' followed by a keyword from the address."
    if query in ["phone", "phones"]:
        return "Use 'showphone' command or type 'search' followed by a phone number like 'search 0661234567'."
    if query in ["birthday", "bday", "birth"]:
        return "Use 'showbday' command or type 'search' followed by a date like 'search 22.07.1995' or 'search anna'."
    if query in ["name", "contact"]:
        return "Just type 'search' followed by a name like 'search Ivan'."
    if query in ["tag"]:
        return "Just type 'search' followed by a tag like 'search #yourtag'."
    results = book.search(query)
    return "\n".join(results) if results else "😓 No matches found."

@input_error
def upcoming_birthdays(args, book, command="upcomingbdays"):
    if args:
        raise IndexError
    upcoming = book.get_upcoming_birthdays()
    return "\n".join(upcoming) if upcoming else "🎂 No upcoming birthdays in the next 7 days."

@input_error
def add_address(args, book, command="addaddress"):
    if len(args) < 2:
        raise IndexError
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            address = " ".join(args[i:]).title()
            break
    else:
        return "😓 Contact not found."
    record = book.find(name)
    if record.address:
        return "😓 Address already exists. Use ‘editaddress’ to change it."
    record.add_address(address)
    return "✅ Address added!"

@input_error
def edit_address(args, book, command="editaddress"):
    if len(args) < 2:
        raise IndexError
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            new_address = " ".join(args[i:]).title()
            break
    else:
        return "😓 Contact not found."
    record = book.find(name)
    record.edit_address(new_address)
    return "✅ Address updated!"

@input_error
def remove_address(args, book, command="removeaddress"):
    if not args:
        raise IndexError
    name = normalize_name(" ".join(args))
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.address:
        return "😓 Address is not set."
    record.remove_address()
    return "✅ Address removed!"

@input_error
def add_email(args, book, command="addemail"):
    if len(args) < 2:
        raise IndexError
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            email = " ".join(args[i:])
            break
    else:
        return "😓 Contact not found."
    record = book.find(name)
    if record.email:
        return "😓 Email already exists. Use ‘editemail’ to change it."
    record.add_email(email)
    return "✅ Email added!"

@input_error
def edit_email(args, book, command="editemail"):
    if len(args) < 2:
        raise IndexError
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            new_email = " ".join(args[i:])
            break
    else:
        return "😓 Contact not found."
    record = book.find(name)
    result = record.edit_email(new_email)
    if result is not None:
        return result

    return "✅ Email updated!"

@input_error
def remove_email(args, book, command="removeemail"):
    if not args:
        raise IndexError
    for i in range(1, len(args) + 1):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            break
    else:
        return "😓 Please provide a valid contact name."

    record = book.find(name)
    if not record:
        return "😓 Contact not found."

    if not record.email:
        return "😓 Email is not set."

    record.remove_email()
    return "✅ Email removed!"

@input_error
def add_note(args, book, command="addnote"):
    if len(args) < 2:
        raise IndexError

    for i in range(1, len(args)):
        name_try = normalize_name(" ".join(args[:i]))
        if book.name_exists(name_try):
            name = name_try
            note_text = " ".join(args[i:])
            break
    else:
        return "😓 Contact not found."

    tags = extract_tags_from_text(note_text)
    clean_text = re.sub(r"#\w+", "", note_text).strip()

    record = book.find(name)
    note_result = record.add_note(clean_text, tags)

    if note_result is None:
        return f"😓 Note already exists. Use 'editnote' to modify it."
    return f"✅ Note added with tags: {', '.join(note_result.tags) if note_result.tags else 'none'}"

@input_error
def edit_note(args, book, command="editnote"):
    if len(args) < 3:
        raise IndexError

    for i in range(1, len(args)):
        name_try = normalize_name(" ".join(args[:i]))
        if book.name_exists(name_try):
            name = name_try
            break
    else:
        return "😓 Please provide the contact name, old note text and new note text."

    record = book.find(name)
    remaining = args[i:]

    for j in range(1, len(remaining)):
        old_candidate = " ".join(remaining[:j]).strip().lower()
        for note in record.notes:
            if note.text.strip().lower() == old_candidate:
                old_text = " ".join(remaining[:j])
                new_text = " ".join(remaining[j:])
                break
        else:
            continue
        break
    else:
        return "😓 Old note not found. Please check the old note text. Be exact."

    tags = extract_tags_from_text(new_text)
    clean_new_text = re.sub(r"#\w+", "", new_text).strip()

    result = record.edit_note(old_text, clean_new_text)
    if "edited" in result.lower():
        for note in record.notes:
            if note.text.strip().lower() == clean_new_text.lower():
                if tags:
                    note.tags = set(tags)
        return f"✅ Note updated{' with tags: ' + ', '.join(tags) if tags else ''}"
    return result
    
@input_error
def remove_note(args, book, command="removenote"):
    if not args:
        raise IndexError

    for i in range(1, len(args) + 1):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            record = book.find(name)
            note_text = " ".join(args[i:]).strip()

            if not note_text:
                if not record.notes:
                    return f"ℹ️ No notes to remove for '{name}'."
                record.notes.clear()
                return f"🗑️ All notes removed for '{name}'."

            if record.remove_note(note_text):
                return "✅ Note removed!"
            else:
                return "😓 Note not found."
    return "🤔 Please provide the contact name and note text to remove."

@input_error
def search_note(args, book, command="searchnote"):
    if not args:
        raise IndexError

    query = " ".join(args).lower()
    matches = set()

    for record in book.values():
        name_match = query in record.name.value.lower()
        for note in record.notes:
            note_match = query in note.text.lower()
            if name_match or note_match:
                matches.add(f"{record.name.value}: {note}")

    return "\n".join(matches) if matches else "😓 No notes found."

@input_error
def add_tag_to_note(args, book, command="addtag"):
    if len(args) < 3:
        raise IndexError
    for i in range(1, len(args) - 1):
        name_try = normalize_name(" ".join(args[:i]))
        if book.name_exists(name_try):
            name = name_try
            break
    else:
        return "📝 Please provide the contact name, note text and tag to add."

    record = book.find(name)
    note_text = " ".join(args[i:-1])
    tag = args[-1].lstrip("#").lower()

    for note in record.notes:
        if note.text.strip().lower() == note_text.strip().lower():
            try:
                if tag in note.tags:
                    return f"⚠️ Tag '#{tag}' is already present in the note."
                note.add_tag(tag)
                return f"🏷️ Tag '#{tag}' added to note: {note.text}"
            except ValueError as ve:
                return str(ve)
    return "😓 Note not found. Please check the note text. Be exact."


@input_error
def remove_tag_from_note(args, book, command="removetag"):
    if len(args) < 2:
        raise IndexError

    for i in range(1, len(args) + 1):
        name_try = normalize_name(" ".join(args[:i]))
        if book.name_exists(name_try):
            name = name_try
            rest_args = args[i:]
            break
    else:
        return "😓 Please provide the contact name, note text and a tag to remove."

    if not rest_args:
        return "😓 Please provide the note text and a tag to remove."

    full_text = " ".join(rest_args)
    tag_match = re.search(r"#\w+", full_text)
    tag_to_remove = tag_match.group(0)[1:].lower() if tag_match else None
    note_text = re.sub(r"#\w+", "", full_text).strip()

    record = book.find(name)

    for note in record.notes:
        if note.text.strip().lower() == note_text.lower():
            if tag_to_remove:
                if tag_to_remove in note.tags:
                    note.tags.remove(tag_to_remove)
                    return f"🗑️ Tag '#{tag_to_remove}' removed from note: '{note.text}'"
                else:
                    return f"😓 Tag '#{tag_to_remove}' not found in this note."
            else:
                if note.tags:
                    note.tags.clear()
                    return f"🗑️ All tags removed from note: '{note.text}'"
                else:
                    return f"ℹ️ This note has no tags."
    return f"🤔 Please provide the note text and a tag to remove for '{name}'."

@input_error
def search_note_by_tag(args, book, command="searchtag"):
    if not args:
        raise IndexError
    tag = args[0].lstrip("#").lower()
    matches = []
    for record in book.values():
        for note in record.notes:
            if note.has_tag(tag):
                matches.append(f"{record.name.value}: {note}")
    return "\n".join(matches) if matches else f"😓 No notes with tag '#{tag}' found."


@input_error
def sort_note_by_tag(args, book, command="sorttag"):
    tag_map = {}

    for record in book.values():
        for note in record.notes:
            for tag in note.tags:
                tag = tag.lower()
                tag_map.setdefault(tag, []).append((record.name.value, note))

    if not tag_map:
        return "😓 No tagged notes to sort."

    result_lines = []
    for tag in sorted(tag_map):
        result_lines.append(f"📌 #{tag}")
        for name, note in tag_map[tag]:
            result_lines.append(f"{name}: {note}")
        result_lines.append("")  # empty line for spacing

    return "\n".join(result_lines)

