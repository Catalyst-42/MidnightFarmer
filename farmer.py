from pynput import keyboard
from time import time, sleep
from json import dumps
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

def re_enter():
    sleep(0.5)

    controller.press(Key.esc)
    controller.release(Key.esc)
    sleep(0.01)
    
    for _ in range(5):
        controller.press(Key.down)
        controller.release(Key.down)
        sleep(0.01)

    controller.press(Key.enter)
    controller.release(Key.enter)
    sleep(0.01)

    controller.press(Key.up)
    controller.release(Key.up)

    controller.press(Key.enter)
    controller.release(Key.enter)
    
    sleep(4.5)

    controller.press(Key.enter)
    controller.release(Key.enter)
    sleep(0.01)

    controller.press(Key.enter)
    controller.release(Key.enter)

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
            global free
            free = True
            return False

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

            state = "action_re_enter"
            re_enter()
            state = "run"

        # Pause mode
        case ("run", "p" | "з"):
            state = "pause"

            run["time"] += time() - timestamp
            state = "action_pause"
            pause()
            state = "pause"

        case ("pause", "p" | "з"):
            pause()
            timestamp = time()
            state = "run"

        # Note mode
        case ("run", "y" | "н"):
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

listener = keyboard.Listener(on_press=on_press)
listener.start()

free = False
while not free:
    pass

with open("save.py", "w", encoding="utf-8") as file:
    file.write(f"runs = ")
    file.write(dumps(runs, indent=4))

print("Loot")
for run in runs[session:]:
    if run["note"]:
        print(run["note"])
