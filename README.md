# 🧠 Assistant Bot (Console Version)

An intelligent and user-friendly console assistant bot written in Python.  
Manage your **contacts**, **phones**, **birthdays**, **emails**, **addresses**, and **tagged notes** — all from your terminal, with rich visual output!

## 🚀 Features

- 📇 Contact management (add/edit/remove/search)
- 📞 Phone number validation & deduplication
- 🎂 Birthday tracking + upcoming birthday reminders
- 📬 Email with validation
- 🏠 Address handling with formatting
- 📝 Notes with tags (add/edit/remove/search/sort)
- 🔍 Search contacts by any field
- 🧠 Intelligent command suggestions
- 💾 Persistent storage with `pickle`
- 🎨 Beautiful console output using [rich]

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SwissLana/assistant_bot.git
   cd assistant_bot
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python3 -m assistant_bot.main
   ```

## ✅ Available Commands

Here are some example commands you can use:

| Category           | Command Example                                                    |
|--------------------|--------------------------------------------------------------------|
| Greeting           | `hello`                                                            |
| Exit               | `exit`, `close`                                                    |
| Help               | `help`                                                             |
| Add Contact        | `addcontact Ivan 0987654321 ivan@example.com vul. Parkova 1, Kyiv` |
| Edit Name          | `editname Ivan Ivan Petrov`                                        |
| Remove Contact     | `remove Ivan`                                                      |
| Add Phone          | `addphone Ivan 0671234567`                                         |
| Change Phone       | `changephone Ivan 0987654321 0661112222`                           |
| Remove Phone       | `removephone Ivan 0671234567`                                      |
| Show Phone         | `showphone Ivan`                                                   |
| Add Birthday       | `addbday Ivan 15.05.1990`                                          |
| Edit Birthday      | `editbday Ivan 16.05.1990`                                         |
| Show Birthday      | `showbday Ivan`                                                    |
| Remove Birthday    | `removebday Ivan`                                                  |
| Upcoming Birthdays | `upcomingbdays`                                                    |
| Add Email          | `addemail Ivan ivan@example.com`                                   |
| Edit Email         | `editemail Ivan new@example.com`                                   |
| Remove Email       | `editemail Ivan`                                                   |
| Add Address        | `addaddress Ivan vul. Vilna 3, Kyiv`                               |
| Edit Address       | `editaddress Ivan vul. New 5, Kyiv`                                |
| Remove Address     | `removeaddress Ivan`                                               |
| Add Note           | `addnote Ivan Meeting at 3PM #urgent #work`                        |
| Edit Note          | `editnote Ivan Meeting at 3PM Rescheduled to 4PM #urgent`          |
| Remove Note        | `removenote Ivan Meeting at 3PM`                                   |
| Add Tag            | `addtag Ivan Meeting at 3PM #reminder`                             |
| Remove Tag         | `removetag Ivan Meeting at 3PM #urgent`                            |
| Search Notes       | `searchnote meeting`                                               |
| Search by Tag      | `searchtag #urgent`                                                |
| Sort Notes by Tag  | `sorttag`                                                          |
| Show All Contacts  | `all`                                                              |
| Search             | `search Ivan` or `search 0671234567` or `search 15.05.1990`        |
|                    | `search Vilna` or `search ivan@example.com`                        |

> 🧠 The assistant provides suggestions if you mistype a command.

## 💾 Data Persistence

- Data is automatically saved to `address_book.pkl` on every update.
- If the file doesn't exist, a new address book is created.

## 🧪 Requirements

- Python 3.8+
- `rich`

Install with:
```bash
pip install rich
```

## 📁 Project Structure

```
assistant_bot/                 # Main package
│
├── __init__.py                # Package initializer
├── main.py                    # Entry point (main loop)
├── book.py                    # Core classes (Record, AddressBook, etc.)
├── commands.py                # Command parsing and logic
├── decorators.py              # Error handling decorators
├── display.py                 # Output formatting (with Rich)
├── help.py                    # Help command descriptions
├── storage.py                 # Data persistence (save/load)
├── utils.py                   # Utility functions
│
├── address_book.pkl           # Data file (auto-generated on save)
├── requirements.txt           # Required packages
└── README.md                  # Project documentation
```

## 📌 Notes

- Phone numbers must be 10 digits and start with allowed codes (e.g., 067, 050, etc.).
- Email addresses are validated.
- Notes support tags with `#`, which can be searched and sorted.

## 📜 License

MIT License – free to use, modify, and share.