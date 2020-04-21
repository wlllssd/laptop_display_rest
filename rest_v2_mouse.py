from wmi import WMI
from pynput import mouse
# https://pynput.readthedocs.io/en/latest/index.html

def main():
	w = WMI(namespace=r'root\wmi')
	m = w.WmiMonitorBrightnessMethods()[0]

	m.WmiSetBrightness(Brightness=0, Timeout=5)

	# mouse exit function
	def on_click(x, y, button, pressed):
	    if not pressed:
	        # Stop listener
	        return False
	# Collect events until released
	with mouse.Listener(on_click=on_click) as listener:
	    listener.join()
	    
	m.WmiSetBrightness(Brightness=100, Timeout=5)

if __name__ == '__main__':
	main()