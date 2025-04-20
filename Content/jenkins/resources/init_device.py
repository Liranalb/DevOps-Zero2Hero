import uiautomator2 as u2
import time

print("Initializing device connection...")
d = u2.connect()  # Automatically connects to first USB device
print(f"Connected to: {d.device_info}")

# Unlock screen if necessary
if not d.screen_on():
    d.screen_on()
    print("Waking up the screen...")
time.sleep(1)
d.press("home")
print("Device ready.")
