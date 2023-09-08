from address_book import *
EXIT_MESSAGE = "Good bye!"

contacts = AddressBook()


def input_error(handler):
    
    def _wrapper(*args, **kwargs):
        """Handles user input exceptions"""
        
        try:
            message = handler(*args, **kwargs)
        except TypeError:
            message = "Less arguments given."
        except KeyError:
            message = "There is no contact with such name. " \
                       "Use 'show all' command to view your contact list."
        except NameExistsError:
            message = "Contact with such name is already exists. " \
                        "Use 'show all' command to view your contact list."
        except IndexError:
            message = "Invalid index. Use 'phone' command to view phone list."
        except PhoneNotFoundError:
            message = "There is no such phone number"
        return message
    
    return _wrapper

def start_bot() -> str:
    """Just say hello"""
    
    message = "Hi, what can I help you?"

    return message

@input_error
def add_contact(name: str, phone="") -> str:
    """Add new record to contact list"""
    
    contact = Record(name, phone)
    contacts.add_record(contact)
    message = f"A contact {name} was successfully added!"

    return message

@input_error
def delete_contact(name: str) -> str:

    contact = contacts.get_record(name)
    contacts.del_record(contact)
    message = f"Contact {name} was successfully deleted!"
    return message

def find_contact(name=None, phone=None) -> str:
    """Searching contacts by given parameters.
    Example 1: find name=Vasya phone=1111
    Example 2: find Vasya 1234"""

    print(name, phone)
    contact_list = contacts.find_records(name, phone)
    if contact_list:
        message = show_contacts(contact_list)
    else:
        message = "Didn't find anything!"
    return message

@input_error
def add_phone(name: str, phone: str) -> str:

    contact = contacts.get_record(name)
    contact.add_phone(phone)
    message = f"For contact {name} was added phone number {phone}"

    return message

@input_error
def edit_phone(name: str, old_phone: str, new_phone: str) -> str:
    
    contact = contacts.get_record(name)
    contact.edit_phone(old_phone, new_phone)
    message = f"Phone of {name} was successfully changed" \
                f" from {old_phone} to {new_phone}."
    
    return message

@input_error
def delete_phone(name: str, phone: str) -> str:
    contact = contacts.get_record(name)
    contact.del_phone(phone)
    message = f"Phone of {name} was successfully deleted"

    return message

@input_error
def show_phone(name: str) -> str:
    """Shows phone numer by Name in contact list"""
    record = contacts.get_record(name)
    message = ""
    
    for phone in record.phones:
        message += f"{phone.value}\n"
    
    return message

def show_contacts(user_contacts=None) -> str:
    """Shows contacts given in user_contacts.
    If not any parameter given shows all contacts
    return str in phormat:
        |  Name  |  Phone  | 
    """

    name_width = 10
    phone_width = 15

    contact_list = user_contacts if user_contacts else list(contacts.data.values())

    
    for contact in contact_list:
        name_width = max(len(contact.name.value), name_width)
        
    message = "|" + "Name".center(name_width) + "|" + "Phone".center(phone_width) + "|\n"
    
    for contact in contact_list:
        name = contact.name.value
        message += "|" + name.ljust(name_width) + "|"

        if not contact.phones:
            message += "".ljust(phone_width) + "|\n"

        for phone in contact.phones:
            message += f"{phone.value}".ljust(phone_width) + "|\n" + "|" + "".ljust(name_width) + "|"

        if contact.phones:
            message = message[:-name_width-2]
        
    return message

def finish_bot() -> str:
    """Just say good bye"""
    
    return EXIT_MESSAGE

HANDLER_DICT = {"hello": start_bot,
                 "add": add_contact,
                 "remove": delete_contact,
                 "find": find_contact,
                 "edit phone": edit_phone,
                 "delete phone": delete_phone,
                 "new phone": add_phone,
                 "phones": show_phone,
                 "show all": show_contacts,
                 "exit": finish_bot,
                 "good bye": finish_bot,
                 "close": finish_bot}
