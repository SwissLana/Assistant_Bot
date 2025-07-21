from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

def show_all_rich(book):
    if not book:
        console.print("😓 Address book is empty.", style="yellow")
        return

    table = Table(title="📒 Address Book", show_lines=True)
    table.add_column("Name", style="bold magenta")
    table.add_column("Phones", style="green")
    table.add_column("Birthday", style="cyan")
    table.add_column("Email", style="blue")
    table.add_column("Address", style="white")
    table.add_column("Notes", style="yellow")

    for record in book.values():
        phones = ", ".join(phone.value for phone in record.phones) if record.phones else "-"
        birthday = record.birthday.value if record.birthday else "-"
        email = record.email.value if record.email else "-"
        address = record.address.value if record.address else "-"

        notes_block = Text("-")
        if record.notes:
            notes_block = Text()
            for note in record.notes:
                note_text = Text(note.text, style="bold yellow")
                tags_text = Text(" " + " ".join(f"#{tag}" for tag in note.tags), style="dim") if note.tags else Text("")
                notes_block.append_text(note_text)
                notes_block.append_text(tags_text)
                notes_block.append("\n")

        table.add_row(
            record.name.value,
            phones,
            birthday,
            email,
            address,
            notes_block
        )

    console.print(table)
    return ""
