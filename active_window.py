import win32api
import win32process
import win32gui

import time
from datetime import date
import os

import keyboard
import pyautogui
import argparse

speed = 0
is_typing = False
typing_time = 1
now = time.time()
future = now + typing_time
take_picture = now + speed/60
directory = "screenshots"

timelapse_windows = ["WindowsTerminal.exe", "firefox.exe"]
timelapse_monitor = 1

def get_window_info():
    fg_window = win32gui.GetForegroundWindow()
    monitor = win32api.MonitorFromWindow(fg_window)
    t, p = win32process.GetWindowThreadProcessId(fg_window)

    try:
        process = win32api.OpenProcess(0x0410, False, p)
        monitor_id = int(win32api.GetMonitorInfo(monitor).get('Device')[11:])
        window_path = win32process.GetModuleFileNameEx(process, 0)
    except:
        return { "window": "\\*.exe", "monitor": None }
    return  { "window" : window_path, "monitor" : monitor_id}

def get_name_from_path(path):
    name = ""
    for n in range(len(path)-1, 0, -1):
        if(path[n] == '\\'):
            break
        else:
            name = path[n] + name
    return name

def screenshot():
    global now
    global directory
    screenshot = pyautogui.screenshot()
    screenshot.save(r'{}\{}-{}.png'.format(directory, date.today(), now))

def on_keypress(key):
    global now
    global future
    global typing_time
    global is_typing
    future = now + typing_time
    is_typing = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autotimelapse for programming sessions")
    parser.add_argument("--speed", "-s", dest="speed", required = True, type = int)
    parser.add_argument("--dir", "-d", dest="directory", required = True, type = str)
    args = parser.parse_args()

    speed = args.speed
    directory = args.directory
    try:
        os.makedirs(directory)
    except OSError as e:
        pass
    
    keyboard.on_press(on_keypress)
    try:
        while True:
            now = time.time()
            info = get_window_info()
            window_name = get_name_from_path(info.get("window"))
            monitor = info.get("monitor")
            if(window_name != "*.exe"):
                if(window_name in timelapse_windows and monitor == timelapse_monitor and is_typing):
                    if(now > take_picture):
                        screenshot() 
                        take_picture = now + speed/60
                        print("took picture")
            if(now > future and is_typing):
                is_typing = False
    except KeyboardInterrupt:
        exit()
