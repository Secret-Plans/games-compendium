

def s_input(prompt : str = ">", accepted_inputs : list = ["break"], case_sensitive : bool = False, fail_message : str = "") -> str:
    """Keeps asking for user input until the answer is acceptable.



    Args:
        prompt (str, optional): User is prompted with this each time. Defaults to ">".
        accepted_inputs (list, optional): List of inputs that allows the user to continue. Defaults to ["break"].
        case_sensitive (bool, optional): Whether or not the input is case sensitive. Defaults to False.
        fail_message (str, optional): The message to print when the input is invalid. Leave blank for no message.

    Returns:
        str: The valid user input. Will be lowercase if case_sensitive is False.
    """

    user_input = ""
    first = True #For checking if the fail message should print or not
    while user_input not in accepted_inputs:
        if fail_message != "" and not first:
            print(fail_message) #Prints the assigned fail message if it isn't the first iteration
        user_input = input(prompt) #Gets user input
        if not case_sensitive:
            user_input = user_input.lower() #Sets the input to lower if needed
        first = False #Ensures that it is not the first iteration anymore
    return user_input