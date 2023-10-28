from handler import CommandCreator, Command
from interfaces import ConsoleUserInterface
     

def main():
    ui = ConsoleUserInterface()
    handler = CommandCreator()
    ui.data_output(ui.Menu.navigate("Main"))
    command: Command = None

    while not ui.Menu.close:
        output_data = ""
        user_data = ui.data_input()

        if command is None:
            output_data = ui.Menu.navigate(user_data)
            command = handler.create(user_data)
        else:
            command.set_args(user_data)
        
        if not command is None:
            result = command.execute()
            if command.success:
                command = None
        if not output_data:
            output_data = result

        ui.data_output(output_data)

        
if __name__ == "__main__":
    
    main()