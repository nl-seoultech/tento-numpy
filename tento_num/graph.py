import os
import json

from fractions import gcd

from soundfile import CheapMP3


class DiffSpace(list):

    @property
    def average(self):
        return sum(self) / len(self)


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
            r = self[i]
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
                                s = mult_simple(remove_lower(payload['frames']),
                                                100)
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
            'yp': me - self.y_plus,
            'ym': me - self.y_minus,
            'xp': me - self.x_plus,
            'xm': me - self.x_minus
        }
        return 0, 0


    def lcm(self, a, b):
        return (a * b) // gcd(a, b)


    def __sub__(self, s):
        self.scale = s.scale = self.lcm(len(self), len(s))
        subject = self
        object_ = s
        if self.interval > s.interval:
            subject = s
            object_ = self
        s = [abs(subject.get(x[0]) - x[1]) for x in object_.interval_items()]
        return DiffSpace(s)


    def interval_items(self):
        for i, x in enumerate(self):
            yield int(i * self.interval), x


    def __repr__(self):
        return 'Space(len={0})'.format(len(self))
