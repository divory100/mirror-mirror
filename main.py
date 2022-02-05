from Graphics import graphics_tools as gt
from gtts import gTTS
from Parsing import commands
from playsound import playsound
import pocketsphinx as ps
import threading
from queue import Queue

MODELDIR = "SpeechModel"
MODEL = "current.lm"
DIC = "current.dic"

def main():
    """Main event loop: listens for speech and carries out commands"""

    q = Queue() #Thread queue for sharing data

    #start the graphics daemon
    threading.Thread(target=gt.screen_handler, args=(q,), daemon=True).start()

    listener = ps.LiveSpeech(
        lm=f"{MODELDIR}/{MODEL}", #language model file
        dic=f"{MODELDIR}/{DIC}", #dictionary of set phrases (commands)
        sampling_rate=16000,
    )
    #listener is a generator function
    for command in listener:
        command = str(command).lower()
        if command != "" and command.startswith("mirror mirror"):
            print(command)
            #call the parser to translate and execute the command
            response, action = commands.execute(command)

            if action is not None:
                #Put data on the queue so that the graphics thread will pick up on it and act
                q.put(action)

            #Text to speech output (google TTS)
            output = gTTS(response)
            output.save("response.mp3")
            playsound("response.mp3")

if __name__ == "__main__":
    print("Starting Mirror...")
    print("Ready!")
    main()
    print("Shutting down...")
