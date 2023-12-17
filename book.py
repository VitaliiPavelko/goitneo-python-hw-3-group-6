# pylint: disable=missing-docstring
import pickle

from collections import defaultdict
from datetime import datetime, timedelta
from fields import Record

class AddressBook():
    __FILEPATH = "./book.bin"

    __CONGRATULATION_WEEKDAYS = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ]

    def get_birthdays_per_week(self):
        contacts = self.data.values()

        start_date = datetime.today().date()
        offset_days = 5 - start_date.weekday() - 1

        if start_date.weekday() == 0:
            start_date = start_date - timedelta(days=2)
            offset_days = 6

        if start_date.weekday() in [5, 6]:
            offset_days = 5 + 6 - start_date.weekday()

        finish_date = start_date + timedelta(days=offset_days)
        result = defaultdict(list)

        for contact in contacts:
            birthday_date = contact.birthday.value
            birhtday_this_year = birthday_date.replace(year=start_date.year)

            if start_date <= birhtday_this_year <= finish_date:
                weekday = 0

                if birhtday_this_year.weekday() not in [5, 6]:
                    weekday = birthday_date.weekday()

                result[weekday].append(contact.name.value)

        rv = {}

        for index, weekday in list(enumerate(self.__CONGRATULATION_WEEKDAYS)):
            if len(result[index]):
                rv[weekday] = result[index]

        return rv

    def __init__(self):
        self.data = {}

        try:
            self.fh = open(AddressBook.__FILEPATH, "r+b")
            self.load_storage()
        except FileNotFoundError:
            self.fh = open(AddressBook.__FILEPATH, 'w+b')

    def is_empty(self):
        return len(self.data) == 0

    def __del__(self):
        self.fh.close()

    def load_storage(self):
        self.fh.seek(0)
        dump = self.fh.read()

        if len(dump):
            st = pickle.loads(dump)
            self.data = st

    def sync_storage(self):
        self.fh.seek(0)
        self.fh.truncate(0)
        dump = pickle.dumps(self.data)
        self.fh.write(dump)


    def add_record(self, record: Record):
        name = record.name.value
        self.data[name] = record


    def iterate(self):
        for record in self.data.values():
            yield record


    def find(self, name):
        if name not in self.data:
            return None

        return self.data[name]


    def delete(self, name):
        if name not in self.data:
            return None

        self.data.pop(name)
