import os
import json

from fractions import gcd
from math import sqrt

from soundfile import CheapMP3


class DiffSpace(list):

    @property
    def average(self):
        return sum(self) / len(self)


    @property
    def dispersion(self):
        avg_pow = self.average ** 2
        s = [x ** 2 for x in self]
        powed_avg = sum(s) / len(s)
        return powed_avg - avg_pow


    @property
    def standard_deviation(self):
        return sqrt(self.dispersion)


class Space(list):

    #: x plus 축의 frame_gains
    x_plus = []

    #: x minus 축의 frame_gains
    x_minus = []

    #: y plus 축의 frame_gains
    y_plus = []

    #: y minus 축의 frame_gains
    y_minus = []

    scale = 1

    def get(self, i):
        if i % self.interval == 0:
            r = self[int(i // self.interval)]
        else:
            front = int(i // self.interval)
            p1 = (front * self.interval, self[front])
            p2 = ((front + 1) * self.interval, self[front + 1])
            r = self.poly(p1, p2, i)
        return r


    def poly(self, p1, p2, g):
        xdf = p2[0] - p1[0]
        ydf = p2[1] - p1[1]
        slope = ydf / xdf
        return slope * (g - p1[0]) + p1[1]


    def init_pos(self, path):
        from tento_num.func import remove_lower
        from tento_num.io import mult_simple
        pos = ['x_plus', 'x_minus', 'y_plus', 'y_minus']
        for b, d, ps in os.walk(path):
            for p in ps:
                if p.endswith('json'):
                    path = os.path.join(b, p)
                    with open(path, 'r') as f:
                        payload = json.loads(f.read())
                        for x in pos:
                            if p.startswith(x):
                                s = remove_lower(payload['frames'])
                                setattr(
                                    self,
                                    x,
                                    Space(s))


    @property
    def interval(self):
        return self.scale / len(self)


    @property
    def position(self):
        if not (self.y_plus and self.y_minus and self.x_plus and self.x_minus):
            raise Exception(
                "Space.{x_plus, x_minus, y_plus, y_minus} must required.")
        me = Space(self[:])
        distance = {
            'yp': self - self.y_plus,
            'ym': self - self.y_minus,
            'xp': self - self.x_plus,
            'xm': self - self.x_minus
        }
        for k, v in distance.copy().items():
            distance[k] = v.standard_deviation
        x = distance['xp']
        if distance['xm'] < distance['xp']:
            x = -distance['xm']
        y = distance['yp']
        if distance['ym'] < distance['yp']:
            y = -distance['ym']
        return x, y


    def lcm(self, a, b):
        return (a * b) // gcd(a, b)


    def interval_items(self):
        for i, x in enumerate(self):
            yield int(i * self.interval), x


    def __sub__(self, s):
        self.scale = s.scale = self.lcm(len(self), len(s))
        subject = self
        object_ = s
        if self.interval > s.interval:
            subject = s
            object_ = self
        s = [abs(subject.get(x[0]) - x[1]) for x in object_.interval_items()]
        return DiffSpace(s)


    def __repr__(self):
        return 'Space(len={0})'.format(len(self))
