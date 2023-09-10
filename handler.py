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
        except ValueError as error:
            message = str(error)
            
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

    if contacts.delete(name):
        message = f"Contact {name} was successfully deleted!"
    else:
        message = f"Contact with name {name} does not exists"
    return message

def find_contact(name=None, phone=None) -> str:
    """Searching contacts by given name"""

    contact = contacts.find(name)
    if contact:
        message = str(contact)
    else:
        message = "Didn't find anything!"
    return message

@input_error
def add_phone(name: str, phone: str) -> str:

    contact = contacts.data[name]
    contact.add_phone(phone)
    message = f"For contact {name} was added phone number {phone}"

    return message

@input_error
def edit_phone(name: str, old_phone: str, new_phone: str) -> str:
    
    contact = contacts.data[name]
    contact.edit_phone(old_phone, new_phone)
    message = f"Phone of {name} was successfully changed" \
                f" from {old_phone} to {new_phone}."
    
    return message

@input_error
def delete_phone(name: str, phone: str) -> str:
    contact = contacts.data[name]
    contact.remove_phone(phone)
    message = f"Phone of {name} was successfully deleted"

    return message

@input_error
def show_phone(name: str) -> str:
    """Shows phone numer by Name in contact list"""
    record = contacts.data[name]
    message = ""
    
    for phone in record.phones:
        message += f"{phone.value}\n"
    
    return message

def show_contacts() -> str:
    """Shows contacts given in user_contacts.
    If not any parameter given shows all contacts
    return str in phormat:
    """

    message = ""
    for contact in contacts.data.values():
        message += str(contact) + "\n"
        
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
