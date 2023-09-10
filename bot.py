from handler import HANDLER_DICT, EXIT_MESSAGE

def command_parcer(input_message: str) -> tuple:
    """Finds a command word in user text.
    If command takes any parameters they must 
    come after the command word and be separated by spaces
    """
    
    message = input_message.lower()
    handler = None
    params = []
    params_dict = {}
    
    for cmd, fnc in HANDLER_DICT.items():
        pos = message.find(cmd)
        
        if pos != -1:
            if not cmd in ("hello", "show all", "exit", "good bye", "close"):
                cut_message = input_message[pos + len(cmd) + 1:]
                if cut_message:
                    params = cut_message.split(" ")
            if cmd in ("add", "delete phone", "new phone"):
                params = params[:2]
            elif cmd == "find":
                params = params[:1]
                params_dict = {}
                for param in params:
                    try:
                        key, value = param.split("=")
                    except ValueError:
                        continue
                    params_dict[key] = value
                    params.remove(param)
            elif cmd in ("phones", "remove"):
                params = params[:1]
            elif cmd == "edit phone":
                params = params[:3]
            
            handler = fnc
            break
        
    return handler, params, params_dict
     

def main():

    message = ""
    while message != EXIT_MESSAGE:

        user_input = input()
        
        handler, args, kwargs = command_parcer(user_input)
        
        if not handler:
            message = "I didn\'t catch you! Please enter one of the " \
                        f"following commands: {', '.join(HANDLER_DICT.keys())}"
        else:
            message = handler(*args, **kwargs)
        
        print(message)
        
if __name__ == "__main__":
    
    main()