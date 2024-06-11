from pynput import keyboard
from time import time, sleep
import os

from pynput.keyboard import Key, Controller
controller = Controller()

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

    if key == keyboard.Key.shift_r:
        state = "exit"
    
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

    if key == keyboard.KeyCode.from_char(".") or key == keyboard.Key.enter and state == "note":
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

                state = "re_entering"
                re_enter()
                state = "run"

            case "exit":
                run["end"] = time()
                runs.append(run)

                return False

    os.system("clear")
    print(f"key: {key} | state: {state} | run: {run}")
    print(f"now on {len(runs)} run")
                
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Ended, log:")
print(runs)
