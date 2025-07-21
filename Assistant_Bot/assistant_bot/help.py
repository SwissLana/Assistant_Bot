from rich.console import Console
from rich.table import Table

console = Console()

def print_available_commands():
    command_groups = {
        "General": ["hello", "help", "exit", "close"],
        "Contacts": ["addcontact", "editname", "removecontact", "search", "all"],
        "Phones": ["addphone", "changephone", "removephone", "showphone", "search"],
        "Birthdays": ["addbday", "showbday", "editbday", "removebday", "search", "upcomingbdays"],
        "Email": ["addemail", "editemail", "removeemail", "search"],
        "Address": ["addaddress", "editaddress", "removeaddress", "search"],
        "Notes": ["addnote", "editnote", "removenote", "searchnote", "addtag", "removetag", "searchtag", "sorttag"]
    }
    table = Table(title="📋 Available Commands", show_header=True, header_style="bold green")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Commands", style="magenta")
    for category, commands in command_groups.items():
        command_list = ", ".join(commands)
        table.add_row(category, command_list)
    console.print(table)

