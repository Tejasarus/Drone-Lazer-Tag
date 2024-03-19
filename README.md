# Fight Flight
This is the code for my senior design project, Fight Flight which is drones playing laser tag.

# Video
[Demo Video](https://www.youtube.com/watch?v=ew4bn0MpUDc)

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
