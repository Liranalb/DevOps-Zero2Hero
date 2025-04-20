<!-- omit in toc -->
# Jenkins Android Device Automation Lab

---

<div align="center">
  <img src="../../resources/images/jenkins/android_automation.webp" alt="Android Device Automation with Jenkins" width="500">
</div>

---

- This lab demonstrates how to use Jenkins to automate Android device interactions via USB using Python and `uiautomator2`
- Learn how to create automated tests and device control through Jenkins pipelines
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
- [Jenkins Configuration](#jenkins-configuration)
  - [Setting Up Android Device as a Node](#setting-up-android-device-as-a-node)
  - [Creating Individual Jobs](#creating-individual-jobs)
  - [Creating a Pipeline Job](#creating-a-pipeline-job)
  - [Troubleshooting](#troubleshooting)

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

## Jenkins Configuration

### Setting Up Android Device as a Node

1. **Access Jenkins Dashboard**:
   - Open your web browser and go to `http://localhost:8080` (or your Jenkins server URL)
   - Log in with your credentials

2. **Add Android Device as a Node**:
   - Click on "Manage Jenkins" in the left sidebar
   - Select "Manage Nodes and Clouds"
   - Click "New Node"
   - Enter a name (e.g., "android-device")
   - Select "Permanent Agent" and click "OK"
   - Configure the node:
     - Number of executors: 1
     - Remote root directory: `/home/jenkins/android` (or your preferred directory)
     - Labels: `android` (this will be used to identify the node)
     - Usage: "Only build jobs with label expressions matching this node"
     - Launch method: "Launch agent via Java Web Start"
   - Click "Save"

3. **Connect the Node**:
   - After saving, you'll see a "Launch" button
   - Click it to download the agent.jar file
   - Run the agent on the machine where your Android device is connected:
     ```bash
     java -jar agent.jar -jnlpUrl http://your-jenkins-url/computer/android-device/jenkins-agent.jnlp -secret YOUR_SECRET
     ```
   - The node should now appear as "connected" in Jenkins

### Creating Individual Jobs

1. **Create a New Job**:
   - Click "New Item" on the Jenkins dashboard
   - Enter a name (e.g., "android-browser-test")
   - Select "Freestyle project"
   - Click "OK"

2. **Configure the Job**:
   - Under "General":
     - Check "Restrict where this project can be run"
     - Enter `android` in the label expression
   - Under "Source Code Management":
     - Select "Git"
     - Enter your repository URL
   - Under "Build":
     - Click "Add build step"
     - Select "Execute shell" (Linux/macOS) or "Execute Windows batch command" (Windows)
     - Enter the build command:
       ```bash
       # Activate virtual environment
       source venv/bin/activate
       
       # Run the script
       python scripts/browser_test.py
       ```
   - Click "Save"

3. **Repeat for Other Scripts**:
   - Create similar jobs for other scripts (e.g., "android-youtube-test", "android-device-controls")
   - Each job should:
     - Use the same node restriction (`android` label)
     - Activate the virtual environment
     - Run its specific script

### Creating a Pipeline Job

1. **Create Pipeline Job**:
   - Click "New Item" on the Jenkins dashboard
   - Enter a name (e.g., "android-automation-pipeline")
   - Select "Pipeline"
   - Click "OK"

2. **Configure Pipeline**:
   - Under "Pipeline":
     - Select "Pipeline script"
     - Enter the following script:
       ```groovy
       pipeline {
           agent {
               label 'android'
           }
           stages {
               stage('Browser Test') {
                   steps {
                       build job: 'android-browser-test'
                   }
               }
               stage('YouTube Test') {
                   steps {
                       build job: 'android-youtube-test'
                   }
               }
               stage('Device Controls') {
                   steps {
                       build job: 'android-device-controls'
                   }
               }
           }
       }
       ```
   - Click "Save"

3. **Run the Pipeline**:
   - Click "Build Now" on the pipeline job
   - Jenkins will:
     1. Run the browser test
     2. Run the YouTube test
     3. Run the device controls test
   - You can monitor the progress in the "Build History" section

### Troubleshooting

1. **Node Connection Issues**:
   - Verify the Android device is connected and authorized
   - Check if ADB is running: `adb devices`
   - Ensure the virtual environment is activated

2. **Job Execution Issues**:
   - Check the console output for error messages
   - Verify all required packages are installed in the virtual environment
   - Ensure the scripts have proper permissions

3. **Pipeline Issues**:
   - Verify all individual jobs exist and are configured correctly
   - Check if the node label matches in all jobs
   - Ensure the virtual environment path is correct

--- 