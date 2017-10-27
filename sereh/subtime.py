import re


class SubtitleTime(object):
    PATTERN = '{:02d}:{:02d}:{:02d},{:03d}'
    TIME_PATTERN = r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})$'

    def __init__(self, hours=0, minutes=0, seconds=0, milliseconds=0):
        self._hours = int(hours)
        self._minutes = int(minutes)
        self._seconds = int(seconds)
        self._milliseconds = int(milliseconds)

    @property
    def ordinal(self):
        return self._milliseconds \
               + self._seconds * 1000 \
               + self._minutes * 1000 * 60 \
               + self._hours * 1000 * 60 * 60

    @ordinal.setter
    def ordinal(self, value):
        self._hours = int((value / (1000 * 60 * 60)) % 24)
        self._minutes = int((value / (1000 * 60)) % 60)
        self._seconds = int((value / 1000) % 60)
        self._milliseconds = int(value % 1000)

    def shift(self, hours=0, minutes=0, seconds=0, milliseconds=0, ratio=None):
        if ratio is not None:
            self *= ratio
        self += SubtitleTime(hours, minutes, seconds, milliseconds)

    def __add__(self, other):
        return self.prepare_time(self.ordinal + other.ordinal)

    def __iadd__(self, other):
        self.ordinal += self.prepare_time(other).ordinal
        return self

    def __sub__(self, other):
        return self.prepare_time(self.ordinal - other.ordinal)

    def __mul__(self, ratio):
        return self.prepare_time(int(round(self.ordinal * ratio)))

    def __imul__(self, ratio):
        self.ordinal = int(round(self.ordinal * ratio))
        return self

    @classmethod
    def prepare_time(cls, time):
        if isinstance(time, SubtitleTime):
            return time

        if isinstance(time, str):
            items = re.findall(cls.TIME_PATTERN, time)[0]
            if len(items) != 4:
                raise Exception('')

            return cls(*items)

        if isinstance(time, int):
            return cls(milliseconds=time)

    def __str__(self):
        return self.PATTERN.format(self._hours, self._minutes, self._seconds, self._milliseconds)
