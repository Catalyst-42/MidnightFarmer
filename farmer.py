from pynput import keyboard
from time import time, sleep
import os

from pynput.keyboard import Key, Controller
keyboard = Controller()

s = 1
m = 60*s
h = 60*m
d = 24*h

state = "begin"
runs = []
run = {
    "begin": None,
    "end": None,
    "note": ""
}

def re_enter():
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    
    for _ in range(6):
        keyboard.press(Key.down)
        keyboard.release(Key.down)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    sleep(3)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def on_press(key):
    global state, runs, run

    if key == keyboard.Key.shift_r:
        return False
    
    if state == "run" and key == keyboard.KeyCode.from_char('n'):
        state = "note"
    
    elif state == "note":
        try:
            run["note"] += key.char
        except AttributeError:
            if key in (keyboard.Key.backspace, keyboard.Key.delete):
                run["note"] = run["note"][:-1]
            if key == keyboard.Key.space:
                run["note"] += " "

    if key == keyboard.Key.enter:
        match state:
            case "begin":
                state = "run"
                run = {
                    "begin": time(),
                    "end": None,
                    "note": "",
                }

            case "run" | "note":
                run["end"] = time()
                runs.append(run)

                run = {
                    "begin": time(),
                    "end": None,
                    "note": "",
                }

                re_enter()

    os.system("clear")
    print(f"key: {key} | state: {state} | run: {run}")
    print(f"now on {len(runs)} run")
                
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Ended, log:")
print(runs)
