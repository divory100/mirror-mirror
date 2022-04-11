# Mirror Mirror
*A program to run a voice assistant with a graphical status display*

## NOTE: currently undergoing major rework, will be rebranded after that

I created this to be run on a raspberry pi magic mirror and be like mirror mirror on the wall from shrek/snow white, hence the name.

## Details
The program uses pocketsphinx to listen for voice commands, while in the background running a graphical status display (using threading) with the time/weather. The voice assistant also uses the graphical display to show relevant information for the command the user used.

### Commands
 - time
 - date
 - weather
 - joke
 - general greeting
 - news
 - definitions

 The assistant listens for keywords, not phrases, for example:
  - "assistant tell me a joke" - this will work
  - "assistant tell a joke" - this will also work

 The default wake word is "assistant"; this can be changed on lines 59 and 60 of main.py.

***More coming soon!***

## Dependencies
 - vosk
 - pysimplegui (Tkinter port)
 - gTTS
 - requests
 - playsound
 - sounddevice
 - websockets

## Required API key files
You will need to create a couple of files in a directory called Keys/.
These are:
 - ```openweathermap_key.json```:
    ```json
    {"key": "INSERT OPENWEATHERMAP API KEY", "lat": "INSERT YOUR LOCATION'S LATITUDE", "lon": "INSERT YOUR LOCATION'S LONGITUDE"}
    ```
 - ```newsapi_key.txt```:
    ```txt
    <insert api key here>
    ```

## Important: Starting VOSK server
This project uses the VOSK speech recognition API, and requires a VOSK server to be running on port 2700.

 - For x86/amd64:
    You can run the VOSK websocket server using docker: `docker run -d -p 2700:2700 alphacep/kaldi-en:latest`

 - For ARM (also works on x86/amd64):
    1. Clone the vosk server repository https://github.com/alphacep/vosk-server/
    2. Download a language model https://alphacephei.com/vosk/models - I'm running this project on a raspberry pi 4, for which I found the en-us small model worked best - I didn't have enough RAM to use the normal sized model. Otherwise however the normal model is useful as it is slightly more accurate.
    3. Extract the model into a directory called "model" which is itself in the `vosk-server/websocket/` directory. (alternatively put it in the `vosk-server/websocket-cpp/` folder if you are going to run the CPP version of the server)
    4. Run the server - either `asr_server.py` if you're using the python version in `vosk-server/websocket/`, or `asr_server.cpp` if you're using the CPP version in `vosk-server/websocket-cpp/` directory.
