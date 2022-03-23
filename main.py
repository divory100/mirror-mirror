import asyncio
from Graphics import graphics_tools as gt
from gtts import gTTS
import json
from Parsing import commands
from playsound import playsound
import pocketsphinx as ps
from queue import Queue
import threading
import sounddevice
import websockets

URI = "ws://localhost:2700"
CONFIG = '{"config": {"sample_rate": 16000}}'
EOF = '{"eof": 1}'

def callback(data_in, f, t, s):
    """Callback function for the voice input stream"""
    loop.call_soon_threadsafe(audio_q.put_nowait, bytes(data_in))

async def main():
    """Main event loop: listens for speech and carries out commands"""

    #asyncio loop and audio queue. global so that callback can access them
    global audio_q
    global loop

    audio_q = asyncio.Queue()
    loop = asyncio.get_event_loop()

    q = Queue() #Thread queue for sharing data with the graphics daemon

    #start the graphics daemon
    threading.Thread(target=gt.screen_handler, args=(q,), daemon=True).start()

    with sounddevice.RawInputStream(samplerate=16000, blocksize=4000, dtype="int16",
                channels=1, callback=callback)as device:
        #Connect to the websocket running vosk server
        async with websockets.connect(URI) as ws:
            await ws.send(CONFIG) #Setup connection

            #main event loop
            while True:

                #receive mic input from the audio queue, then send to the websocket
                data = await audio_q.get()
                await ws.send(data)

                #receive recognised speech from the websocket
                speech_data = await ws.recv()
                speech_data = json.loads(speech_data)

                try:
                    #if the text is a complete sentence
                    command = speech_data["text"]
                except KeyError:
                    #websocket returned a partial response, ignore
                    continue

                if command != "" and command.startswith("assistant"):

                    #call the parser to translate and execute the command
                    response, action = commands.execute(command)

                    if action is not None:
                        #Put data on the queue so that the graphics thread will pick up on it and act
                        q.put(action)

                    #Text to speech output (google's TTS API)
                    output = gTTS(response)
                    output.save("response.mp3")
                    playsound("response.mp3")

            await ws.send(EOF)

if __name__ == "__main__":
    print("Starting Mirror...")
    print("Ready!")
    asyncio.run(main())
    print("Shutting down...")
