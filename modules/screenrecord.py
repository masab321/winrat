import pyautogui
import time
import os
import numpy as np
import cv2

DURATION = 10
FPS = 12.0

def run(file_name, reload_interval=86400):
    if not os.path.isdir("data"):
        os.makedirs("data")
    file_name = f"{file_name}.avi"

    screen_size = tuple(pyautogui.size())
    codec = cv2.VideoWriter_fourcc(*"XVID")
    video_out = cv2.VideoWriter(f"data/{file_name}", codec, FPS, (screen_size))

    for _ in range(int(min(DURATION, reload_interval) * FPS)):
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_out.write(frame)
    
    cv2.destroyAllWindows()
    video_out.release()

    time.sleep(max(reload_interval - DURATION, 0))

    return f"stored:{file_name}"
    
if __name__ == "__main__":
    r = run("s13", 5)
    print(r)