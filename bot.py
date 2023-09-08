from handler import HANDLER_DICT, EXIT_MESSAGE

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
            if not cmd in ("hello", "show all", "exit", "good bye", "close"):
                params = input_message[pos + len(cmd) + 1:].split(" ")
            if cmd in ("add", "delete phone", "new phone"):
                params = params[:2]
            elif cmd in ("phones", "remove"):
                params = params[:1]
            elif cmd == "edit phone":
                params = params[:3]
            
            handler = fnc
            break
        
    return handler, params
     

def main():

    message = ""
    while message != EXIT_MESSAGE:

        user_input = input()
        
        handler, params = command_parcer(user_input)
        
        if handler is None:
            message = "I didn\'t catch you! Please enter one of the " \
                        f"following commands: {', '.join(HANDLER_DICT.keys())}"
        elif params is None:
            message = handler()
        else:
            message = handler(*params)
        
        print(message)
        
if __name__ == "__main__":
    
    main()