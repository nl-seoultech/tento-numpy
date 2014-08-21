import os
import json

from collections import namedtuple
from itertools import groupby

from numpy import linspace, array
from soundfile import CheapMP3

import matplotlib.pyplot as plt

Point = namedtuple('Point', ['x', 'y'])

def soft(frame):
    max_gain = 0
    for gain in frame:
        if max_gain < gain:
            max_gain = gain
    factor = 255 / max_gain
    len_gain = len(payload['frames']) - 1
    soft_gain = [0 for x in range(len_gain + 1)]
    min_gain = 255
    for i, gain in enumerate(payload['frames']):
        if i != 0 and  i < len_gain:
            sum_ = frame[i - 1] + gain + frame[i + 1]
            soft_gain[i] = sum_ / 3
        else:
            soft_gain[i] = gain
        soft_gain[i] = soft_gain[i] * factor
        if soft_gain[i] < min_gain and soft_gain[i] > 0:
            min_gain = soft_gain[i]
    return soft_gain


def simple(frame):
    l = []
    i = 0
    p1 = Point(x=0, y=frame[0])
    p2 = Point(x=1, y=frame[1])
    l.append(p1.y)
    l.append(p2.y)
    while i < len(frame) - 3:
        p3 = Point(x=i + 2, y=frame[i + 2])
        p4 = Point(x=i + 3, y=frame[i + 3])
        _slope = slope(p1, p2)
        next_slope = slope(p3, p4)
        c = is_cross(_slope, p1, next_slope, p3)
        if c is None:
            p1 = p2
            p2 = middle(p3, p4)
            l.append(p2.y)
        else:
            l.append(c.y)
        i += 2
    return l


def mult_simple(frame, n, max_):
    i = 0
    while i < n:
        if len(frame) < n:
            break
        frame = simple(frame)
        i += 1
    return frame


def is_cross(slope1, p1, slope2, p2):
    try:
        x = (p2.y - p1.y) / (slope1 - slope2)
    except ZeroDivisionError:
        return None
    y1 = linear_func(slope1, p1, x)
    y2 = linear_func(slope2, p1, x)
    if y1 == y2:
        return Point(x=x, y=y1)
    return None


def linear_func(slope1, p1, x):
    return slope1 * (x - p1.x) + p1.y


def read_json(path, filename):
    s = path.split('/')
    i = filename.rfind('.')
    name = filename[:i]
    ext = filename[i + 1:]
    with open(path, 'r') as f:
        if ext == 'json':
            payload = json.loads(f.read())
        else:
            return None
    return payload


def read_music(path, filename, out_base_root):
    payload = read_json(path, filename)
    if payload is None:
        return None
    m = len(payload['frames'])
    l = mult_simple(payload['frames'], 500, m)
    x = linspace(0, payload['duration'] / 1000, len(l))
    x2 = linspace(0, payload['duration'] / 1000, len(payload['frames']))
    frames = array(l)
    plt.clf()
    plt.plot(x2, payload['frames'], linestyle='--', marker='o', color='b')
    plt.savefig(os.path.join(out_base_root,
                             'complete-{0}.png'.format(payload['title'])))
    plt.clf()
    plt.plot(x, frames, linestyle='--', marker='o', color='b')
    plt.savefig(os.path.join(out_base_root,
                             '{0}.png'.format(payload['title'])))


def get_histo(samples):
    s = sorted(samples[:])
    for k, l in groupby(s):
        yield k, len(list(l))


def slope(p1, p2):
    return (p1.y - p2.y) / (p1.x - p2.x)


def middle(p1, p2):
    return Point(x=(p1.x + p2.x) / 2, y=(p1.y + p2.y) / 2)


def read_n_write(root, out_root):
    for b, d, ps in os.walk(root):
        for p in ps:
            path = os.path.join(b, p)
            read_music(path, p, out_root)


def to_json(filename, mp3, out):
    print(filename)
    i = filename.rfind('.')
    name = filename[:i]
    ext = filename[i + 1:]
    p = {
        'title': name,
        'frames': list(mp3.frame_gains),
        'duration': 1000
    }
    with open(os.path.join(out, '{0}.json'.format(name)), 'w') as f:
        f.write(json.dumps(p))


def dump_mp3(root, out, n=2):
    for i, (b, d, ps) in enumerate(os.walk(root)):
        for p in ps:
            if p.endswith('mp3'):
                path = os.path.join(b, p)
                cheap = CheapMP3(path)
                with cheap.read() as mp3:
                    to_json(p, mp3, out)
        if i == n:
            break
