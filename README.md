# Fight Flight
This is the code for my senior design project, Fight Flight which is drones playing laser tag.

# Video
[Demo Video](https://www.youtube.com/watch?v=ew4bn0MpUDc)

# Code/Files Overview for TA grading this (hi! :wave:)
- `game.py`: The main script to play the game. Controls UI, player health, controller button readings from Arduino controllers, and communications between players via the server.
- `vision.py`: Does the computer vision detection of the drones. `game.py` will refer to this when the player attempts to shoot an opposing drone.
- `audio.py`: Contains classes to control the various audio effects in the game.
- `server.py`: Serves as the bridge for communication between players. Sends data between the players to communicate health status, attacks, abilities, and connections/disconnections.
- `ui.py`: Contains helper classes and functions to draw various menus and declutter `game.py`.
- `/drone types/Character.py`: Implementation of the 8 different drone classes, with their unique attack stats and abilities.
- `controller.ino`: Arduino code for the custom controller
- `/test and reference`: Contains the initial code for `vision.py` and `server.py`.
- `/images`: Contains all of the UI elements used in the game
- `/audio`: Contains all of the audio elements used in the game

# Set Up and Running
1) Install the following Python libraries
- [ ] Pygame
- [ ] OpenCV
- [ ] Pyserial
- [ ] Socket
2) Connect Arduino-based controller running `controller.ino`
- Modify line 13 in `game.py` to reflect the correct serial port.
  - MacOS: run `ls /dev/tty.*` in terminal, result should look like: `/dev/cu.usbmodem11401`
  - Windows: Open Device Manager -> Ports(COM & LPT), result should look like `COM#`
3) Comment/Uncomment line 114 or 115 in `game.py` depending on which OS you are running (MacOS or Windows)
4) Run `server.py`, note IP and PORT addresses
5) Modify line 123 in `game.py` to reflect IP and PORT of host running `server.py` in step 4
6) Connect drone camera receivers to the computer, and confirm that it can identify it as a camera (via the camera app)
7) Run `game.py` and enjoy!

# Common Issues
### **Problem:** Game showing incorrect camera (ex: showing laptop webcam instead) ###

**Solution:** In lines 114 or 115 of `game.py`, increment the `0` up by 1 until the correct camera is selected.

### **Problem:** Computers are not connecting to the server ###

**Solution:** 
1) Double check IP and PORT address
2) Make sure Computers are on the same WiFi network
3) If no WiFi or different networks, connect the computers with an Ethernet cable
