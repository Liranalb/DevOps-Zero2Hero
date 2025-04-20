import uiautomator2 as u2
import time

d = u2.connect()
print("Swiping down from top to open notifications.")
d.swipe(500, 0, 500, 1000, 0.1)
