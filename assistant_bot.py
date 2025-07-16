from collections import UserDict # Імпортуємо UserDict для створення адресної книги
from datetime import datetime, timedelta # Імпортуємо datetime для роботи з датами
import pickle # Імпортуємо pickle для серіалізації та десеріалізації даних
import os # Імпортуємо os для перевірки наявності файлу
import re # Імпортуємо re для роботи з регулярними виразами (для перевірки email)
from rich.console import Console # Імпортуємо rich для красивого виведення тексту
from rich.table import Table # Імпортуємо rich для красивого виведення таблиць
import difflib # Імпортуємо difflib для пошуку схожих команд

console = Console()

def show_all_rich(book):
    if not book.data:
        return "No contacts saved."

    # Створюємо таблицю з заголовками
    table = Table(title="Available Contacts", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Phone", style="magenta")
    table.add_column("Birthday", style="green")
    table.add_column("Address", style="yellow")
    table.add_column("Email", style="blue")
    table.add_column("Notes", style="white")

    for _, record in sorted(book.data.items(), key=lambda item: item[0].lower()):
        name = record.name.value
        phones = ", ".join(phone.value for phone in record.phones)
        birthday = record.birthday.value if record.birthday else ""
        address = record.address.value if record.address else ""
        email = record.email.value if record.email else ""
        notes = " | ".join(record.notes) if record.notes else ""

        table.add_row(name, phones, birthday, address, email, notes)

    console.print(table)
    return ""

# Файл для збереження
DEFAULT_FILENAME = "address_book.pkl"

# Базовий клас для всіх полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Клас для імені контакту
class Name(Field):
    pass


# Клас для телефонного номера
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


# Клас для дати народження
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        if birthday_date > datetime.today().date():
            raise ValueError("Birthday cannot be in the future.")
        if birthday_date.year < 1930:
            raise ValueError("Unrealistic birthday. Please try again.")

        super().__init__(value)


class Address(Field):
    pass


class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email format. Please use name@example.com")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, value) is not None


class Note(Field):
    pass


# Клас для запису контакту
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None
        self.notes = []

    # Метод для додавання телефону
    def add_phone(self, phone):
        if self.find_phone(phone):
            return False
        try:
            self.phones.append(Phone(phone))
        except ValueError:
            return False
        return True

    # Метод для видалення телефону
    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return True
        return False

    # Метод для редагування телефону
    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            try:
                self.phones.remove(phone_obj)
                self.phones.append(Phone(new_phone))
                return True
            except ValueError:
                return False
        return False

    # Метод для пошуку телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    # Метод для додавання дати народження
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    # Метод для редагування дати народження
    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    # Метод для видалення дати народження
    # Якщо дата народження не встановлена, нічого не робимо
    def remove_birthday(self):
        self.birthday = None

    # Метод для додавання адреси
    def add_address(self, address):
        self.address = Address(address)
    
    # Метод для редагування адреси  
    def edit_address(self, new_address):
        if self.address:
            self.address.value = new_address
        else:
            self.add_address(new_address)
    
    # Метод для видалення адреси
    def remove_address(self):
        self.address = None
        
    # Метод для додавання email
    def add_email(self, email):
        self.email = Email(email)
        
     
    # Метод для редагування email   
    def edit_email(self, new_email):
        if self.email:
            try:
                self.email = Email(new_email)
            except ValueError as e:
                return str(e)
        else:
            return "Email not set. Use 'addemail' to add a new email."
    
    # Метод для видалення email
    def remove_email(self):
        self.email = None
        
        
    # Метод для додавання нотаток
    # Нотатки зберігаються у списку, кожна нотатка — це об'єкт класу Note
    # Нотатки можуть бути будь-якого типу, але зберігаються як рядки
    # Якщо нотатка вже існує, вона не додається
    
    def add_note(self, note):
        self.notes.append(note)

    def remove_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            return True
        return False

    def edit_note(self, old_note, new_note):
        if old_note in self.notes:
            index = self.notes.index(old_note)
            self.notes[index] = new_note
            return True
        return False

    # Метод для виведення інформації про контакт
    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if hasattr(self, 'birthday') and self.birthday else ""
        address_str = f", Address: {self.address}" if hasattr(self, 'address') and self.address else ""
        email_str = f", Email: {self.email}" if hasattr(self, 'email') and self.email else ""
        notes_str = f", Notes: {'; '.join(self.notes)}" if hasattr(self, 'notes') and self.notes else ""
        return f"{self.name.value}: {phones_str}{birthday_str}{email_str}{address_str}{notes_str}"
        


# Клас для адресної книги, що наслідує UserDict
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    # Метод для пошуку контакту за іменем
    def find(self, name):
        name = name.lower()
        for key, record in self.data.items():
            if key.lower() == name:
                return record
        return None
    
    # Метод для перевірки наявності контакту за іменем
    def name_exists(self, name):
        return any(name.lower() == key.lower() for key in self.data)
    
    # Метод для видалення контакту за іменем
    def delete(self, name):
        for key in list(self.data):
            if key.lower() == name.lower():
                del self.data[key]
                return True
        return False
    
    # Метод для пошуку контактів за іменем або телефоном
    def search(self, query):
        result = []
        query = query.lower()

        for record in self.data.values():
            name_match = query in record.name.value.lower()
            phone_match = any(query in phone.value for phone in record.phones)
            email_match = record.email and query in record.email.value.lower()
            address_match = record.address and query in record.address.value.lower()
            birthday_match = record.birthday and query in record.birthday.value.lower()

            if name_match or phone_match or email_match or address_match or birthday_match:
                result.append(str(record))

        return result
    
    # Метод для отримання майбутніх днів народження
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue
            try:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_date: # Перевіряємо, чи день народження в межах наступних 7 днів
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() == 5:  # Субота
                        # Якщо день народження припадає на суботу, переносимо на понеділок
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:  # Неділя
                        # Якщо день народження припадає на неділю, переносимо на понеділок
                        congratulation_date += timedelta(days=1)

                    upcoming.append(f"{record.name.value}: {congratulation_date.strftime('%d.%m.%Y')}")
            except ValueError:
                continue

        return upcoming



# Збереження та завантаження

# Функція для збереження адресної книги у файл
def save_address_book(book, filename=DEFAULT_FILENAME):
    try:
        with open(filename, "wb") as file:
            pickle.dump(book, file)
    except Exception as e:
        print(f"Error saving address book to '{filename}': {e}")

# Функція для завантаження адресної книги з файлу
def load_address_book(filename=DEFAULT_FILENAME):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as file:
                book = pickle.load(file)
                # Оновлюємо всі старі записи, які могли бути без нових полів
                for record in book.values():
                    if not hasattr(record, "address"):
                        record.address = None
                    if not hasattr(record, "email"):
                        record.email = None
                    if not hasattr(record, "notes"):
                        record.notes = []
                return book
        except Exception as e:
            print(f"Error while loading address book from '{filename}': {e}")
            print("Creating a new empty address book instead.")
            return AddressBook()
    return AddressBook()


# Функція для розбору введення користувача
def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.strip().lower(), args


# Функція для нормалізації імені контакту
def normalize_name(name):
    def fix_part(part):
        return "-".join(subpart.capitalize() for subpart in part.split("-"))

    return " ".join(fix_part(word) for word in name.strip().split())


# Декоратор для обробки помилок введення, які можуть виникнути під час виконання функцій
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Missing input. Please provide valid arguments."
    return inner


# Декоратор для обробки помилок введення
@input_error
def add_contact(args, book): # Функція для додавання нового контакту
    if len(args) < 2:
        raise ValueError("Please enter name and at least one phone number.")

    # Шукаємо перший телефон — число з 10 цифрами
    phone_start_index = None
    for i, arg in enumerate(args):
        if arg.isdigit() and len(arg) == 10:
            phone_start_index = i
            break

    if phone_start_index is None: # Якщо не знайдено жодного телефону з 10 цифрами
        raise ValueError("At least one valid phone number required (10 digits).")

    name_parts = args[:phone_start_index]
    phones = args[phone_start_index:]

    if not name_parts: # Якщо ім'я не вказано
        raise ValueError("Name is missing.")

    name = normalize_name(" ".join(name_parts))

    if book.name_exists(name):
        return "Contact with this name already exists."

    record = Record(name)

    for phone in phones:
        try:
            if not record.add_phone(phone):
                return f"Phone number '{phone}' already exists."
        except ValueError:
            return f"Invalid phone number '{phone}'. Must contain exactly 10 digits."

    book.add_record(record)
    return "Contact added."


@input_error
def edit_contact_name(args, book): # Функція для зміни імені контакту
    if len(args) < 2:
        raise ValueError("Please provide old and new full names.")

    # Знаходимо позицію першого імені, що вже є в книзі
    for i in range(1, len(args)):
        old_name_try = normalize_name(" ".join(args[:i]))
        if book.name_exists(old_name_try):
            old_name = old_name_try
            new_name = normalize_name(" ".join(args[i:]))
            break
    else:
        raise KeyError("Contact not found.")

    record = book.find(old_name)
    book.delete(old_name)
    record.name = Name(new_name)
    book.add_record(record)

    return f"Contact name changed to '{new_name}'."


@input_error
def change_contact(args, book): # Функція для зміни телефону контакту
    if len(args) < 3:
        raise ValueError("Please provide full name, old phone, and new phone.")
    
    old_phone = args[-2]
    new_phone = args[-1]

    if not (old_phone.isdigit() and len(old_phone) == 10):
        raise ValueError("Old phone number must be 10 digits.")
    if not (new_phone.isdigit() and len(new_phone) == 10):
        raise ValueError("New phone number must be 10 digits.")

    name = normalize_name(" ".join(args[:-2]))

    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")

    if not record.edit_phone(old_phone, new_phone):
        return f"Old phone number '{old_phone}' not found or new number invalid."

    return "Phone number updated."


@input_error
def add_phone_to_contact(args, book): # Функція для додавання телефону до контакту
    if len(args) < 2:
        raise ValueError("Please provide name and phone number to add.")
    
    possible_phone = args[-1] # Останній аргумент вважаємо телефоном
    if not possible_phone.isdigit() or len(possible_phone) != 10:
        raise ValueError("Please provide a valid phone number (10 digits).")

    name = normalize_name(" ".join(args[:-1])) # Все, що перед останнім аргументом, вважаємо іменем
    phone = possible_phone

    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")

    if record.add_phone(phone):
        return "Phone number added."
    else:
        return f"Phone number '{phone}' already exists for this contact."


@input_error
def remove_phone(args, book): # Функція для видалення телефону з контакту
    if len(args) < 2:
        raise ValueError("Please provide full name and phone number to remove.")
    
    possible_phone = args[-1]
    if not possible_phone.isdigit() or len(possible_phone) != 10:
        raise ValueError("Please provide a valid phone number (10 digits).")

    name = normalize_name(" ".join(args[:-1]))
    phone = possible_phone
    
    record = book.find(name)
    if not record:
        raise KeyError
    
    if not record.remove_phone(phone):
        return f"Phone number '{phone}' not found for this contact."

    return "Phone number removed."


@input_error
def remove_contact(args, book): # Функція для видалення контакту
    if not args:
        raise ValueError("Please provide the contact name to remove.")
    
    name = normalize_name(" ".join(args))
    
    if not book.delete(name):
        raise KeyError("Contact not found.")
    
    return f"Contact '{name}' removed."


@input_error
def add_birthday(args, book): # Функція для додавання дати народження до контакту
    if len(args) < 2:
        raise ValueError("Please provide name and birthday (DD.MM.YYYY).")
    
    name = normalize_name(" ".join(args[:-1]))
    birthday = args[-1]
    
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        return "Invalid or missing date. Use format DD.MM.YYYY."

    record = book.find(name)
    if not record:
        return "Contact not found. Please provide full name."

    if record.birthday:
        return "Birthday already exists. Use 'editbday' to change it."

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book): # Функція для показу дати народження контакту
    if not args:
        raise ValueError("Please provide the contact name.")
    
    name = normalize_name(" ".join(args))
     # Знаходимо всі потенційні збіги
    matches = [record for key, record in book.data.items() if name.lower() in key.lower()]

    if not matches:
        raise KeyError("Contact not found.")

    # Якщо один збіг — повертаємо одразу
    if len(matches) == 1:
        record = matches[0]
        if record.birthday:
            return f"{record.name.value}'s birthday is {record.birthday.value}"
        else:
            return "Birthday is not set for this contact."

    # Якщо знайдено кілька контактів з заданим ім’ям
    matches_with_birthday = [r for r in matches if r.birthday]

    if not matches_with_birthday:
        return "None of the matching contacts have a birthday set."

    # Якщо знайдено кілька контактів з днем народження
    result = ["Found multiple contacts:"]
    result += [f"{record.name.value}: {record.birthday.value}" for record in matches]
    result.append("Please enter the full name to get an exact match.")
    return "\n".join(result)


@input_error
def edit_birthday(args, book): # Функція для редагування дати народження контакту
    if len(args) < 2:
        raise ValueError("Please provide name and new birthday (DD.MM.YYYY).")
    name = normalize_name(" ".join(args[:-1]))
    birthday = args[-1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_birthday(birthday)
    return "Birthday updated."


@input_error
def remove_birthday(args, book): # Функція для видалення дати народження контакту
    if not args:
        raise ValueError("Please provide name to remove birthday.")
    name = normalize_name(" ".join(args))
    record = book.find(name)
    if not record:
        raise KeyError
    record.remove_birthday()
    return "Birthday removed."


@input_error
def show_phone(args, book): # Функція для показу телефону контакту
    if not args:
        raise ValueError("Please provide the contact name.")

    name = normalize_name(" ".join(args))
    
     # Знаходимо всі потенційні збіги
    matches = [record for key, record in book.data.items() if name.lower() in key.lower()]

    if not matches:
        raise KeyError

    # Якщо один збіг — повертаємо одразу
    if len(matches) == 1:
        return str(matches[0])

    # Якщо кілька — повертаємо всі
    result = ["Found multiple contacts:"]
    result += [f"{str(r)}" for r in matches]
    return "\n".join(result)

@input_error
def search_contacts(args, book): # Функція для пошуку контактів за іменем або телефоном
    if not args:
        return "Please enter a name, phone, email, address or birthday to search."

    query = args[0].lower()

    if query in ["note", "notes"]:
        return "To search notes, use: searchnote <keyword>"
    if query in ["email"]:
        return "Try searching with a correct email or part of it (e.g. gmail)"
    if query in ["address"]:
        return "Try searching with a keyword from the address."
    if query in ["birthday", "bday", "birth"]:
        return "Use a real date, like 03.11.1991 or part of it."

    results = book.search(query)
    return "\n".join(results) if results else "No matching input found. Use correct format for search."


# Функція для отримання майбутніх днів народження
def upcoming_birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    return "\n".join(upcoming) if upcoming else "No upcoming birthdays in the next 7 days."


@input_error
def add_address(args, book): # Функція для додавання адреси до контакту
    if len(args) < 2:
        raise ValueError("Please provide name and address.")
    
    # Шукаємо ім’я з початку, що точно існує в книзі
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            address = " ".join(args[i:]).title()  # решта аргументів — адреса
            break
    else:
        return ("Contact not found.")

    record = book.find(name)
    if record.address:
        return "Address already exists. Use 'editaddress' to change it."
    record.add_address(address)
    return "Address added."


@input_error
def edit_address(args, book): # Функція для редагування адреси контакту
    if len(args) < 2:
        raise ValueError("Please provide full name and new address.")

    # Знайти ім’я, яке є в адресній книзі
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            new_address = " ".join(args[i:]).title()
            break
    else:
        return ("Contact not found. Try with full name.")

    record = book.find(name)
    record.edit_address(new_address)
    return "Address updated."


@input_error
def remove_address(args, book): # Функція для видалення адреси контакту
    if not args:
        raise ValueError("Please provide name to remove address.")
    
    name = normalize_name(" ".join(args))
    record = book.find(name)
    if not record:
        return "Contact not found. Please provide a valid or full name."
    if not record.address:
        return "Address is not set."
    record.remove_address()
    return "Address removed."



@input_error
def add_email(args, book): # Функція для додавання email до контакту
    if len(args) < 2:
        raise ValueError("Please provide name and email.")
    
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            email = " ".join(args[i:])  # дозволяє email з пробілами, якщо є помилки у введенні
            break
    else:
        return("Contact not found. Try with full name.")

    record = book.find(name)
    if record.email:
        return "Email already exists. Use 'editemail' to change it."
    record.add_email(email)
    return "Email added."


@input_error
def edit_email(args, book): # Функція для редагування email контакту
    if len(args) < 2:
        raise ValueError("Please provide name and new email.")
    
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            new_email = " ".join(args[i:])
            break
    else:
        return("Contact not found. Try with full name.")

    record = book.find(name)
    record.edit_email(new_email)
    return "Email updated."

@input_error
def remove_email(args, book): # Функція для видалення email контакту
    if not args:
        raise ValueError("Please provide name to remove email.")
    
    name = normalize_name(" ".join(args))
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.email:
        return "Email is not set."
    record.remove_email()
    return "Email removed."


@input_error
def add_note(args, book):
    if len(args) < 2:
        return "Please provide name and note text."
    
    # Шукаємо ім’я з початку, що точно існує в книзі
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            note_text = " ".join(args[i:])
            break
    else:
        return "Contact not found. Please provide full name."
    record = book.find(name)
    
    # Перевіряємо, чи нотатка вже існує
    if note_text in record.notes:
        return "Note already exists."
    
    record.add_note(note_text)
    return "Note added."


@input_error
def edit_note(args, book):
    if len(args) < 3:
        return "Please provide name, old note, and new note."
    
    for i in range(1, len(args) - 1):  # мінімум 1 слово для old, 1 для new
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            record = book.find(name)

            # розбиваємо на old_note і new_note
            for j in range(i + 1, len(args) - 1):
                old_note = " ".join(args[i:j])
                new_note = " ".join(args[j:])
                if old_note in record.notes:
                    if record.edit_note(old_note, new_note):
                        return "Note updated."
            return "Old note not found."

    return "Contact not found. Please provide full name."


@input_error
def remove_note(args, book):
    if len(args) < 2:
        return "Please provide full name and note to remove."
    
    # Пробуємо знайти ім’я
    for i in range(1, len(args)):
        possible_name = normalize_name(" ".join(args[:i]))
        if book.name_exists(possible_name):
            name = possible_name
            note_text = " ".join(args[i:]).strip()
            if not note_text:
                return "Please provide full name and note to remove."
            record = book.find(name)
            if record.remove_note(note_text):
                return "Note removed."
            else:
                return "Note not found."
    
    # Якщо не знайшли ім’я
    return "Please provide full name and note to remove."


@input_error
def search_note(args, book):
    if not args:
        return "Please provide a keyword to search in notes."
    
    query = " ".join(args).lower()
    matches = []

    for record in book.values():
        for note in record.notes:
            if query in note.lower():
                matches.append(f"{record.name.value}: {note}")
                break  # одна відповідність достатня для одного запису

    return "\n".join(matches) if matches else "No notes matching your query were found."


# Функція для показу всіх контактів у алфавітному порядку
def show_all(book):
    if not book.data:
        return "No contacts saved."
    
    # Сортування контактів за іменем (незалежно від регістру)
    sorted_records = sorted(book.data.items(), key=lambda item: item[0].lower())
    return "\n".join(str(record) for _, record in sorted_records)


# Функція для виведення доступних команд
def print_available_commands():
    command_groups = {
        "General": ["hello", "help", "exit", "close"],
        "Contacts": ["addcontact", "editname", "removecontact", "search", "all"],
        "Phones": ["addphone", "changephone", "removephone", "showphone", "search"],
        "Birthdays": ["addbday", "showbday", "editbday", "removebday", "search", "upcomingbdays"],
        "Emails": ["addemail", "editemail", "removeemail", "search"],
        "Addresses": ["addaddress", "editaddress", "removeaddress", "search"],
        "Notes": ["addnote", "editnote", "removenote", "searchnote"]
    }

    table = Table(title="Available Commands", show_header=True, header_style="bold green")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Commands", style="magenta")

    for category, commands in command_groups.items():
        command_list = ", ".join(commands)
        table.add_row(category, command_list)

    console.print(table)
 
 
AVAILABLE_COMMANDS = [
    "hello", "help", "exit", "close",
    "addcontact", "editname", "removecontact", "search", "all",
    "addphone", "changephone", "removephone", "showphone",
    "addbday", "showbday", "editbday", "removebday", "upcomingbdays",
    "addemail", "editemail", "removeemail",
    "addaddress", "editaddress", "removeaddress",
    "addnote", "editnote", "removenote", "searchnote"
]

# Функція для пропозиції команди на основі введення користувача 
def suggest_command(raw_input: str):
    parts = raw_input.strip().split()
    joined = "".join(parts).lower()
    first = parts[0].lower() if parts else ""

    candidates = set([first, joined])
    matches = []
    for candidate in candidates:
        matches += difflib.get_close_matches(candidate, AVAILABLE_COMMANDS, n=1, cutoff=0.6)

    return matches[0] if matches else None
    

# Головна функція для запуску бота
# Після всіх функцій, які змінюють адресну книгу -->
# (результат містить “added”, “removed”, “updated”) виконується автозбереження.
# Файл .pkl буде оновлюватися відразу після кожної операції.
def main():
    filename = DEFAULT_FILENAME
    book = load_address_book(filename)
    console.print(("Welcome to the assistant bot!"), style="green")
    console.print(("Type 'help' to see available commands."), style="green")
    try:
        while True:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                continue

            command, args = parse_input(user_input)

            if command in ["exit", "close"]:
                save_address_book(book, filename)
                console.print(("Good bye!"), style="green")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "addcontact":
                result = add_contact(args, book)
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
                    
            elif command == "editname":
                result = edit_contact_name(args, book)
                console.print(result, style="green")
                if "changed" in result.lower():
                    save_address_book(book, filename)
                
            elif command == "removecontact":
                result = remove_contact(args, book)
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)

            elif command == "addphone":
                result = add_phone_to_contact(args, book)
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)

            elif command == "changephone":
                result = change_contact(args, book)
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)

            elif command == "removephone":
                result = remove_phone(args, book)
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
                    
            elif command == "showphone":
                console.print(show_phone(args, book), style="green")

            elif command == "addbday":
                result = add_birthday(args, book)
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
                    
            elif command == "showbday":
                result = show_birthday(args, book)
                console.print(result, style="green")

            elif command == "editbday":
                result = edit_birthday(args, book)
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)

            elif command == "removebday":
                result = remove_birthday(args, book)
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)

            elif command == "upcomingbdays":
                console.print(upcoming_birthdays(book), style="green")

            elif command == "search":
                console.print(search_contacts(args, book), style="green")

            elif command == "all":
                show_all_rich(book)

            elif command == "addemail":
                result = add_email(args, book)
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)

            elif command == "editemail":
                result = edit_email(args, book)
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)

            elif command == "removeemail":
                result = remove_email(args, book)
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)

            elif command == "addnote":
                result = add_note(args, book)
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)

            elif command == "editnote":
                result = edit_note(args, book)
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)

            elif command == "removenote":
                result = remove_note(args, book)
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)

            elif command == "searchnote":
                console.print(search_note(args, book), style="green")
                
            elif command == "addaddress":
                result = add_address(args, book)
                console.print(result, style="green")
                if "added" in result.lower():
                    save_address_book(book, filename)
                    
            elif command == "editaddress":
                result = edit_address(args, book)
                console.print(result, style="green")
                if "updated" in result.lower():
                    save_address_book(book, filename)
                    
            elif command == "removeaddress":
                result = remove_address(args, book)
                console.print(result, style="green")
                if "removed" in result.lower():
                    save_address_book(book, filename)
                
            elif command == "help":
                print_available_commands()
                
            else:
                suggested = suggest_command(user_input)
                if suggested:
                    console.print(f"Did you mean: [bold yellow]{suggested}[/]?", style="red")  
                else:
                    console.print(f"Unknown command '{command}'.", style="red")
                print_available_commands()
                
    except KeyboardInterrupt: # Збереження без явного виходу з програми (exit, close)
        print("\nGood bye!")
        save_address_book(book, filename)
        print("Address book saved successfully.")


if __name__ == "__main__":
    main()