from collections import UserDict
from datetime import datetime
from pickle import dump, load
from abc import abstractmethod, ABC
from re import search

class Target(ABC):
    pagination = None
    
    @abstractmethod
    def add(self):
        """Adding record"""
    
    @abstractmethod
    def delete(self):
        """Delete record"""
    
    @abstractmethod
    def find(self):
        """Finding record"""

    @abstractmethod
    def save(self):
        """Saving changes"""
    
    @abstractmethod
    def restore(self):
        """Restoring racords"""

    @abstractmethod
    def iterator(self):
        """Iteration by records"""

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
    DATE_FORMAT = "%d.%m.%Y"

    def __str__(self):
        if self.value:
            return datetime.strftime(self.value, self.DATE_FORMAT)
        else:
            return ""

    @Field.value.setter
    def value(self, new_value: str):
        date_value = datetime.strptime(new_value, self.DATE_FORMAT).date()
        if date_value > datetime.now().date():
            raise ValueError("Date of birth can not be in the future!")
        else:
            self._value = date_value

class Email(Field):
    def __str__(self):
        if self.value is None:
            return ""
        else:
            return self.value

    @Field.value.setter
    def value(self, new_value: str):
        if search(r"^[\w+\.]+@([\w-]+\.)+[\w+]{2,4}$", new_value):
            self._value = new_value
        else:
            raise ValueError("Give me correct email")

class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None, email: Email=None):
        self.name = name
        self.phones = []
        self.add_phone(phone)
        self.birthday = None
        self.add_birthday(birthday)
        self.email = None
        self.add_email(email)

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, "\
                        f"phones: {'; '.join(p.value for p in self.phones)}, "\
                        f"birthday: {self.birthday if self.birthday else ''}"\
                        f"email: {self.email}"
        
    def find_phone(self, value: str, strict=True) -> Phone:
        result = None
        for phone in self.phones:
            if phone.value == value or \
                    not strict and phone.value.find(value) != -1:
                
                result = phone
                break

        return result

    def add_phone(self, phone: Phone) -> None:
        if phone:
            self.phones.append(phone)
        
    def remove_phone(self, value: str) -> None:
        phone = self.find_phone(value)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone doesn't exist")
        

    def edit_phone(self, old_value: str, new_value: str) -> None:
        phone = self.find_phone(old_value)
        if phone:
            phone.value = new_value
        else:
            raise ValueError("Phone doesn't exist")
    
    def add_birthday(self, birthday: Birthday):
        if birthday:
            self.birthday = birthday

    def days_to_birthday(self) -> int:
        if self.birthday:
            cur_date = datetime.now().date()
            
            new_birthday = self.birthday.value
            new_birthday = new_birthday.replace(year=cur_date.year)
            
            if new_birthday < cur_date:
                new_birthday = new_birthday.replace(year=cur_date.year+1)
            
            delta = new_birthday - cur_date
            
            return delta.days
        
    def add_email(self, email: Email):
        if email:
            self.email = email

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
    def __init__(self, file_name: str = None):
        self.__file_name = None
        self.file_name = file_name

    @property
    def file_name(self):
        return self.__file_name
    
    @file_name.setter
    def file_name(self, file_name:str):
        self.__file_name = file_name
        self.restore()
    
    def add(self, record: Record) -> None:
        if record.name.value in self.data:
            raise ValueError(f"Record with name {record.name.value} is already exists")
        self.data[record.name.value] = record
        self.save()
    
    def delete(self, name: str) -> Record:
        if name in self.data:
            self.data.pop(name)
            self.save()
            return True
        

    def find(self, search: str) -> Record:
        records = []
        for name, record in self.data.items():
            pos = name.find(search)
            if pos != -1:
                records.append(record)
            elif record.find_phone(search, strict=False):
                records.append(record)
            elif search in record.email:
                records.append(record)
            elif search in str(record.birthday):
                records.append(record)

        return records
    
    def iterator(self, records_per_page=None):
        records = [self.data[key] for key in self.data]
        return Pagination(records, records_per_page)

    def save(self):
        with open(self.file_name, "wb") as f:
            dump(self.data, f)

    def restore(self):
        try:
            with open(self.file_name, "rb") as f:
                self.data = load(f)
        except:
            self.data = {}
