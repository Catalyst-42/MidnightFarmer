from pynput import keyboard
from time import time, sleep
from json import dumps
from threading import Thread
import os

from pynput.keyboard import Key, Controller
controller = Controller()

s = 1
m = 60*s
h = 60*m
d = 24*h

runs = []
open("save.py", "a")
from first_save import *
session = len(runs)

timestamp = 0
state = "begin"
run = {
    "time": 0,
    "note": ""
}

class KEY:
    BEGIN = "."
    BEGIN_ALT = "ю"

    PAUSE = "p"
    PAUSE_ALT = "з"

    NOTE = "y"
    NOTE_ALT = "н"

class TIMEOUT:
    SMALL = 0.05
    MEDIUM = 0.5
    BIG = 4.5

def re_enter():
    global state
    sleep(TIMEOUT.MEDIUM)

    controller.press(Key.esc)
    controller.release(Key.esc)
    sleep(TIMEOUT.SMALL)
    
    for _ in range(5):
        controller.press(Key.down)
        controller.release(Key.down)
        sleep(TIMEOUT.SMALL)

    controller.press(Key.enter)
    controller.release(Key.enter)
    sleep(TIMEOUT.SMALL)

    controller.press(Key.up)
    controller.release(Key.up)

    controller.press(Key.enter)
    controller.release(Key.enter)
    
    sleep(TIMEOUT.BIG)

    controller.press(Key.enter)
    controller.release(Key.enter)
    sleep(TIMEOUT.SMALL)

    controller.press(Key.enter)
    controller.release(Key.enter)

    state = "run"

def pause():
    controller.press(Key.esc)
    controller.release(Key.esc)

def on_press(key):
    global timestamp, state, runs, run

    # TODO:
    # Выбор фала сохранения
    # Более информативный stat мод, подумать
    # Вынос всех настроек

    if hasattr(key, 'char'):
        key_code = key.char
    else:
        key_code = key.name

    match state, key_code:
        case _, "shift_r":
            return False

        # Main run mode
        case ("begin", KEY.BEGIN | KEY.BEGIN_ALT):
            timestamp = time()
            run = {
                "time": 0,
                "note": "",
            }

            state = "run"

        case ("run", KEY.BEGIN | KEY.BEGIN_ALT) | ("note", "enter"):
            run["time"] += time() - timestamp
            runs.append(run)

            timestamp = time()
            run = {
                "time": 0,
                "note": "",
            }

            state = "re_enter"
            Thread(target=re_enter).start()
            # state = "run"

        # Pause mode
        case ("run", KEY.PAUSE | KEY.PAUSE_ALT):
            state = "pause"

            run["time"] += time() - timestamp
            pause()
            state = "pause"

        case ("pause", KEY.PAUSE | KEY.PAUSE_ALT):
            Thread(target=pause).start()
            timestamp = time()

        # Note mode
        case ("run", KEY.NOTE | KEY.NOTE_ALT):
            state = "note"
        
        case "note", "esc":
            timestamp = time()
            run["note"] = ""
            pause()
            state = "run"

        case "note", "backspace":
            run["note"] = run["note"][:-1]

        case "note", "space":
            run["note"] += " "

        case "note", _:
            if hasattr(key, 'char'):
                run["note"] += key.char

    print(f"key: {key} | state: {state} | run: {len(runs) + 1} {run['note']}")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

with open("save.py", "w", encoding="utf-8") as file:
    file.write(f"runs = ")
    file.write(dumps(runs, indent=4, ensure_ascii=False))

if any([run["note"] for run in runs[session:]]):
    print("\nLoot:")
    for run in runs[session:]:
        if run["note"]:
            print(run["note"])
