import serial
import scipy.signal as signal

import time

ser = serial.Serial()
ser.baudrate = 9600 # will set automatically
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.port = "COM8"
ser.open()

input_buffer = []

channels = [[], [], [], []]

print(time.time())

# sync
while ser.read() != b'\x00':
    pass

for _ in range(1000000):
    input_buffer.append(ser.read(9))
    #print(ser.read(9))

print(time.time())

print(len(input_buffer))

inputs = input_buffer.copy()
input_buffer = []


for inp in inputs:
    try:
        for bbyte in inp:
            input_buffer.append(bbyte)
            if input_buffer[0] == 0:
                if len(input_buffer) == 9:
                    channels[0].append(input_buffer[1] | input_buffer[2] << 8)
                    channels[1].append(input_buffer[3] | input_buffer[4] << 8)
                    channels[2].append(input_buffer[5] | input_buffer[6] << 8)
                    channels[3].append(input_buffer[7] | input_buffer[8] << 8)
                    input_buffer = []
            else:
                input_buffer = []
    except Exception as e:
        pass

import matplotlib.pyplot as plt

for channel in channels:
    for n in range(2, len(channel)-2):
        vals = [channel[n-2], channel[n-1], channel[n], channel[n+1], channel[n+2]]
        vals.sort()
        channel[n] = vals[2]



plt.plot(channels[0])

tabs = 5001
freq = 50
sample_rate = 100_000
tpeinh = signal.firwin(tabs, freq, pass_zero=True, fs=sample_rate)                                 # Filterkoeffizienten berechnen
channels[0] = signal.lfilter(tpeinh, 1, channels[0])
channels[1] = signal.lfilter(tpeinh, 1, channels[1])
channels[2] = signal.lfilter(tpeinh, 1, channels[2])
channels[3] = signal.lfilter(tpeinh, 1, channels[3])

plt.plot(channels[0][2500:])
#plt.plot(channels[1])
#plt.plot(channels[2])
#plt.plot(channels[3])
plt.show()