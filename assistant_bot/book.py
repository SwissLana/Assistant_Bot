from collections import UserDict #Імпортуємо UserDict для створення адресної книги
from datetime import datetime, timedelta #Імпортуємо datetime та timedelta для роботи з датами
import re #Імпортуємо re для роботи з регулярними виразами

class Field:
    """Базовий клас для всіх полів контактів."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Клас для представлення імені з валідацією формату."""
    pass

class Phone(Field):
    """Клас для представлення телефонного номера з валідацією формату."""
    VALID_CODES = ["050", "066", "067", "068", "095", "096", "097", "098", "099", "063", "073", "093"]

    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("😓 Phone number must contain exactly 10 digits.")
        if not any(value.startswith(code) for code in self.VALID_CODES):
            raise ValueError(f"😓 The phone number must start with a valid code: {', '.join(self.VALID_CODES)}.")
        super().__init__(value)

class Birthday(Field):
    """Клас для представлення дати народження з валідацією формату."""
    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("😓 Invalid date format. Use DD.MM.YYYY")
        if birthday_date > datetime.today().date():
            raise ValueError("😓 Birthday cannot be in the future.")
        if birthday_date.year < 1930:
            raise ValueError("😓 Unrealistic birthday. Please try again.")
        super().__init__(value)

class Address(Field):
    """Клас для представлення адреси з валідацією формату."""
    pass

class Email(Field):
    """Клас для представлення електронної пошти з валідацією формату."""
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("😓 Invalid email format. Please use name@example.com")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, value) is not None

class Note(Field):
    """Клас для представлення нотатки з можливістю додавання тегів."""
    
    #Валідація тегів: 1-30 символів, лише літери, цифри та підкреслення
    TAG_PATTERN = re.compile(r"^[a-zA-Z0-9_]{1,30}$")
    
    # Конструктор для ініціалізації тексту нотатки та тегів
    def __init__(self, text, tags=None):
        self.text = text.strip()
        self.tags = set()
        for tag in (tags or []):
            self.add_tag(tag)

    # Метод для додавання тегу до нотатки
    def add_tag(self, tag):
        tag_clean = tag.lstrip("#").lower()
        if not self.TAG_PATTERN.fullmatch(tag_clean):
            raise ValueError(f"😓 Invalid tag: '{tag}'. Only letters, digits, and underscores are allowed (1–30 chars).")
        self.tags.add(tag_clean)

    # Метод для видалення тегу з нотатки
    def remove_tag(self, tag):
        self.tags.discard(tag.lstrip("#").lower())

    # Метод для перевірки наявності тегу в нотатці
    def has_tag(self, tag):
        return tag.lstrip("#").lower() in self.tags

    # Метод для виведення нотатки у вигляді рядка
    def __str__(self):
        tag_str = f" [#{', #'.join(sorted(self.tags))}]" if self.tags else ""
        return f"{self.text}{tag_str}"

    # Метод для порівняння двох нотаток
    def __eq__(self, other):
        return isinstance(other, Note) and self.text == other.text and self.tags == other.tags


class Record:
    """Клас для представлення запису в адресній книзі."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None
        self.notes = []
    

    def add_phone(self, phone, book):
        try:
            phone_obj = Phone(phone)
        except ValueError as e:
            return str(e)
        if any(p.value == phone for p in self.phones):
            return f"😓 The number '{phone}' already exists for this contact."
        for record in book.data.values():
            if record != self and any(p.value == phone for p in record.phones):
                return f"😓 The number '{phone}' already belongs to '{record.name.value}'."
        self.phones.append(phone_obj)
        return None

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return True
        return False

    def edit_phone(self, old_phone, new_phone, book):
        if not self.find_phone(old_phone):
            return f"😓 The old number '{old_phone}' was not found."
        try:
            new_phone_obj = Phone(new_phone)
        except ValueError as e:
            return str(e)
        for record in book.data.values():
            if record != self and any(p.value == new_phone for p in record.phones):
                return f"😓 The new number '{new_phone}' already belongs to '{record.name.value}'."
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = new_phone_obj
                return None
        return "😓 Something went wrong while updating the number."

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    def remove_birthday(self):
        self.birthday = None

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        if self.address:
            self.address.value = new_address
        else:
            self.add_address(new_address)

    def remove_address(self):
        self.address = None

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, new_email):
        if self.email:
            try:
                self.email = Email(new_email)
            except ValueError as e:
                return str(e)
        else:
            return "😓 Email is not set. Use 'addemail' to add one."

    def remove_email(self):
        self.email = None

    def add_note(self, text, tags=None):
        new_note = Note(text, tags)

        for existing_note in self.notes:
            if existing_note.text.strip().lower() == new_note.text.strip().lower():
                return None

        self.notes.append(new_note)
        return new_note

    def remove_note(self, text):
        normalized_input = re.sub(r"#\w+", "", text).strip().lower()
        for note in self.notes:
            if note.text.strip().lower() == normalized_input:
                self.notes.remove(note)
                return "✅ Note removed!"
        return "😓 Note not found."

    def edit_note(self, old_text, new_text):
        normalized_old = old_text.strip().lower()
        cleaned_new_text = re.sub(r"#\w+", "", new_text).strip()
        new_tags = re.findall(r"#(\w+)", new_text)

        for i, note in enumerate(self.notes):
            if note.text.strip().lower() == normalized_old:
                self.notes[i] = Note(cleaned_new_text, new_tags)
                return "✅ Note edited!"
        return "😓 Note not found."
    
    def get_notes_by_tag(self, tag):
        return [note for note in self.notes if note.has_tag(tag)]

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones) if self.phones else "No phone numbers available."
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        address_str = f", Address: {self.address}" if self.address else ""
        email_str = f", Email: {self.email}" if self.email else ""
        notes_str = f", Notes: {'; '.join(str(note) for note in self.notes)}" if self.notes else ""
        return f"👤 {self.name.value}: {phones_str}{birthday_str}{email_str}{address_str}{notes_str}"

class AddressBook(UserDict):
    """Клас для виведення адресної книги, що містить записи контактів."""
   
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        name = name.lower()
        for key, record in self.data.items():
            if key.lower() == name:
                return record
        return None

    def name_exists(self, name):
        return any(name.lower() == key.lower() for key in self.data)

    def delete(self, name):
        for key in list(self.data):
            if key.lower() == name.lower():
                del self.data[key]
                return True
        return False

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
    
    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        upcoming = []
        for record in self.data.values():
            if not record.birthday:
                continue
            try:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if today <= birthday_this_year <= end_date:
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() == 5:
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:
                        congratulation_date += timedelta(days=1)
                    upcoming.append(f"{record.name.value}: {congratulation_date.strftime('%d.%m.%Y')}")
            except ValueError:
                continue
        return upcoming


