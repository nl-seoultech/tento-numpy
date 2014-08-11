from sys import argv

from numpy import linspace, log10
from numpy.fft import fftfreq, fft
from pydub import AudioSegment

import matplotlib.pyplot as plt

sound = AudioSegment.from_mp3(argv[1])
raw_data = sound._data
print(type(raw_data))
xs = bytearray(raw_data)
x = linspace(0, 274, len(raw_data))
freqs = fftfreq(len(raw_data), x[1] - x[0])
sp = fft(xs)
plt.plot(freqs, sp.real, freq, sp.imag)
plt.savefig('./abc.png')

