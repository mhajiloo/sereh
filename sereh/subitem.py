from sereh.subtime import SubtitleTime


class SubtitleItem(object):
    PATTERN = '[{} - {}] {}'

    def __init__(self, index=0, start=None, end=None, text=''):
        self._index = int(str(index).strip())
        self._start = SubtitleTime.prepare_time(start)
        self._end = SubtitleTime.prepare_time(end)
        self._text = str(text).strip()

    @property
    def index(self):
        return self._index

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def text(self):
        return self._text

    def duration(self):
        return self._end - self._start

    def shift(self, *args, **kwargs):
        self._start.shift(*args, **kwargs)
        self._end.shift(*args, **kwargs)

    def __str__(self):
        return self.PATTERN.format(self._start, self._end, self._text)
