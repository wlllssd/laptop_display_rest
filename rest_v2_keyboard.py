import wmi
from pynput import keyboard
# https://pynput.readthedocs.io/en/latest/index.html

def main():
	w = wmi.WMI(namespace=r'root\wmi')
	m = w.WmiMonitorBrightnessMethods()[0]

	m.WmiSetBrightness(Brightness=0, Timeout=5)

	# keyboard exit function
	def on_release(key):
	    exit = [keyboard.Key.esc, keyboard.Key.space]
	    if key in exit:
	        # Stop listener
	        return False
	# Collect events until released
	with keyboard.Listener(on_release=on_release) as listener:
	    listener.join()
	    
	m.WmiSetBrightness(Brightness=100, Timeout=5)

if __name__ == '__main__':
	main()
	

