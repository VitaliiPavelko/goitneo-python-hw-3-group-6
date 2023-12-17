# pylint: disable=missing-docstring

from book import AddressBook
from common import return_err_message, parse_input, validate_args_array
from fields import Record

@return_err_message
@validate_args_array("<username> <phone>")
def add_contact(args, book: AddressBook):
    name, phone = args
    record = Record(name)

    record.add_phone(phone)
    book.add_record(record)
    book.sync_storage()

    return "Contact added."

@return_err_message
@validate_args_array("<username> <birthday DD.MM.YYYY>")
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record: Record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found.")

    record.add_birthday(birthday)
    book.sync_storage()

    return "Birthday added."

@return_err_message
def show_birthdays(book: AddressBook):
    if book.is_empty():
        return "No contacts added."

    birthdays = book.get_birthdays_per_week()

    if not birthdays:
        return "No birthdays this week."

    result = ""

    for weekday, contacts in birthdays.items():
        people = "\n".join(F"- {contact}" for contact in contacts)
        result += f"{weekday}:\n{people}\n"

    return result


@return_err_message
@validate_args_array("<username>")
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)

    if not record:
        raise KeyError("Contact does not exist")

    if not record.birthday:
        return "Contact has no birthday"

    return str(record.birthday)

@return_err_message
@validate_args_array("<username> <old phone> <new phone>")
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record: Record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found.")

    record.edit_phone(old_phone, new_phone)
    book.sync_storage()

    return "Contact updated."


@return_err_message
@validate_args_array("<username>")
def show_phone(args, book: AddressBook):
    name, = args
    contact = book.find(name)

    if contact is None:
        raise KeyError("Contact does not exist")

    return contact.phones_str()

def show_all(book: AddressBook):
    if book.is_empty():
        return "No contacts added."

    return "\n\n".join([str(contact) for contact in book.iterate()])

@return_err_message
@validate_args_array("<username> <phone>")
def add_phone(args, book: AddressBook):
    name, phone = args
    record: Record = book.find(name)

    if record is None:
        raise KeyError(f"Contact {name} not found.")

    record.add_phone(phone)
    book.sync_storage()

    return "Phone added."

def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")

    while True:
        command_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(command_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        output = "Invalid command."

        if command == "add":
            output = add_contact(args, book)
        if command == "add-phone":
            output = add_phone(args, book)
        elif command == "change":
            output = change_contact(args, book)
        elif command == "add-birthday":
            output = add_birthday(args, book)
        elif command == "show-birthday":
            output = show_birthday(args, book)
        elif command == "birthdays":
            output = show_birthdays(book)
        elif command == "phone":
            output = show_phone(args, book)
        elif command == "all":
            output = show_all(book)
        elif command == "hello":
            output = "How can I help you?"

        print(output)


if __name__ == "__main__":
    main()
