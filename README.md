# Cosmobeat
Computer Architecture and Organization project<br><br>
Cosmobeat is an innovative rhythm game that merges intuitive gyroscopic controls with dynamic beat-matching gameplay. The game challenges players to navigate by moving a player bar horizontally across the screen to catch and interact with notes that descend based on the rhythm of the soundtrack.

**Software Tools:**
- Python
- Pygame library
- Mpu6050-raspberrypi library
- Gpiozero

**Hardware Tools:**	
- Raspberry Pi 400 
- MPU-6050 digital accelerometer and gyroscope
- Buzzer 
- Switches
- LEDs

# Game controls
**Keyboard:**
- Left and Right arrow to move the bar horizontally.
- Press or hold the Spacebar to interact with the notes. 
- Press “p” to pause the game
- Up arrow to increase volume, Down arrow to decrease volume
**Gyro controller:**
- Tilt the controller to the left and right to move the bar horizontally
- Press or hold the buttons to interact with the notes.

**Type of notes**
- **Normal note:** Move the bar to the note position then press the button.
- **Hold note:** Move the bar to the note position then hold the button until the note ends.
- **Move note:** Move the bar to the note position. No need to press or hold the button.



# Steps for creating virtual environment and installing packages
1. Create virtual environment using this command:  
   ```bash
   python3 -m venv .venv
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
3. Install the packages from requirement.txt file:
   ```bash
   pip3 install -r requirements.txt

# Steps for running the program
1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
2. run the python code
   ```bash
   python3 main.py
3. When finished, deactivate the virtual environment
   ```bash
   deactivate
