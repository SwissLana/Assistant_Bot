from assistant_bot.storage import DEFAULT_FILENAME
from assistant_bot.storage import save_address_book, load_address_book
from assistant_bot.commands import (
    add_contact, edit_contact_name, remove_contact, add_phone_to_contact, change_contact,
    remove_phone, show_phone, add_birthday, show_birthday, edit_birthday, remove_birthday,
    add_email, edit_email, remove_email, add_note, edit_note, remove_note, search_note,
    add_tag_to_note, remove_tag_from_note, search_note_by_tag, sort_note_by_tag,
    add_address, edit_address, remove_address, search_contacts, upcoming_birthdays
)
from assistant_bot.utils import parse_input, suggest_command
from assistant_bot.help import print_available_commands
from assistant_bot.utils import suggest_command
from assistant_bot.display import show_all_rich
from rich.console import Console

def main():
    console = Console()
    filename = DEFAULT_FILENAME
    book = load_address_book(filename)
    valid_commands = [
        "hello", "help", "exit", "close", "addcontact", "editname", "removecontact",
        "addphone", "changephone", "removephone", "showphone", "addbday", "showbday",
        "editbday", "removebday", "upcomingbdays", "search", "all", "addemail",
        "editemail", "removeemail", "addaddress", "editaddress", "removeaddress",
        "addnote", "editnote", "removenote", "searchnote", "addtag", 
        "removetag", "searchtag", "sorttag"
    ]
    console.print("😊 Welcome to the assistant bot!", style="green")
    console.print(f"Upcoming Birthdays:\n{upcoming_birthdays([], book)}", style="yellow")
    console.print("\nType 'help' to see available commands.", style="blue")
    try:
        while True:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                console.print("😓 You didn’t enter anything! Please try again.", style="yellow")
                continue
            command, args = parse_input(user_input)
            if command in ["exit", "close", "ex"]:
                save_address_book(book, filename)
                console.print("👋 Good bye!", style="green")
                break
            elif command == "hello":
                console.print("😊 How can I help you?", style="green")
            elif command == "addcontact":
                result = add_contact(args, book, command="addcontact")
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
            elif command == "editname":
                result = edit_contact_name(args, book, command="editname")
                console.print(result, style="green")
                if "changed" in result.lower():
                    save_address_book(book, filename)
            elif command == "removecontact":
                result = remove_contact(args, book, command="removecontact")
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
            elif command == "addphone":
                result = add_phone_to_contact(args, book, command="addphone")
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
            elif command == "changephone":
                result = change_contact(args, book, command="changephone")
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)
            elif command == "removephone":
                result = remove_phone(args, book, command="removephone")
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
            elif command == "showphone":
                console.print(show_phone(args, book, command="showphone"), style="green")
            elif command == "addbday":
                result = add_birthday(args, book, command="addbday")
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
            elif command == "showbday":
                console.print(show_birthday(args, book, command="showbday"), style="green")
            elif command == "editbday":
                result = edit_birthday(args, book, command="editbday")
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)
            elif command == "removebday":
                result = remove_birthday(args, book, command="removebday")
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
            elif command == "upcomingbdays":
                console.print(upcoming_birthdays(args, book, command="upcomingbdays"), style="green")
            elif command == "search":
                console.print(search_contacts(args, book, command="search"), style="green")
            elif command == "all":
                show_all_rich(book)
            elif command == "addemail":
                result = add_email(args, book, command="addemail")
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
            elif command == "editemail":
                result = edit_email(args, book, command="editemail")
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)
            elif command == "removeemail":
                result = remove_email(args, book, command="removeemail")
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
            elif command == "addnote":
                result = add_note(args, book, command="addnote")
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
            elif command == "editnote":
                result = edit_note(args, book, command="editnote")
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)
            elif command == "removenote":
                result = remove_note(args, book, command="removenote")
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
            elif command == "searchnote":
                console.print(search_note(args, book, command="searchnote"), style="green")
            elif command == "addtag":
                result = add_tag_to_note(args, book, command="addtag")
                console.print(result, style="green")
                save_address_book(book, filename)
            elif command == "removetag":
                result = remove_tag_from_note(args, book, command="removetag")
                console.print(result, style="green")
                save_address_book(book, filename)
            elif command == "searchtag":
                result = search_note_by_tag(args, book, command="searchtag")
                console.print(result, style="green")
            elif command == "sorttag":
                result = sort_note_by_tag(args, book, command="sorttag")
                console.print(result, style="green")
            elif command == "addaddress":
                result = add_address(args, book, command="addaddress")
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
            elif command == "editaddress":
                result = edit_address(args, book, command="editaddress")
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)
            elif command == "removeaddress":
                result = remove_address(args, book, command="removeaddress")
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
            elif command == "help":
                print_available_commands()
            else:
                console.print(suggest_command(command, valid_commands), style="yellow")
    except KeyboardInterrupt:
        console.print("\n👋 Good bye!", style="green")
        save_address_book(book, filename)
        console.print("📚 Address book saved successfully.", style="green")

if __name__ == "__main__":
    main()