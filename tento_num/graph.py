class DiffSpace(list):

    @property
    def average(self):
        return sum(self) / len(self)


class Space(list):

    @property
    def interval(self):
        return 1 / (len(self) - 1)


    def get(self, i):
        f = i / self.interval
        if f % 1 > 0:
            if_ = int(f)
            first = if_ * self.interval
            second = (if_ + 1) * self.interval
            r = self.poly((first, self.get(first)),
                          (second, self.get(second)), i)
        else:
            r = self[int(f)]
        return r


    def poly(self, p1, p2, g):
        xdf = p2[0] - p1[0]
        ydf = p2[1] - p1[1]
        slope = ydf / xdf
        return slope * (g - p1[0]) + p1[1]


    def __sub__(self, s):
        self_len = len(self)
        other_len = len(s)
        long_ = s
        short = self
        if self_len > other_len:
            long_ = self
            short = s
        r = [abs(x - long_.get(i * short.interval)) for i,x in enumerate(short)]
        return DiffSpace(r)
