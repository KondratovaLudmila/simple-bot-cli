from address_book import *
from notebook import *
from user_config import Config
from arg_handlers import *
from abc import abstractmethod, ABC

config = Config("bot_config.txt")

def input_error(handler):
    
    def _wrapper(*args, **kwargs):
        """Handles user input exceptions"""
        
        try:
            message = handler(*args, **kwargs)
        except TypeError as error:
            message = str(error)
        except KeyError:
            message = "There is no contact with such name. " \
                       "Use 'show all' command to view your contact list."
        except ValueError as error:
            message = str(error)
            
        return message
    
    return _wrapper

#########################        
#----Command handlers---#
#########################

class Command(ABC):
    """
    Interface for executing a command
    """
    _args = None
    args_handlers = None
    success = False
    name = None

    def set_args(self):
        return None
    
    def handle_args(self):
        return None
    
    @abstractmethod
    def execute(self) -> None:
        self.success = True

class StartCommand(Command):
    """Just say hello"""
    def execute(self) -> str:
        super().execute()
        return "Hi, what can I help you?"
    
class ExitCommand(Command):
    def execute(self) -> str:
        super().execute()
        """Just say good bye"""
        return "Good bye!"

class TargetCommand(Command):
    target: Target = None
    record = None
    _args = {}
    
    def set_args(self, value):
        for key in self._args:
            if self._args[key] is None:
                self._args[key] = value
                break

    def handle_args(self):
        args = dict(self._args)
        try:
            for name, value in self._args.items():
                args[name] = self.args_handlers.handle({name: value})
        except Exception as e:
            self._args[name] = None
            raise ValueError(str(e))
        return list(args.values())

    @abstractmethod
    def execute(self) -> None:
        super().execute()

class AddCommand(TargetCommand):
    @input_error
    def execute(self) -> str:
        """Add new record to contact list"""
        args = self.handle_args()
        record = self.record(*args)
        self.target.add(record)
        message = f"A contact was successfully added!"
        super().execute()
        return message

class DeleteCommand(TargetCommand):
    @input_error
    def execute(self) -> str:
        self.handle_args()
        if self.target.delete(*self._args.values()):
            message = f"Record was successfully deleted!"
        else:
            message = f"Record does not exists"
        super().execute()
        return message

class FindCommand(TargetCommand):
    @input_error
    def execute(self) -> str:
        """Searching contacts by given string"""

        args = self.handle_args()
        records = [str(cnt) for cnt in self.target.find(*args)]
        if records:
            message = "\n".join(records)
        else:
            message = "Didn't find anything!"
        super().execute()
        return message


class AddPhoneCommand(TargetCommand):
    _args = {
            "name": None,
            "phone": None
             }
    def handle_args(self):
        args = dict(self._args)
        try:
            for name, value in self._args.items():
                args[name] = self.args_handlers.handle({name: value})
                if self._args["name"] not in self.target:
                    raise ValueError("No such record")
        except Exception as e:
            self._args[name] = None
            raise ValueError(str(e))
        return args
    
    @input_error
    def execute(self) -> str:
        args = self.handle_args()
        contact = self.target[self._args["name"]]
        contact.add_phone(args["phone"])
        self.target.save()
        message = f"New phone was successfully added"
        super().execute()
        return message
    

class DelPhoneCommand(TargetCommand):
    _args = {
            "name": None,
            "phone": None
             }
    def handle_args(self):
        args = dict(self._args)
        try:
            for name, value in self._args.items():
                args[name] = self.args_handlers.handle({name: value})
                if self._args["name"] not in self.target:
                    raise ValueError("No such record")
        except Exception as e:
            self._args[name] = None
            raise ValueError(str(e))
        return args
    
    @input_error
    def execute(self) -> str:
        self.handle_args()
        contact = self.target[self._args["name"]]
        contact.remove_phone(self._args["phone"])
        self.target.save()
        message = f"Phone was successfully deleted"
        super().execute()
        return message
    
    
class AddTagsCommand(TargetCommand):
    _args = {
            "id": None,
            "tags": None
             }
    def handle_args(self):
        args = dict(self._args)
        try:
            for name, value in self._args.items():
                args[name] = self.args_handlers.handle({name: value})
                if self._args["id"] not in self.target:
                    raise ValueError("No such record")
        except Exception as e:
            self._args[name] = None
            raise ValueError(str(e))
        return args
    
    @input_error
    def execute(self) -> str:
        args = self.handle_args()
        contact = self.target[args["id"]]
        contact.add_tags(args["tags"])
        self.target.save()
        message = f"New tag was successfully added"
        super().execute()
        return message
    

class DelTagCommand(TargetCommand):
    _args = {
            "id": None,
            "tag": None
             }
    def handle_args(self):
        args = dict(self._args)
        try:
            for name, value in self._args.items():
                args[name] = self.args_handlers.handle({name: value})
                if self._args["id"] not in self.target:
                    raise ValueError("No such record")
        except Exception as e:
            self._args[name] = None
            raise ValueError(str(e))
        return args
    
    @input_error
    def execute(self) -> str:
        args = self.handle_args()
        contact = self.target[args["id"]]
        contact.remove_tag(args["tag"])
        self.target.save()
        message = f"Tag was successfully deleted"
        super().execute()
        return message
    

class ShowCommand(TargetCommand):
    @input_error
    def execute(self) -> str:
        """Shows contacts given in user_contacts.
        If not any parameter given shows all contacts
        return str in phormat:
        """
        if self.target == {}:
            return "You have no notes yet"
        
        self.target.pagination = self.target.iterator(records_per_page=int(config["records_per_page"]))
        message = next(self.target.pagination)
        super().execute()
        return message


class DtbCommand(TargetCommand):
    _args = {"name": None}
    
    @input_error
    def execute(self):
        self.handle_args()
        days = None
        contact = self.target[self._args["name"]]
        if not contact:
            return "No such contact"
        days = contact.days_to_birthday()
        super().execute()
        if days:
            return str(days)
        else:
            return ""

class NextCommand(TargetCommand):
    def execute(self):
        """Using for listing addressbook"""
        try:
            message = next(self.target.pagination)
        except StopIteration:
            message = "You have reached the end of the addressbook"
        
        super().execute()
        return message

class UnknownCommand(Command):
    def execute(self) -> None:
        super().execute()
        return "Unknown command"
    
class CommandCreator:
    targets = {
                "contacts": AddressBook(config["addressbook_file"]),
                "notes": NoteBook(config["notebook_file"]),
                }
    records = {
                "contacts": Record,
                "notes": Note
                }
    commands = {"hello" : StartCommand,
                "add": AddCommand, 
                "delete": DeleteCommand, 
                "find": FindCommand, 
                "del phone": DelPhoneCommand, 
                "add phone": AddPhoneCommand,
                "del tag": DelTagCommand, 
                "add tags": AddTagsCommand, 
                "show": ShowCommand,
                "next": NextCommand,
                "exit": ExitCommand,
                "good bye": ExitCommand,
                "close": ExitCommand,
                "dtb": DtbCommand,
                "sort files": "6",
                "unknown": UnknownCommand,
                }
    args_handlers = None

    def set_handlers(self, command: Command):
        if self.args_handlers is not None:
            command.args_handlers = self.args_handlers
            return True
        
        self.args_handlers = NameHandler()
        self.args_handlers.set_next(PhoneHandler())\
                                    .set_next(BirthdayHandler())\
                                    .set_next(EmailHandler())\
                                    .set_next(TextHadnler())\
                                    .set_next(TagsHandler())\
                                    .set_next(FolderHandler())\
                                    .set_next(IdHandler())\
                                    .set_next(SearchHandler())\
                                    .set_next(IntersecHandler())\
                                    .set_next(FieldHandler())\
                                    .set_next(TagHandler())

        command.args_handlers = self.args_handlers
        return True
    
    def set_args(self, cmd: Command):
        if cmd.name in ("add", "edit"):
            if isinstance(cmd.target, AddressBook):
                cmd._args = {
                            "name": None,
                            "phone": None,
                            "birthday": None,
                            "email": None,
                            }
            elif isinstance(cmd.target, NoteBook):
                cmd._args = {
                            "text": None,
                            "tags": None,
                            }
        elif cmd.name == "delete":
            if isinstance(cmd.target, AddressBook):
                cmd._args = {
                            "name": None
                            }
            elif isinstance(cmd.target, NoteBook):
                cmd._args = {
                            "id": None
                            }
        elif cmd.name == "find":
            if isinstance(cmd.target, AddressBook):
                cmd._args = {
                            "search": None
                            }
            elif isinstance(cmd.target, NoteBook):
                cmd._args = {
                            "tags": None,
                            "intersec": None, 
                            }
    def set_target(self, target: str):
        TargetCommand.target = self.targets[target]
        TargetCommand.record = self.records[target]
    
    def create(self, command: str):
        if command in ("notes", "contacts"):
            self.set_target(command)
        cmd: Command = self.commands.get(command)
        if not cmd:
            cmd = self.commands.get("unknown")
        cmd = cmd()
        cmd.name = command
        self.set_handlers(cmd)
        self.set_args(cmd)
        
        return cmd