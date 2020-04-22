from wmi import WMI
from pynput import mouse, keyboard
from threading import Thread
# https://pynput.readthedocs.io/en/latest/index.html

def keyboard_control():
    # keyboard exit function
    def on_release(key):
        exit = [keyboard.Key.esc, keyboard.Key.space]
        if key in exit:
            # Stop listener
            return False
    # Collect events until released
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
    mouse.Controller().release(mouse.Button.left)


def mouse_control():
    # mouse exit function
    def on_click(x, y, button, pressed):
        if not pressed:
            # Stop listener
            return False
    # Collect events until released
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    keyboard.Controller().release(keyboard.Key.space)



if __name__ == '__main__':
    w = WMI(namespace=r'root\wmi')

    a = w.WmiMonitorBrightness()[0]
    cur_brightness = a.CurrentBrightness

    m = w.WmiMonitorBrightnessMethods()[0]
    m.WmiSetBrightness(Brightness=0, Timeout=0)
    
    t1 = Thread(target=keyboard_control)
    t2 = Thread(target=mouse_control)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    m.WmiSetBrightness(Brightness=cur_brightness, Timeout=0)


