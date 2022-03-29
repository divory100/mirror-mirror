import datetime
import random
import requests

def shutdown():
    return {"speech": "Goodbye!", "action": None}


def time(subcommand=None):
    """Command to reply with the current time (24H)"""
    return {"speech": f"The current time is {datetime.datetime.now().strftime('%H:%M')}", \
     "action": None}

def date(subcommand=None):
    """Command to reply with today's date"""
    months = ["January", "February", "March", "April", "May", "June", "July", "August", \
    "September", "October", "November", "December"]
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    #get the name of the month
    month_format = months[month - 1]

    #add "st"/"nd"/"rd"/"th" suffix to the day
    day_format = str(day)
    if day_format == "11" or day_format == "12" or day_format == "13":
        day_format += "th"
    elif day_format.endswith("1"):
        day_format += "st"
    elif day_format.endswith("2"):
        day_format += "nd"
    else:
        day_format += "th"

    main_response = f"Today is the {day_format} of {month_format} {year}"

    return {"speech": main_response, "action": None}

def greeting(subcommand=None):
    """Hello command that replies with random response when user asks 'how are you'"""
    responses = ["I am good thank you.", "I am doing great", "I'm fine thank you", \
     "All is well thank you for asking"]
    return {"speech": random.choice(responses), "action": {"TEXT_M": \
    {"text": "Hello!", "font": "Helvetica 70"}}}
