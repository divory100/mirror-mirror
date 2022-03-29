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

            subcommand = None
            if "subcommands" in details:
                #command has subcommands
                for elem in details["subcommands"]:
                    if elem in arguments:
                        subcommand = elem
                        break

            if "params" in details:
                #command has parameters
                params = arguments if subcommand is None else arguments.partition(subcommand)[2]
                params = params.strip(" ")
                if params == "":
                    params = None
            else:
                params = None



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
            response = command_function(parser[keyword]["func"], subcommand=subcommand, params=params)

    return response["speech"], response["action"]

def command_function(func, subcommand=None, params=None, window=None):
    """Function to 'eval' the command's function with arguments"""
    args = ""
    if subcommand is not None:
        args += f"subcommand='{subcommand}'" if params is None else f"subcommand='{subcommand}', "
    if params is not None:
        args += f"params='{params}'"
    return eval(f"{func}({args})")
