from abc import abstractmethod, ABC
from menu import Menu

class UserInterface(ABC):
    exit = False

    @abstractmethod
    def data_input(self):
        """Returns user data or actions"""
    
    @abstractmethod
    def data_output(self, data):
        """Shows proccessed data to user"""


class ConsoleUserInterface(UserInterface):
    def __init__(self):
        self.Menu = Menu()
        self.command = None

    def data_input(self):
        user_input = input()
        
        return user_input
    
    def data_output(self, data):
        print(data)

        