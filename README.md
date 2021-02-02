# programming_timelapse.py  
Click the image below to view a short demostration.  
[![Alt text](https://img.youtube.com/vi/5veQqFvsMJc/0.jpg)](https://www.youtube.com/watch?v=5veQqFvsMJc)  
I hate editing so I made this tool to auto timelapse my programming sessions and spit out an avi video. The example above really under sells how cool the resulting timelapse is due to the gif's length and compression. The script is pretty simple and the code is kinda gross in my opinion. I wrapped everything in a class for some reason because I think someone told me that was good practice at some point, but to me it's gross so I'll probably never do it again. If you feel like fixing my gross code or adding features please do so! As of right now the script only works on linux. For an Unix version the get_window_info() function would need to be rewritten. As far as I know the rest should be cross-platform.

# Setup
Before use a "few" dependencies must be installed. This command should install them all:  
```pip install pywin32 keyboard numpy opencv-python pyautogui argparse```  
I can't test if this works so if it doesn't please create an issue. Thanks!

# Use
The script is simple to use. It will automagically timelapse the screen whenever the right window is on the right monitor. The windows are defined by their executable name. By default I have it set to capture WindowsTerminal.exe and firefox.exe, if you wish to capture other software simply remove the undesired executable names and add your own. The script also only timelapse when typing, the time spent capturing after typing can be adjusted in the script as well.  
To run the the script type the following in the console:  
```py programming_timelapse.py -s <desired speed> -n <desired name>```  
Note the name should NOT include an extension! So if you put in "-n test" the outputted file will be test.avi. The script takes a screenshot every speed/60 seconds.

# Future
I would like to add cross platform capabilities, but I don't know if I'll get around to that. I'd also like to add the abilitie to concatenate frames onto an already existing video file. I also kind of hate the state of the code right now and would like to make it more readable. I would like to do these things, but for now it works for me and that is good enough.
