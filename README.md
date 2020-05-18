# Teensy_ADC
A test of how to sample 4 analog inputs as fast and synchronous as possible.

## Structure
This is a PlatformIO project on VSCode.
I added a folder /bin where I put some Python code to receive, store, plot and later analyze the data.

## Results
I found the Teensy 4.0 to be able to capture 4 analog inputs and transmitting the data to a PC at about 100 kHz.
This is mainly limited by the transfer speed to the PC.
The Teensy alone could sample up to about 300 kHz this way.