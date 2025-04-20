import uiautomator2 as u2
import time

d = u2.connect()
d.app_start("com.google.android.youtube")
print("YouTube app launched.")
