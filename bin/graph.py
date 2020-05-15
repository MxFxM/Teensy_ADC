import serial
import scipy.signal as signal

ser = serial.Serial()
ser.baudrate = 9600 # will set automatically
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.port = "COM8"
ser.open()

input_buffer = []

channels = [[], [], [], []]

while len(channels[0]) < 100_000:
    newbytes = ser.in_waiting
    for _ in range(newbytes):
        input_buffer.append(ser.read())
        if input_buffer[0] == b'\x00':
            if len(input_buffer) == 9:
                channels[0].append(int.from_bytes(input_buffer[1], byteorder='big') | int.from_bytes(input_buffer[2], byteorder='big') << 8)
                channels[1].append(int.from_bytes(input_buffer[3], byteorder='big') | int.from_bytes(input_buffer[4], byteorder='big') << 8)
                channels[2].append(int.from_bytes(input_buffer[5], byteorder='big') | int.from_bytes(input_buffer[6], byteorder='big') << 8)
                channels[3].append(int.from_bytes(input_buffer[7], byteorder='big') | int.from_bytes(input_buffer[8], byteorder='big') << 8)
                input_buffer = []
        else:
            input_buffer = []

import matplotlib.pyplot as plt

for channel in channels:
    for n in range(2, len(channel)-2):
        vals = [channel[n-2], channel[n-1], channel[n], channel[n+1], channel[n+2]]
        vals.sort()
        channel[n] = vals[2]

tabs = 5001
freq = 50
sample_rate = 10_000
tpeinh = signal.firwin(tabs, freq, pass_zero=True, fs=sample_rate)                                 # Filterkoeffizienten berechnen
channels[0] = signal.lfilter(tpeinh, 1, channels[0])
channels[1] = signal.lfilter(tpeinh, 1, channels[1])
channels[2] = signal.lfilter(tpeinh, 1, channels[2])
channels[3] = signal.lfilter(tpeinh, 1, channels[3])

plt.plot(channels[0])
plt.plot(channels[1])
plt.plot(channels[2])
plt.plot(channels[3])
plt.show()