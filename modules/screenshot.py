import pyautogui
import time
import os

def run(file_name, reload_interval=86400):
    file_name = f"{file_name}.jpg"
    screen = pyautogui.screenshot()
    if not os.path.isdir("data"):
        os.makedirs("data")
    screen.save(f"data/{file_name}")

    time.sleep(reload_interval)

    return f"stored:{file_name}"

if __name__ == "__main__":
    r = run("s1")
    print(r)