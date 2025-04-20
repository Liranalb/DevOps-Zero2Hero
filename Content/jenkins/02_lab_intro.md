<!-- omit in toc -->
# Jenkins Android UIAutomation Lab

---

<div align="center">
  <img src="../../resources/images/jenkins/android_automation.webp" alt="Android Automation with Jenkins" width="500">
</div>

---

- This lab demonstrates how to use Jenkins to control an Android phone via USB using Python and `uiautomator2`
- Learn how to automate common Android device interactions through Jenkins pipelines
- Includes setup instructions, prerequisites, and example automation tasks

---

- [Prerequisites](#prerequisites)
  - [Host Requirements (Jenkins Agent)](#host-requirements-jenkins-agent)
  - [Android Device Requirements](#android-device-requirements)
  - [ADB Installation](#adb-installation)
    - [macOS](#macos)
    - [Ubuntu / Debian](#ubuntu--debian)
    - [Verify ADB Installation](#verify-adb-installation)
- [Initial Setup](#initial-setup)
  - [Connect Android Device](#connect-android-device)
    - [Device Configuration](#device-configuration)
  - [Install Dependencies](#install-dependencies)
  - [Initialize Device Communication](#initialize-device-communication)
- [Pipeline Actions](#pipeline-actions)
  - [Browser Automation](#browser-automation)
  - [App Interaction](#app-interaction)
  - [Device Controls](#device-controls)

## Prerequisites

### Host Requirements (Jenkins Agent)
- Python 3 installed
- Required pip packages (to be installed in virtual environment)
- ADB (Android Debug Bridge) installed
- Jenkins installed and running

### Android Device Requirements
- Developer Mode enabled
- USB Debugging enabled
- ADB authorization accepted
- USB cable for connection

### ADB Installation

#### macOS
Install ADB using Homebrew:
```bash
brew install android-platform-tools
```

#### Ubuntu / Debian
Install ADB using apt:
```bash
sudo apt update
sudo apt install -y android-tools-adb
```

#### Verify ADB Installation
After installation, verify ADB is working by running:
```bash
adb version
```
You should see the ADB version number displayed.

## Initial Setup

### Connect Android Device

#### Device Configuration
1. Enable Developer Options:
   - Go to Settings > About Phone
   - Find "Build Number" and tap it 7 times
   - You'll see a message "You are now a developer!"

2. Enable USB Debugging:
   - Go to Settings > System > Developer Options
   - Enable "USB Debugging"
   - If prompted, confirm the action

3. Connect the Device:
   - Use a USB cable to connect your Android device to the Jenkins agent
   - When prompted on the device, select "Allow USB debugging"
   - Check "Always allow from this computer" if you want to skip this prompt in the future
   - Tap "Allow" to grant USB debugging permission

4. Verify USB Connection Mode:
   - When connected, pull down the notification shade
   - Look for "USB for..." or "Charging this device via USB"
   - Tap it and select "File Transfer" or "MTP" mode

5. Verify ADB Connection:
   ```bash
   adb devices
   ```
   You should see your device listed with a "device" status. If you see "unauthorized", check the device screen for the USB debugging authorization prompt.

6. Troubleshooting:
   - If the device is not detected:
     - Try a different USB cable
     - Check if USB debugging is enabled
     - Restart ADB server: `adb kill-server && adb start-server`
     - Reconnect the device
   - If "unauthorized" persists:
     - Revoke USB debugging authorizations in Developer Options
     - Disconnect and reconnect the device
     - Accept the authorization prompt on the device

### Install Dependencies
1. Create and activate a Python virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```

2. Install required packages in the virtual environment:
   ```bash
   pip install -U uiautomator2 adbutils requests
   ```

3. Verify the installation:
   ```bash
   pip list
   ```
   You should see the installed packages in the list.

4. Deactivate the virtual environment when done:
   ```bash
   deactivate
   ```

Note: Make sure to activate the virtual environment before running any Python scripts or commands that require these packages.

### Initialize Device Communication
Run the initialization script (make sure the virtual environment is activated):
```bash
python scripts/init_device.py
```
This script will:
- Install necessary apps on the device
- Set up device communication
- Verify the connection

## Pipeline Actions

### Browser Automation
- Open Chrome browser
- Navigate to specified URLs
- Perform web interactions

### App Interaction
- Launch YouTube app
- Search for videos
- Play/pause content

### Device Controls
- Simulate swipes
- Perform button presses
- Handle device orientation
- Capture screenshots

--- 