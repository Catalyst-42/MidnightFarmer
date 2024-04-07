from time import time
import datetime
import curses

timestamp = time()
runs = []

s = curses.initscr()
sh, sw = s.getmaxyx()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.curs_set(0)

w = curses.newwin(sh, sw, 0, 0)
w.keypad(True); w.timeout(1000)

while True:
    w.clear()

    delta = round((time() - timestamp))
    w.addstr(f"{len(runs) + 1} 0{datetime.timedelta(seconds=delta)} ")
    if len(runs): w.addstr(f"0{datetime.timedelta(seconds=round(sum(runs) / len(runs)))}", curses.color_pair(1))
    else: w.addstr(f"--:--:--")

    for run in runs[:-sh:-1]:
        w.addstr(f"\n{(len(str(len(runs) + 1))) * ' '} 0{datetime.timedelta(seconds=run)}")

    try: key = w.get_wch()
    except: key = ''

    if  key == '\n': # enter
        delta = round((time() - timestamp))
        runs.append(delta)
        timestamp = time()

    elif key == 'p': # pause
        w.timeout(-1)
        w.clear()

        w.addstr(f"{len(runs) + 1}  paused  ")
        if len(runs): w.addstr(f"0{datetime.timedelta(seconds=round(sum(runs) / len(runs)))}", curses.color_pair(1))

        for run in runs[:-sh:-1]:
            w.addstr(f"\n{(len(str(len(runs) + 1))) * ' '} 0{datetime.timedelta(seconds=run)}")

        w.getch()
        timestamp = time()
        w.timeout(1000)

    elif key == '\x1b': # escape
        curses.endwin()
        if len(runs): 
            print(f"Среднее за {len(runs)}: 0{datetime.timedelta(seconds=round(sum(runs) / len(runs)))}")
        break

# save data to file
with open("save.txt", 'a') as file:
    for run in runs: file.write(f"{run}\n")

# get data for all time
with open("save.txt", 'r') as file:
    runs = [int(run) for run in file.readlines()]
    if len(runs): 
        print(f"Среднее за {len(runs)}: 0{datetime.timedelta(seconds=round(sum(runs) / len(runs)))}")
