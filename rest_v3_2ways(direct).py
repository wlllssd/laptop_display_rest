from wmi import WMI
from pynput import mouse, keyboard
# https://pynput.readthedocs.io/en/latest/index.html

def on_release(key):
    exit = [keyboard.Key.esc, keyboard.Key.space]
    if key in exit:
        mouse.Controller().release(mouse.Button.left)
        # Stop listener
        return False
def on_click(x, y, button, pressed):
    if not pressed:
        keyboard.Controller().release(keyboard.Key.space)
        # Stop listener
        return False

def listen_input():
    listener1 = keyboard.Listener(on_release=on_release)
    listener2 = mouse.Listener(on_click=on_click)
    listener1.start()
    listener2.start()
    listener1.join()
    listener2.join() 


if __name__ == '__main__':
    w = WMI(namespace=r'root\wmi')
    m = w.WmiMonitorBrightnessMethods()[0]
    m.WmiSetBrightness(Brightness=0, Timeout=5)

    listen_input()

    m.WmiSetBrightness(Brightness=90, Timeout=5)

