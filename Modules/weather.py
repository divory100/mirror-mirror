import datetime #library to get current time
import json
import requests

#open file that holds API key
with open("Keys/openweathermap_key.json", "r") as fp:
    j = json.load(fp)
    key = j["key"]
    lat = j["lat"]
    lon = j["lon"]
HOURLY_URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}" \
f"&exclude=daily,minutely,alerts&units=metric&appid={key}"
WEEKLY_URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}"\
f"&exclude=hourly,minutely,alerts&units=metric&appid={key}"

def weather(subcommand="today"):
    """
    Command to retrieve weather data from openweathermap
    Has subcommands 'today', 'tomorrow' and 'week'
    Displays different set of data depending on subcommand used
    'today' is default subcommand
    """

    if subcommand == "week":
        response = requests.get(WEEKLY_URL) #get the data
        data = response.json() #convert to json format

        daily = data["daily"][:5] #only want first 5 days

        reply = ""

        #iterate through the week's weather data list
        for i, elem in enumerate(daily):
            desc = elem["weather"][0]["description"]
            temp = int(round(elem["temp"]["day"], 2))
            days = ["Today", "Tomorrow", "Day after tomorrow", "Next day", "Day after that"]
            reply += f"{days[i]}: {desc}, {temp}°C" if i == 0 \
                    else f"\n{days[i]}: {desc}, {temp}°C"

        speech = "The weather for the next few days is on the screen."
        title = "Weather this week"
    else:
        response = requests.get(HOURLY_URL)
        data = response.json()

        #find current hour, to calculate which hours to show
        hour = int(datetime.datetime.now().strftime("%H"))
        index = 24 - hour

        if subcommand == "today":
            hourly = data["hourly"][:index]
        else:
            #weather for tomorrow: removes data from today and then only takes...
            #...16 hours worth of data because of space constraints
            hourly = data["hourly"][(index+7):][:16]
            hour = 7

        hourly_weather = []

        reply = ""

        for i, elem in enumerate(hourly):
            desc = elem["weather"][0]["description"]
            temp = int(round(elem["temp"], 0))
            if hour+i < 10:
                a = "0"
            else:
                a = ""
            reply += f"{a}{hour+i}:00 - {desc}, {temp}°C" if i == 0 else f"\n{a}{hour+i}:00 - {desc}, {temp}°C"

        if subcommand == "today":
            next_hour = hourly[0]["weather"][0]["description"]
            speech = f"The weather for the next hour is {next_hour}"
            title = "Weather today"
        else:
            speech = "Tomorrow's weather is on the screen."
            title = "Weather tomorrow"

    return {"speech": speech , "action": {"TEXT_M": {"text": title, "font": "Helvetica 40"}, \
    "TEXT_S": {"text": reply, "font": "Helvetica 20"}}}
