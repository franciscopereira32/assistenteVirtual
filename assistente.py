
#!/usr/bin/env python3

import argparse
from asyncio.windows_events import NULL
from multiprocessing.resource_sharer import stop
from pydoc import TextRepr
import queue
import sys
from tkinter.messagebox import NO
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3
import json
import core
import datetime

#sintese de fala
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice',voices [-2].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

#reconhecimento de fala

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()  # type: ignore
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")  # type: ignore
args = parser.parse_args(remaining)

#loop do reconhecimento de fala
try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])  # type: ignore

    model = Model(lang="pt")

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result = json.loads(result)

                if result is not None:
                    text = result['text']

                    print(text)
                    #speak(text)

                    if text == 'que horas são' or text == 'me informe a hora':
                        speak(core.SystemInfo.get_time())
                    
                    if text == 'obrigado' or text ==  'obrigada':
                        res_obr = 'disponha, estou aqui para te ajudar'
                        speak(res_obr)
                        print(res_obr)

                    if  text == 'me informe a data' or text == 'data atual':
                        date = datetime.date.today()
                        data_em_texto = "{}/{}/{}".format(date.day, date.month,date.year)
                        speak(data_em_texto)  
                        print(data_em_texto)
except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))# type: ignore
    