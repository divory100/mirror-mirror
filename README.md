# Mirror Mirror
*A program to run a voice assistant with a graphical status display*

I created this to be run on a raspberry pi magic mirror and be like mirror mirror on the wall from shrek/snow white, hence the name.

## Details
The program uses pocketsphinx to listen for voice commands, while in the background running a graphical status display (using threading) with the time/weather. The voice assistant also uses the graphical display to show relevant information for the command the user used.

### Commands
 - time
 - date
 - weather
 - joke
 - general greeting

***More coming soon!***

## Dependencies
 - pocketsphinx
 - pysimplegui (Tkinter port)
 - gTTS
 - requests
 - playsound

In addition, you need to create the json file ```openweathermap_key.json```, in the in the same directory as main.py.

```json
{"key": "INSERT OPENWEATHERMAP API KEY", "lat": "INSERT YOUR LOCATION'S LATITUDE", "lon": "INSERT YOUR LOCATION'S LONGITUDE"}
