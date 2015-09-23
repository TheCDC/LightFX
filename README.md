#LightFX

##Intro:
Welcome to LightFX, a hardware and software solution for making Windows or Linux system audio control RGB leds!
The hardware is composed of an Arduino microcontroller connected to a strip of WS28* "Neopixel" addressable RBG LEDs. The software is a sound analysis program and separate web interface both written in Python. This readme assumes the user is already knowledgeable in finding and installing Python libraries on their system.


##Software Dependencies:
Python 3
Libraries:
```flexx pygame pyaudio serial optparse```
I have included a download of the Flexx library in this repo for convenience. I do not expect to update it often so please always install from pip or the Flexx GitHub repo.
##Arduino:
  * Any Arduino microcontroller
  * Sufficient power supply for your strip of LEDs
  * Strip of WS28* LEds

##Setup:
Attach the Arduino to the strip. The user is expected to know how to correctly construct the circuit, the readme does not provide an electronics tutorial.
The program expects the strip to be on pin 6, but another capable pin may be used if the user reflects that change in the code.
The strip is assumed to have 30 LEDs. Personally, I used an Adafruit Neopixel 30 LED 1 meter strip.
Upload the LightFX.ino program to the Arduino using the Arduino IDE.
Plug the Arduino with the strip into the computer.


##Usage:
  1. Start either `linux-launch.sh` script or `windows-launch.sh`. On Linux it does require `sudo` access, which is reflected in the `linux-launch.sh` script.
  It will print the port on which the web interface for the program is running.
  2. Go to `localhost:THE_PORT/LightFX_Controller/` i.e. `http://127.0.0.1:49270/LightFX_Controller/`
  3. Select an audio device by number, on Windows you should most likely use Stereo Mix.
  4. From the drop down menu, select the serial port the Arduino is on.
  5. Click Start.
  6. Adjust the audio scale and exponent as needed and click Start to update the values. Optionally, enable Debug and Graph to see audio levels in the console.

Alternatively, the analyzer may be run in headless mode with `headless-windows.bat` or `headless-linux.sh`. These are simply shortcuts for running main.py with some arbitrary values that work on my own system. These values *MUST* be changed to work on yours.
