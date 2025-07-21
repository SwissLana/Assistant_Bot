import pickle # Імпортуємо pickle для серіалізації та десеріалізації об'єктів
import os # Імпортуємо os для роботи з файловою системою
from .book import AddressBook # Імпортуємо AddressBook з book.py для роботи з адресною книгою

DEFAULT_FILENAME = "address_book.pkl"

def save_address_book(book, filename=DEFAULT_FILENAME):
    try:
        with open(filename, "wb") as file:
            pickle.dump(book, file)
    except Exception as e:
        console.print(f"😓 Error saving address book to '{filename}': {e}", style="red")

def load_address_book(filename=DEFAULT_FILENAME):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as file:
                book = pickle.load(file)
                for record in book.values():
                    if not hasattr(record, "address"):
                        record.address = None
                    if not hasattr(record, "email"):
                        record.email = None
                    if not hasattr(record, "notes"):
                        record.notes = []
                return book
        except Exception as e:
            console.print(f"😓 Error loading address book from '{filename}': {e}", style="red")
            console.print("Creating a new empty address book instead.", style="yellow")
            return AddressBook()
    return AddressBook()

