# Built in libraries used for tracking time and creating directories
import time
import os

# used to get info about the current window and monitor
import win32api
import win32process
import win32gui

# used to monitor keyboard input
import keyboard
# used to convert screenshots to a numpy array
import numpy as np
# used to create video
import cv2
# used to capturn screenshot
import pyautogui
# used to parse the provided arguments
import argparse

class timelapser:
    def __init__(self, resolution, speed, name, timelapse_windows, timelapse_monitor):
        self.RESOLUTION = resolution
        self.speed = speed
        self.name = name 
        self.timelapse_windows = timelapse_windows
        self.timelapse_monitor = timelapse_monitor

        self.is_typing = False
        # time to stop capturing after a key press
        self.typing_time = 1
        self.now = time.time()
        self.future = self.now + self.typing_time
        self.picture_time = self.now + self.speed/60
        self.frame_count = 0

        keyboard.on_press(self.on_keypress)

        fourcc = cv2.VideoWriter_fourcc(*"XVID")

        # change the 60.0 here to adjust framerate
        self.out = cv2.VideoWriter(f"{self.name}.avi", fourcc, 60.0, (self.RESOLUTION))

    def __del__(self):
        cv2.destroyAllWindows()
        self.out.release()

    def timelapse(self):
        try:
            self.now = time.time()
            info = self.get_window_info()
            window_name = info.get("window")
            monitor = info.get("monitor")
            if(window_name != "*.exe"):
                if(window_name in self.timelapse_windows and monitor == self.timelapse_monitor and self.is_typing):
                    if(self.now > self.picture_time):
                        self.screenshot() 
                        self.picture_time = self.now + self.speed/60
                        self.frame_count += 1
                        print(f'{self.frame_count} frames captured.')
            if(self.now > self.future and self.is_typing):
                self.is_typing = False
        except KeyboardInterrupt:
            print(f"Timelapse completed. {name}.avi has been saved with a total of {self.frame_count} frames.")
            exit()

    def get_window_info(self):
        fg_window = win32gui.GetForegroundWindow()
        monitor = win32api.MonitorFromWindow(fg_window)
        t, p = win32process.GetWindowThreadProcessId(fg_window)
        try:
            process = win32api.OpenProcess(0x0410, False, p)
            monitor_id = int(win32api.GetMonitorInfo(monitor).get('Device')[11:])
            window_name = win32process.GetModuleFileNameEx(process, 0)
            window_name = self.get_exe_from_path(window_name)
        except:
            return { "window": "\\*.exe", "monitor": None }
        return  { "window" : window_name, "monitor" : monitor_id}
    
    def get_exe_from_path(self, path):
        name = ""
        for n in range(len(path)-1, 0, -1):
            if(path[n] == '\\'):
                break
            else:
                name = path[n] + name
        return name

    def screenshot(self):
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.out.write(frame)

    def on_keypress(self, key):
        self.future = self.now + self.typing_time
        self.is_typing = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autotimelapse for programming sessions")
    parser.add_argument("--speed", "-s", dest="speed", required = True, type = int)
    parser.add_argument("--name", "-n", dest="name", required = True, type = str)
    args = parser.parse_args()


    speed = args.speed
    name = args.name

    # adjust desired windows to capture in this array
    windows = ["WindowsTerminal.exe", "firefox.exe"]
    # desired monitor to capture
    monitor = 1

    t = timelapser((1920, 1080), speed, name, windows, monitor)
    while True:
        t.timelapse()
