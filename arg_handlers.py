#########################        
#---Arguments handlers--#
#########################
from pathlib import Path
from abc import abstractmethod, ABC
from address_book import *

class Handler(ABC):
    """
    Base handler class
    """

    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        
        return handler

    @abstractmethod
    def handle(self, request) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None

class NameHandler(Handler):
    def handle(self, args):
        if "name" not in args:
            return super().handle(args)
        name = args["name"]
        if not name:
            raise ValueError("Give me name please")
        
        return Name(name, True)
        

class BirthdayHandler(Handler):
    def handle(self, args):
        if "birthday" not in args:
            return super().handle(args)
        birthday = args["birthday"]
        if birthday is None:
            raise ValueError("Giva me date of birth")
        
        return Birthday(birthday)
        

class PhoneHandler(Handler):
    def handle(self, args):
        if "phone" not in args:
            return super().handle(args)
        phone = args["phone"]
        if phone is None:
            raise ValueError("Give me phone number")
        
        return Phone(phone)


class EmailHandler(Handler):
    def handle(self, args):
        if "email" not in args:
            return super().handle(args)
        email = args["email"]
        if email is None:
            raise ValueError("Give me email")
        
        return Email(email)
    
    
class TextHadnler(Handler):
    def handle(self, args):
        if "text" not in args:
            return super().handle(args)
        text = args["text"]
        if not text:
            raise ValueError("Write your note here:")
        
        return text


class TagsHandler(Handler):
    def handle(self, args):
        if "tags" not in args:
            return super().handle(args)
        tags = args["tags"]
        if not tags:
            raise ValueError("Enter your tags")
        
        tags_list = []
        for tag in tags.split(" "):
            if tag:
                tags_list.append(tag)

        return tags_list


class FolderHandler(Handler):
    def handle(self, args: dict):
        if "folder" not in args:
            return super().handle(args)

        path = args["folder"]
        if path is None:
            raise ValueError("Give me a folder")
        if not Path(path).exists():
            raise ValueError("invalid path")
        return Path(path)
    
class IdHandler(Handler):
    def handle(self, args) -> str:
        if "id" not in args:
            return super().handle(args)
        id = args["id"]
        if not id:
            raise ValueError("Give me id:")
        
        return id
    
class SearchHandler(Handler):
    def handle(self, args) -> str:
        if "search" not in args:
            return super().handle(args)
        search = args["search"]
        if not search:
            raise ValueError("What do you want to search:")
        
        return search
    
class IntersecHandler(Handler):
    def handle(self, args):
        if "intersec" not in args:
            return super().handle(args)
        intersec = args["intersec"]
        if intersec is None:
            raise ValueError("All of your tags in each record?(Y/N)")
        
        return intersec.lower() == "y"
    
class FieldHandler(Handler):
    def handle(self, args):
        if "field" not in args:
            return super().handle(args)
        field = args["field"]
        if not field:
            raise ValueError("What field do you want to edit:")
        
        return field
    
class TagHandler(Handler):
    def handle(self, args):
        if "tag" not in args:
            return super().handle(args)
        tag = args["tag"]
        if not tag:
            raise ValueError("Enter tag:")
        
        return tag