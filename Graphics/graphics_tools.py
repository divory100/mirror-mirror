import datetime
import json
import PySimpleGUI as psg
import requests #library for performing http requests on webpages
import time

with open("Keys/openweathermap_key.json", "r") as file:
    j = json.load(file)
    key = j["key"]
    lat = j["lat"]
    lon = j["lon"]
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}" \
    f"&exclude=daily,minutely,alerts&units=metric&appid={key}"

def screen_handler(queue):
    """
    Function to start up the display, then listen for any actions from the main loop
    and carry these out.
    """
    weather_counter = 0 #Counter for the program to know when to update the weather widget
    #Each command's action should only be displayed for 10s, so this counter is here to count that
    command_counter = 0
    #Create instance of pysimplegui window, then set default widgets
    window = create_window()
    cur_weather = current_weather()
    window.read(timeout=0, close=False)
    window = default_display(window, cur_weather)
    while True:

        window.read(timeout=0, close=False) #Update the window

        if not queue.empty(): #If there is data sent from the main thread
            command_counter = 0
            action = queue.get() #get any data that the main thread has put on the queue
            window = clear_screen(window)
            window = command_graphics(window, action) #display the "action" the command sent on the screen.
        if command_counter == 30:
            window = default_display(window, cur_weather) #clear the command action; show default display
        if weather_counter == 1800:
            cur_weather = current_weather()
            weather_counter = 0

        time.sleep(1) #delay, to give main thread a chance to execute its code
        #increment the counters
        weather_counter += 1
        command_counter += 1

def create_window():
    #Text slot 1
    text_main = psg.Text(
        font="Helvetica 30",
        background_color="black",
        text_color="white",
        key="TEXT_M", #so that can reference later with .update()
        auto_size_text=True,
    )
    #Text slot 2
    text_secondary = psg.Text(
        font="Helvetica 30 italic",
        background_color="black",
        text_color="white",
        key="TEXT_S",
        auto_size_text=True,
    )
    #Image slot
    image_slot = psg.Image(
        key="IMAGE"
    )

    layout = [[text_main], [text_secondary], [image_slot]]

    #Create graphical window
    window = psg.Window(
        title="Magic Mirror",
        element_justification="center",
        no_titlebar=True, #no window titlebar
        location=(0, 0),
        keep_on_top=True, #fullscreen
        size=(1155, 1000),
        layout=layout,
        background_color="black",
    )

    return window

def default_display(window, cur_weather):
    """Default status display with time and weather"""
    cur_time = datetime.datetime.now().strftime("%H:%M")
    window["TEXT_M"].update(cur_time, font="Helvetica 30")
    window["TEXT_S"].update(cur_weather, font="Helvetica 30 italic")
    window["IMAGE"].update() #blank
    return window

def clear_screen(window):
    """Clear the main text, secondary text, and image widgets"""
    window["TEXT_M"].update("", font="Helvetica 30")
    window["TEXT_S"].update("", font="Helvetica 30 italic")
    window["IMAGE"].update()
    return window

def current_weather():
    """Get current weather data from openweathermap.org"""
    response = requests.get(WEATHER_URL)
    data = response.json()
    current = data["current"]

    weather_desc = current["weather"][0]["description"]
    temp = int(round(current["temp"], 0)) #temperature
    return f"{weather_desc.title()}, {temp}°C" #formatted description

def command_graphics(window, action):
    """Display graphics required by a command"""
    for key in action:
        if key == "IMAGE": #image slot
            window[key].update(source=action[key])
        else: #text main or text secondary
            window[key].update(action[key]["text"], font=action[key]["font"])
    return window
