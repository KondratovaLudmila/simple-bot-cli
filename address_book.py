from collections import UserDict
from datetime import datetime

DATE_FORMAT = "%d.%m.%Y"

class Field:
    def __init__(self, value, required=False):
        self.required = required
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    

class Name(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if self.required and not new_value:
            raise ValueError("Required field can not be empty!")
        else:
            self._value = new_value

class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            self._value = new_value
        else:
            raise ValueError("Phone must contain 10 digits")

    def __str__(self):
        return str(self.value)
    
    def is_valid_phone(self, phone: str) -> bool:
        is_valid = phone.isdigit() and len(phone) == 10
        return is_valid

class Birthday(Field):
    def __str__(self):
        if self.value:
            return datetime.strftime(self.value, DATE_FORMAT)
        else:
            return ""

    @Field.value.setter
    def value(self, new_value: str):
        date_value = datetime.strptime(new_value, DATE_FORMAT).date()
        if date_value > datetime.now().date():
            raise ValueError("Date of birth can not be in the future!")
        else:
            self._value = date_value

class Record:
    def __init__(self, name: str, phone=None, birthday=None):
        self.name = Name(name, required=True)
        self.phones = []
        self.add_phone(phone)
        self.birthday = None
        self.add_birthday(birthday)

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, "\
                        f"phones: {'; '.join(p.value for p in self.phones)}, "\
                        f"birthday: {self.birthday if self.birthday else ''}"
        
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
    
    def add_birthday(self, birthday: str):
        if birthday:
            self.birthday = Birthday(birthday)

    def days_to_birthday(self) -> int:
        if self.birthday:
            cur_date = datetime.now().date()
            
            new_birthday = self.birthday.value
            new_birthday = new_birthday.replace(year=cur_date.year)
            
            if new_birthday < cur_date:
                new_birthday = new_birthday.replace(year=cur_date.year+1)
            
            delta = new_birthday - cur_date
            
            return delta.days

class Pagination:
    DEFAULT_PER_PAGE = 3

    def __init__(self, records: list, records_per_page=None):
        self.curent_page = 1
        self.records_per_page = records_per_page if records_per_page else self.DEFAULT_PER_PAGE
        self.records = records
        self.pages_count = (len(self.records) - 1) // self.records_per_page + 1

    def __next__(self):
        if self.curent_page <= self.pages_count:
            start = (self.curent_page - 1) * self.records_per_page
            stop = start + self.records_per_page
            page = ""
            for record in self.records[start: stop]:
                page += str(record) + "\n"
            page += f"Page {self.curent_page} of {self.pages_count}"
            self.curent_page += 1
            
            return page
        raise StopIteration

class AddressBook(UserDict):
    def __init__(self):
        self.pagination = None
        super().__init__()
        
    def add_record(self, record: Record) -> None:
        if record.name.value in self.data:
            raise ValueError(f"Record with name {record.name.value} is already exists")
        self.data[record.name.value] = record
    
    def delete(self, name: str) -> Record:
        if name in self.data:
            return self.data.pop(name)

    def find(self, name: str) -> Record:
        return self.data.get(name)
    
    def iterator(self, records_per_page=None):
        records = [self.data[key] for key in self.data]
        return Pagination(records, records_per_page)

