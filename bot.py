EXIT_MESSAGE = "Good bye!"

contacts = {}

def input_error(handler):
    
    def _wrapper(*args):
        """Handles user input exceptions"""
        
        try:
            message = handler(*args)
        except TypeError:
            if len(args) == 0:
                message = "Please give me name"
            else:
                message = "Please give me phone number"
        except KeyError:
            message = "There is no contact with such name. \
                        Use 'show all' command to view your contact list"

        return message
    
    return _wrapper

def start_bot() -> str:
    """Just say hello"""
    
    message = "Hi, what can I help you?"

    return message

@input_error
def add_contact(name: str, phone: str) -> str:
    """Add new record to contact list"""
    
    if name in contacts:
        message = "A contact with the sanme name already exists!"
    else:
        contacts[name] = phone
        message = f"A contact {name} was successfully added!"

    return message

@input_error
def change_contact(name: str, phone: str) -> str:
    """Change contact phone by Name"""

    old_phone = contacts[name]
    contacts[name] = phone

    return f"{name}'s phone was changed from {old_phone} to {phone}"

@input_error
def show_phone(name: str) -> str:
    """Shows phone numer by Name in contact list"""
    
    return contacts[name]

def show_all_contacts() -> str:
    """Shows all contacts in list in
    |  Name  |  Phone  | table
    """

    name_width = 10
    phone_width = 10
    
    for name, phone in contacts.items():
        name_width = max(len(name), name_width)
        phone_width = max(len(phone), phone_width)
        
    message = "|" + "Name".center(name_width) + "|" + "Phone".center(phone_width) + "|\n"
    
    for name, phone in contacts.items():
        message += "|" + name.ljust(name_width) + "|" + phone.ljust(phone_width) + "|\n"
        
    return message

def finish_bot() -> str:
    """Just say good bye"""
    
    return EXIT_MESSAGE

HANDLER_DICT = {"hello": start_bot,
                 "add": add_contact,
                 "change": change_contact,
                 "phone": show_phone,
                 "show all": show_all_contacts,
                 "exit": finish_bot,
                 "good bye": finish_bot,
                 "close": finish_bot}

def command_parcer(input_message: str) -> tuple:
    """Finds a command word in user text.
    If command takes any parameters they must 
    come after the command word and be separated by spaces
    """
    
    message = input_message.lower()
    handler = None
    params = None
    
    for cmd, fnc in HANDLER_DICT.items():
        pos = message.find(cmd)
        
        if pos != -1:
            if cmd in ("add", "change"):
                params = input_message[pos + len(cmd) + 1:].split(" ")
                params = params[:2]
            if cmd == "phone":
                params = input_message[pos + len(cmd) + 1:].split(" ")
                params = params[0]
            handler = fnc
            break
        
    return handler, params
     

def main():

    message = ""
    while message != EXIT_MESSAGE:

        user_input = input()
        
        handler, params = command_parcer(user_input)
        
        if handler is None:
            message = f"I didn\'t catch you! Please enter one of the \
                        following commands: {', '.join(HANDLER_DICT.keys())}"
        elif params is None:
            message = handler()
        else:
            message = handler(*params)
        
        print(message)
        
if __name__ == "__main__":
    
    main()