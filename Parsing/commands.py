import json
from Modules import general
from Modules import weather
from Modules import fun
from Modules import info

with open("Parsing/parser.json", "r") as fp:
    COMMANDS = json.load(fp)

def execute(command):
    """
    Handler to translate and then execute the command passed in.
    Returns a speech response and action (dictionary)
    The action is instructions on which graphics element to edit, eg TEXT_M is the main text slot
    """
    #COMMANDS = ["weather", "time", "date", "how are you", "joke", "news"]

    #open the json file which stores all the detailed command data
    with open("Parsing/parser.json", "r") as p:
        parser = json.load(p)

    #default response
    response = {"speech": "Sorry, I did not recognise that command.", "action": None}

    for keyword in COMMANDS:
        #If a command trigger is found in the phrase the user said
        if keyword in command:
            #check for subcommands
            arguments = command.partition(keyword)[2]
            details = parser[keyword]
            try:
                subcommand = None
                for subc in details["subcommands"]:
                    if subc in arguments:
                        subcommand = subc
                        break
            except KeyError:
                #The command doesn't have any subcommands
                subcommand = None
            #execute the command's function
            response = command_function(parser[keyword]["func"], subcommand=subcommand)

    return response["speech"], response["action"]

def command_function(func, subcommand=None, window=None):
    """Function to 'eval' the command's function with arguments"""
    if subcommand is not None:
        return eval(f"{func}(subcommand='{subcommand}')")
    else:
        return eval(f"{func}()")
