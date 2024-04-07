from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

sleep(5)
iter = 0

while True:
    iter += 1
    print(iter)
    
    keyboard.type("v")

    sleep(0.5)

