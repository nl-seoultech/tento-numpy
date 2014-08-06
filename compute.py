import json

from numpy import linspace, array
from numpy.fft import fft

import matplotlib.pyplot as plt

with open('abc.json', 'r') as f:
    payload = json.loads(f.read())

fou = fft(payload['frames'])
max_gain = 0
for gain in payload['frames']:
    if max_gain < gain:
        max_gain = gain

factor = 255 / max_gain
len_gain = len(payload['frames']) - 1
soft_gain = [0 for x in range(len_gain + 1)]

for i, gain in enumerate(payload['frames']):
    if i != 0 and  i < len_gain:
        sum_ = payload['frames'][i - 1] + gain + payload['frames'][i + 1]
        soft_gain[i] = sum_ / 3
    else:
        soft_gain[i] = gain
    soft_gain[i] = soft_gain[i] * factor


x = linspace(0, 120, len(payload['frames']))
frames = array(payload['frames'])
line = plt.plot(x, soft_gain, linewidth=1)

plt.savefig('./abc.png')
