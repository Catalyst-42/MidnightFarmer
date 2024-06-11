from pynput import keyboard
from time import time, sleep
import os
from json import dumps

from pynput.keyboard import Key, Controller
controller = Controller()

s = 1
m = 60*s
h = 60*m
d = 24*h

runs = []
open("save.py", "a")
from save import *

state = "begin"
run = {
    "begin": None,
    "end": None,
    "note": ""
}

def re_enter():
    sleep(1)

    controller.press(Key.esc)
    controller.release(Key.esc)
    sleep(0.05)
    
    for _ in range(5):
        controller.press(Key.down)
        controller.release(Key.down)
        sleep(0.05)

    controller.press(Key.enter)
    controller.release(Key.enter)
    sleep(0.05)

    controller.press(Key.up)
    controller.release(Key.up)

    controller.press(Key.enter)
    controller.release(Key.enter)
    
    sleep(6)

    controller.press(Key.enter)
    controller.release(Key.enter)
    sleep(0.05)

    controller.press(Key.enter)
    controller.release(Key.enter)

def on_press(key):
    global state, runs, run
    
    if state == "run" and key == keyboard.KeyCode.from_char('y'):
        state = "note"

    elif state == "note":
        try:
            run["note"] += key.char

        except AttributeError:
            if key in (keyboard.Key.backspace, keyboard.Key.delete):
                run["note"] = run["note"][:-1]
            if key == keyboard.Key.space:
                run["note"] += " "
        
    if state == "begin" and key == keyboard.KeyCode.from_char("."):
        state = "run"
        run = {
            "begin": time(),
            "end": None,
            "note": "",
        }

    elif state == "run" and key == keyboard.KeyCode.from_char(".") or state == "note" and key == keyboard.Key.enter:
        run["end"] = time()
        runs.append(run)

        run = {
            "begin": time(),
            "end": None,
            "note": "",
        }

        state = "re_entering"
        re_enter()
        state = "run"

    elif key == keyboard.Key.shift_r:
        print("exiting")
        run["end"] = time()
        runs.append(run)

        return False

    print(f"key: {key} | state: {state} | run: r{len(runs)}: {run}")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Ended, log:")
print(runs)

with open("save.py", "w", encoding="utf-8") as file:
    file.write(f"runs = ")
    file.write(dumps(runs, indent=4))
