from collections import UserDict

class Field:
    def __init__(self, value, required=False):
        self.value = value
        self.required = required

class Name(Field):
    pass

class Phone(Field):
    def __setattr__(self, key: str, value: str) -> None:
        if key == 'value' and not self.is_valid_phone(value):
            raise ValueError("Phone must contain 10 digits")
        return super().__setattr__(key, value)
    
    def __str__(self):
        return str(self.value)
    
    def is_valid_phone(self, phone: str) -> bool:
        is_valid = phone.isdigit() and len(phone) == 10

        return is_valid

class Record:
    def __init__(self, name: str, phone=""):
        self.name = Name(name, required=True)
        self.phones = []
        self.add_phone(phone)

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        
    def find_phone(self, value: str) -> Phone:
        result = None
        for phone in self.phones:
            if phone.value == value:
                result = phone
                break
        
        if not result:
            raise ValueError("Phone not found")
        return result

    def add_phone(self, phone: str) -> None:
        if phone:
            self.phones.append(Phone(phone))
        
    def remove_phone(self, value: str) -> None:
        phone = self.find_phone(value)
        if phone:
            self.phones.remove(phone)
        

    def edit_phone(self, old_value: str, new_value: str) -> None:
        phone = self.find_phone(old_value)
        if phone:
            phone.value = new_value

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        if record.name.value in self.data:
            raise ValueError(f"Record with name {record.name.value} is already exists")
        self.data[record.name.value] = record
    
    def delete(self, name: str) -> Record:
        if name in self.data:
            return self.data.pop(name)

    def find(self, name: str) -> list:
        return self.data.get(name)

