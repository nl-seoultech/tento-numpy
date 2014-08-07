import os
import json

from itertools import groupby

from numpy import linspace, array

import matplotlib.pyplot as plt

def read_music(path, filename):
    s = path.split('/')
    name, ext = filename.split('.')
    with open(path, 'r') as f:
        payload = json.loads(f.read())
    max_gain = 0
    for gain in payload['frames']:
        if max_gain < gain:
            max_gain = gain
    factor = 255 / max_gain
    len_gain = len(payload['frames']) - 1
    soft_gain = [0 for x in range(len_gain + 1)]
    min_gain = 255
    for i, gain in enumerate(payload['frames']):
        if i != 0 and  i < len_gain:
            sum_ = payload['frames'][i - 1] + gain + payload['frames'][i + 1]
            soft_gain[i] = sum_ / 3
        else:
            soft_gain[i] = gain
        soft_gain[i] = soft_gain[i] * factor
        if soft_gain[i] < min_gain and soft_gain[i] > 0:
            min_gain = soft_gain[i]
    x = linspace(0, payload['duration'] / 1000, len(payload['frames']))
    frames = array(payload['frames'])
    line = plt.plot(x, frames, linewidth=1)
    plt.savefig('./out/{0}.png'.format(payload['title']))


def get_histo(samples):
    s = sorted(samples[:])
    for k, l in groupby(s):
        yield k, len(list(l))


for b, d, ps in os.walk('./music_frames/'):
    for p in ps:
        path = os.path.join(b, p)
        read_music(path, p)
