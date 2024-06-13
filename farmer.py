from time import time, sleep
from threading import Thread
import tomllib

from pynput.keyboard import Controller, Listener, Key
keyboard = Controller()

# Setup
with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)

session = []
tag = settings["DEFAULT_TAG"]

timestamp = 0
state = "begin"

run = {
    "time": 0,
    "note": ""
}

class KEY:
    BEGIN = settings["KEY"]["BEGIN"]
    BEGIN_ALT = settings["KEY"]["BEGIN_ALT"]

    PAUSE = settings["KEY"]["PAUSE"]
    PAUSE_ALT = settings["KEY"]["PAUSE_ALT"]

    NOTE = settings["KEY"]["NOTE"]
    NOTE_ALT = settings["KEY"]["NOTE_ALT"]

class TIMEOUT:
    SMALL = settings["TIMEOUT"]["SMALL"]
    MEDIUM = settings["TIMEOUT"]["MEDIUM"]
    BIG = settings["TIMEOUT"]["BIG"]

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
    Thread(
        target=inner,
        args=(
            function,
            begin_state,
            final_state,
            start_delay
        )
    ).start()

def on_press(key):
    global timestamp, state, session, run

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
            session.append(run)

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
    print(f"run: {len(session) + 1} {run['note']}".ljust(20))

with Listener(on_press=on_press) as listener:
    listener.join()

# Extend save
with open("save.toml", "a+") as f:
    for run in session:
        f.write(f"[[{tag}]]\n")
        f.write(f"time = {run['time']}\n")
        f.write(f'note = "{run['note']}"\n\n')

# Load all save
with open("save.toml", "rb") as f:
    save = tomllib.load(f)

# Stats by session
if len(session):
    print("\nSession")
    print(f"Runs: {len(session)}")
    print(f"Average time: {round(sum([run['time'] for run in session]) / len(session))}s")

    # Loot
    if any([run["note"] for run in session]) :
        print("\nLoot")
        for run in session:
            if run["note"]:
                print(run["note"])

# Global stats
if tag in save:
    print(f"\nGlobal")
    print(f"Runs: {len(save[tag])}")
    print(f"Average time: {round(sum([run['time'] for run in save[tag]]) / len(save[tag]))}s")
