@echo off
set /p framerate=Enter framerate:
set /p directory=Enter directory:
for /r %%a in (%directory%\*.png) do (
    echo file '%%a' >> images.txt
)
ffmpeg.exe -r %framerate% -f concat -safe 0 -i images.txt -c:v libx264 -pix_fmt yuv420p %directory%\video.mp4
del /q images.txt