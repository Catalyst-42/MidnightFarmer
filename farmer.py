from time import time, sleep
from json import dumps
from threading import Thread

from pynput.keyboard import Controller, Listener, Key
keyboard = Controller()

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
    BIG = 5

# Shortcut actions
def re_enter():
    keyboard.tap(Key.esc)
    sleep(TIMEOUT.SMALL)
    
    for _ in range(5):
        keyboard.tap(Key.down)
        sleep(TIMEOUT.SMALL)

    keyboard.tap(Key.enter)
    sleep(TIMEOUT.SMALL)

    keyboard.tap(Key.up)
    keyboard.tap(Key.enter)
    
    sleep(TIMEOUT.BIG)

    keyboard.tap(Key.enter)
    sleep(TIMEOUT.SMALL)

    keyboard.tap(Key.enter)

def pause():
    keyboard.tap(Key.esc)

def shortcut(function, begin_state, final_state, start_delay=0):
    def inner(function, begin_state, final_state, start_delay):
        global state

        state = begin_state
        sleep(start_delay)
        function()
        state = final_state
    
    # Execute shortcut without delays in main script
    Thread(target=inner, args=(function, begin_state, final_state, start_delay)).start()

def on_press(key):
    global timestamp, state, runs, run

    # TODO:
    # Выбор фала сохранения
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
            
            shortcut(re_enter, "re_enter", "run", TIMEOUT.MEDIUM if state == "note" else TIMEOUT.SMALL)

        # Pause mode
        case ("run", "esc"):
            run["time"] += time() - timestamp
            state = "pause"

        case ("run", KEY.PAUSE | KEY.PAUSE_ALT):
            run["time"] += time() - timestamp
            shortcut(pause, "pausing", "pause")

        case ("pause", KEY.PAUSE | KEY.PAUSE_ALT | "enter" | "esc" | "space"):
            timestamp = time()
            shortcut(pause, "unpausing", "run")

        # Note mode
        case ("run", KEY.NOTE | KEY.NOTE_ALT):
            state = "note"
        
        case "note", "esc":
            timestamp = time()
            run["note"] = ""
            state = "run"

        case "note", "backspace":
            run["note"] = run["note"][:-1]

        case "note", "space":
            run["note"] += " "

        case "note", _:
            if hasattr(key, 'char'):
                run["note"] += key.char

    print(f"key: {key}".ljust(20), end=" | ")
    print(f"state: {state}".ljust(20), end=" | ")
    print(f"run: {len(runs) + 1} {run['note']}".ljust(20))

with Listener(on_press=on_press) as listener:
    listener.join()

with open("save.py", "w", encoding="utf-8") as file:
    file.write(f"runs = ")
    file.write(dumps(runs, indent=4, ensure_ascii=False))

# Stats by session
if len(runs[session:]):
    print("\nSession")
    print(f"Runs: {len(runs) - session}")
    print(f"Average time: {round(sum([run['time'] for run in runs[session:]]) / len(runs[session:]))}s")

    # Loot
    if any([run["note"] for run in runs[session:]]) :
        print("\nLoot:")
        for run in runs[session:]:
            if run["note"]:
                print(run["note"])

# Global stats
print("\nGlobal")
print(f"Runs: {len(runs)}")
print(f"Average time: {round(sum([run['time'] for run in runs]) / len(runs))}s")
