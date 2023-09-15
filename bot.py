from handler import HANDLER_DICT, EXIT_MESSAGE, input_error

@input_error
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
            cut_message = input_message[pos + len(cmd) + 1:]
            if cut_message:
                params = cut_message.split(" ")
            
            if cmd in ("delete phone", "new phone"):
                params = params[:2]
            
            elif cmd == "show all":
                params = params[:1]
                if params and params[0].isdigit():
                    params[0] = int(params[0])
                elif params and not params[0].isdigit():
                    raise ValueError("Number of records per page must be positive integer value")

            elif cmd in ("phones", "remove", "find"):
                params = params[:1]
            
            elif cmd in ("edit phone", "add"):
                params = params[:3]
            
            handler = fnc
            break
    
    if handler is None:
        raise ValueError("I didn\'t catch you! Please enter one of the " 
                         f"following commands: {', '.join(HANDLER_DICT.keys())}")
    else:
        return handler(*params, **params_dict)
     

def main():

    message = ""
    while message != EXIT_MESSAGE:

        user_input = input()
        
        message = command_parcer(user_input)
        
        print(message)
        
if __name__ == "__main__":
    
    main()