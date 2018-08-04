# Rotary Phone Player

This project uses a Raspberry Pi 3 to read inputs from an old rotary phone and play a recording when a specific number is dialed. Signals from the rotary dial are connected to GPIO pins on the Pi, while the composite video jack is used to output audio to the receiver.
A Python based wrapper for omxplayer instead of pure bash commands is used for its easiness and cleaner programming.

**** In the folder "recordings" an empty file must be placed inside named "Blank.wav" ****

#### HARDWARE ####

There are 3 wires connected to the GPIO for the hook, rotary dial, and ground 
and 2 wires using the AUX connecting to the phone speaker

**** if recreating this with a new Raspbian, you need to comment out an exception raised in the OMXplayer ****
