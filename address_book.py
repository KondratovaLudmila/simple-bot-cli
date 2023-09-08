from collections import UserDict

class PhoneNotFoundError(Exception):
    pass

class NameExistsError(Exception):
    pass

class Field:
    def __init__(self, value, required=False):
        self.value = value
        self.required = required

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name: str, phone=""):
        self.name = Name(name, required=True)
        self.phones = []
        self.add_phone(phone)
        
    def get_phone(self, value: str) -> Phone:
        result = None
        for phone in self.phones:
            if phone.value == value:
                result = phone
                break
        
        return result

    def add_phone(self, phone: str):
        if phone:
            self.phones.append(Phone(phone))
        
    def del_phone(self, value: str):
        phone = self.get_phone(value)
        if phone:
            self.phones.remove(phone)
        else:
            raise PhoneNotFoundError

    def edit_phone(self, old_value: str, new_value: str):
        phone = self.get_phone(old_value)
        if phone:
            phone.value = new_value
        else:
            raise PhoneNotFoundError

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise NameExistsError
        self.data[record.name.value] = record
    
    def del_record(self, record: Record):
        return self.data.pop(record.name.value)
    
    def get_record(self, name: str) -> Record:
        return self.data[name]


    

    