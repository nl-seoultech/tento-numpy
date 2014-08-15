# -*- coding: utf-8 -*-
import os
import json

from collections import namedtuple
from itertools import groupby

from numpy import linspace, array

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
    p = max_ / 4
    while i < n:
        if len(frame) < p:
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


def read_music(path, filename):
    s = path.split('/')
    name, ext = filename.split('.')
    with open(path, 'r') as f:
        if path.endswith('json'):
            payload = json.loads(f.read())
        else:
            return None
    with open('half.txt', 'w') as f:
        f.write(','.join([str(x) for x in simple(payload['frames'])]))
    m = len(payload['frames'])
    print(m)
    l = mult_simple(payload['frames'], 10, m)
    print(len(l))
    x = linspace(0, payload['duration'] / 1000, len(l))
    x2 = linspace(0, payload['duration'] / 1000, len(payload['frames']))
    frames = array(l)
    plt.plot(x2, payload['frames'], linestyle='--', marker='o', color='b')
    plt.savefig('./out/complete-{0}.png'.format(payload['title']))
    plt.clf()
    plt.plot(x, frames, linestyle='--', marker='o', color='b')
    plt.savefig('./out/{0}.png'.format(payload['title']))


def get_histo(samples):
    s = sorted(samples[:])
    for k, l in groupby(s):
        yield k, len(list(l))


def slope(p1, p2):
    return (p1.y - p2.y) / (p1.x - p2.x)


def middle(p1, p2):
    return Point(x=(p1.x + p2.x) / 2, y=(p1.y + p2.y) / 2)


for b, d, ps in os.walk('./music_frames/'):
    for p in ps:
        path = os.path.join(b, p)
        read_music(path, p)
