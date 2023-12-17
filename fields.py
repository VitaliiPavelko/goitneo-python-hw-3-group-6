# pylint: disable=missing-docstring

from datetime import datetime
from re import match
from common import map_err_message

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    @map_err_message(ValueError, "Name must be at least 1 character long")
    def __init__(self, value):
        if len(value) < 1:
            raise ValueError()

        super().__init__(value)

class Phone(Field):
    @map_err_message(ValueError, "Invalid phone format. Expected: 10 digits")
    def __init__(self, value):
        if match(r"^\d{10}$", value) is None:
            raise ValueError()

        super().__init__(value)

class Birthday(Field):
    @map_err_message(ValueError, "Invalid birthday format. Expected: DD.MM.YYYY")
    def __init__(self, value):
        value = datetime.strptime(value, "%d.%m.%Y")
        super().__init__(value.date())

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def phones_str(self):
        return '\n'.join(f"- {p.value}" for p in self.phones)

    def __str__(self):
        name = self.name.value
        phones = self.phones_str()
        birthday_str = ''

        if self.birthday:
            birthday = str(self.birthday)
            birthday_str = f"birthday: {birthday}\n"


        return f"name: {name}\n{birthday_str}phones:\n{phones}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)

        if phone is None:
            raise ValueError("Phone not found")

        phone.value = new_phone
