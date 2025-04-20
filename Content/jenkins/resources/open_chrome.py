import uiautomator2 as u2
import time

d = u2.connect()
d.press("home")
time.sleep(1)
d.app_start("com.android.chrome")
time.sleep(2)
d(resourceId="com.android.chrome:id/url_bar").click()
d.send_keys("https://www.google.com\n", clear=True)
print("Opened Chrome with Google.")
