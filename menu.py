class Menu():
    close = False
    MENU = {
    "Main": ["Hello", "Contacts", "Notes", "File Sorter", "Exit/Close/Good Bye"],
    "Contacts": ["Add", "Delete", "Add phone", "Del phone", "Find", "DTB", "SBS", "Show", "Next"],
    "Notes": ["Add", "Delete", "Add tag", "Del tag", "Find", "Show", "Next"],
    "Edit": [],
    "Add": [],
    "Delete": [],
    "Find": [],
    "DTB": [],
    "SBS": [],
    "File Sorter": [],
    "Exit": [],
    "Close": [],
    "Good Bye": [],
    "Show": [],
    "Phone": ["add", "edit", "delete"]
    }

    def navigate(self, command: str):
        result = ""
        for key in self.MENU:
            if command.lower() == key.lower():
                self.close = command.lower() in "exit/close/good bye"
                if self.MENU[key]:
                    result = "\n"
                    result = result.join(self.MENU[key]) + "\n------------------------"
                    result = f"-----------{key}--------\n" + result
                break

        return result