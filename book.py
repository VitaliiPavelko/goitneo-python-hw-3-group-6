# pylint: disable=missing-docstring

import pickle

from fields import Record

class AddressBook():
    filepath = "./book.bin"

    def __init__(self):
        self.data = {}
        self.fh = open("./book.bin", "r+b")
        self.load_storage()

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
