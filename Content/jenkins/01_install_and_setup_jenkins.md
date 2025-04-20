<!-- omit in toc -->
# Jenkins Installation and Setup

---

<div align="center">
  <img src="../../resources/images/jenkins/jenkins_banner.webp" alt="Jenkins Installation" width="500">
</div>

---

- This guide covers the installation and initial setup of Jenkins on macOS and Linux systems
- Detailed instructions for both Homebrew and WAR file installation methods
- Includes prerequisites, installation steps, and initial configuration

---

- [Prerequisites](#prerequisites)
  - [macOS](#macos)
  - [Ubuntu / Debian](#ubuntu--debian)
- [Installing Jenkins on macOS](#installing-jenkins-on-macos)
  - [Method 1: Homebrew Installation (macOS)](#method-1-homebrew-installation-macos)
    - [Install Homebrew](#install-homebrew)
    - [Install Jenkins using Homebrew](#install-jenkins-using-homebrew)
    - [Start the Jenkins service](#start-the-jenkins-service)
    - [Verify Jenkins is running](#verify-jenkins-is-running)
  - [Method 2: Running Jenkins from the .war file (macOS or Cross-Platform)](#method-2-running-jenkins-from-the-war-file-macos-or-cross-platform)
    - [Download the Jenkins WAR](#download-the-jenkins-war)
    - [Run the WAR file with Java](#run-the-war-file-with-java)
    - [Access Jenkins UI](#access-jenkins-ui)
- [Installing Jenkins on Linux (Ubuntu/Debian example)](#installing-jenkins-on-linux-ubuntudebian-example)
  - [Method 1: Using apt Package Manager (Debian/Ubuntu)](#method-1-using-apt-package-manager-debianubuntu)
  - [Method 2: Running Jenkins from the .war file (Linux)](#method-2-running-jenkins-from-the-war-file-linux)
- [Initial Admin Password and Unlocking Jenkins](#initial-admin-password-and-unlocking-jenkins)
- [Basic Configuration and Jenkins Interface Overview](#basic-configuration-and-jenkins-interface-overview)
  - [Initial Setup and Configuration](#initial-setup-and-configuration)

## Prerequisites

Jenkins runs on Java. Ensure you have a Java Development Kit (JDK) installed (JDK 11 or newer is recommended) on your system. You can check with:
```bash
java -version
```
If Java is not installed, install it (e.g., via Homebrew or apt, or from the OpenJDK distributions) before proceeding.

### macOS
```bash
brew install openjdk@11

# Add it to the shell (for zsh or bash)
echo 'export PATH="/usr/local/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y openjdk-11-jdk
```

## Installing Jenkins on macOS

On macOS, Jenkins can be installed easily using Homebrew (a package manager for macOS). Alternatively, you can run Jenkins using its standalone .war file.

### Method 1: Homebrew Installation (macOS)

#### Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Jenkins using Homebrew
```bash
brew update
brew install jenkins-lts
```

#### Start the Jenkins service
After installation, start Jenkins as a background service:
```bash
brew services start jenkins-lts
```
This will launch Jenkins listening on the default port 8080.

#### Verify Jenkins is running
Open a browser and navigate to `http://localhost:8080`. You should see the Jenkins initial setup screen (which will prompt for an initial admin password, covered in the [Basic Configuration](#basic-configuration-and-jenkins-interface-overview) section below).

**Homebrew notes:**
- By default, Homebrew sets the Jenkins home directory to `/usr/local/var/jenkins_home`
- Jenkins will run under the current Mac user account
- Logs can usually be found under `/usr/local/var/log/jenkins.log`
- On first run, Jenkins will generate an admin password (in the secrets folder of the Jenkins home) which we'll use during setup

### Method 2: Running Jenkins from the .war file (macOS or Cross-Platform)

The .war file method is a standard way to run Jenkins and works on any system with Java installed (macOS, Linux, or Windows):

#### Download the Jenkins WAR
Go to the Jenkins download page and download the latest stable jenkins.war file. Alternatively, use wget or curl in a terminal:
```bash
wget -O jenkins.war https://get.jenkins.io/war-stable/latest/jenkins.war
```
This command downloads the latest stable Jenkins WAR to the current directory.

#### Run the WAR file with Java
Execute the WAR using the java -jar command:
```bash
java -jar jenkins.war
```
This will start Jenkins on port 8080 by default. The console output will show log information. Keep this terminal open to keep Jenkins running. (To run it in the background, you might use nohup or run as a service, but for now running in foreground is fine for testing.)

#### Access Jenkins UI
Once the WAR is running, open `http://localhost:8080` in your browser. You should see Jenkins starting up and the initial setup screen.

**Note:** When running the WAR manually, Jenkins by default uses `~/.jenkins` (in the home directory of the user running it) as the Jenkins home for configuration and data. The initial admin password will be generated in `~/.jenkins/secrets/initialAdminPassword`. We will use this password in the [setup step](#initial-admin-password-and-unlocking-jenkins).

## Installing Jenkins on Linux (Ubuntu/Debian example)

On Linux systems, you can install Jenkins via your package manager or use the WAR file method similarly. Here we'll outline using the apt package manager for Ubuntu/Debian, as well as the WAR method.

### Method 1: Using apt Package Manager (Debian/Ubuntu)

1. Install Java: Ensure Java (JDK 11 or newer) is installed on the server:
```bash
sudo apt install openjdk-11-jre
```

2. Add Jenkins apt repository: Jenkins is not included by default in Ubuntu repositories. Add the Jenkins official repository and import its GPG key:
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```
(The above commands download and trust Jenkins's signing key, then add the Jenkins repository. These commands might change over time; refer to the official Jenkins documentation for the latest instructions.)

3. Update and install Jenkins:
```bash
sudo apt update
sudo apt install jenkins
```
This installs Jenkins and sets it up as a system service.

4. Start Jenkins service:
Jenkins may start automatically upon installation. If not, start it with:
```bash
sudo systemctl start jenkins
```

5. Enable it to start on boot (optional):
```bash
sudo systemctl enable jenkins
```

6. Access Jenkins UI:
By default, the Jenkins service runs on port 8080. Open a browser and go to `http://<your-server>:8080` (use localhost if running locally) to see the Jenkins web interface.

**Note:** On Ubuntu/Debian, the Jenkins home directory is usually `/var/lib/jenkins` and Jenkins runs as the jenkins user. The initial admin password will be in `/var/lib/jenkins/secrets/initialAdminPassword`. We will use this for the [initial setup](#initial-admin-password-and-unlocking-jenkins).

### Method 2: Running Jenkins from the .war file (Linux)

You can run the Jenkins WAR on Linux just as described for macOS:

1. Download jenkins.war (if not already downloaded) to your Linux machine.
2. Run it with Java: `java -jar jenkins.war` (run as a non-root user for security). Ensure that nothing else is running on port 8080 or use the `--httpPort=<port>` option to specify a different port.
3. Keep Jenkins running: The process will run in your terminal. For a longer-term solution, consider running Jenkins in a screen/tmux session or as a systemd service for stability.
4. Access the UI: Navigate to `http://<server>:8080` as usual to access Jenkins.

This method is useful if you want a quick test instance or do not want to install system-wide packages. Remember to have Java installed beforehand on the Linux system as well.

## Initial Admin Password and Unlocking Jenkins

No matter which installation method you used, when you first access Jenkins it will ask for an Administrator password to unlock. This password is automatically generated on first startup. To retrieve it:

Find the `initialAdminPassword` file on the Jenkins host. It's located in the Jenkins home directory under `secrets/initialAdminPassword`. Some common locations:

- Homebrew (macOS): `/usr/local/var/jenkins_home/secrets/initialAdminPassword`
- Linux apt (Debian/Ubuntu): `/var/lib/jenkins/secrets/initialAdminPassword`
- WAR file (default user home): `~/.jenkins/secrets/initialAdminPassword`

Open that file to get the 32-character alphanumeric password, and enter it into the Jenkins setup page to unlock.

## Basic Configuration and Jenkins Interface Overview

Once Jenkins is unlocked with the admin password, it will guide you through initial setup.

### Initial Setup and Configuration

1. **Install Plugins**: Jenkins will prompt you to install plugins. You can choose "Install suggested plugins," which will include Git, Pipeline, Docker, and others commonly used. This may take a few minutes as Jenkins downloads plugins. 

2. **Create Admin User**: After plugins installation, you'll be prompted to create your first admin user (set username, password, and email). Fill in the details to avoid using the initial admin password going forward.

3. **Configure Instance**: Jenkins might ask for an instance configuration (like Jenkins URL). Ensure the URL is correct (especially if Jenkins is accessed remotely). You can change this later in Manage Jenkins > Configure System.

When the setup is complete, you will see the main Jenkins dashboard.

---
