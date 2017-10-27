import re

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from chardet import UniversalDetector

from sereh.subexception import InvalidExtension
from sereh.subitem import SubtitleItem


class Subtitle(object):
    SUFFIX = ('.srt',)
    _items = []
    TIME_SEPARATOR = ' --> '

    def __init__(self, path):
        subtitle_path = Path(path)
        if not subtitle_path.is_file():
            raise FileNotFoundError

        if subtitle_path.suffix not in self.SUFFIX:
            raise InvalidExtension('Invalid file extension!')

        self._path = path
        self._name = subtitle_path.name

        self._detect_encoding()
        self._prepare()

    @property
    def path(self):
        return self._path

    @property
    def encoding(self):
        return self._encoding

    def _detect_encoding(self, max_line=200):
        detector = UniversalDetector()

        with open(self._path, 'rb') as f:
            for num, line in enumerate(f, 1):
                if num > max_line:
                    break
                detector.feed(line)
                if detector.done:
                    break

            detector.close()

        if detector.result['confidence'] > 0.9:
            self._encoding = detector.result['encoding']
        else:
            with open(self._path, encoding='cp1256') as f:
                for num, line in enumerate(f, 1):
                    if num > max_line:
                        break

            self._encoding = 'cp1256'

    def _prepare(self):
        with open(self._path, encoding=self.encoding) as f:
            self._subtitle = f.read()

        dic = {'ي': 'ی', 'ك': 'ک'}

        pattern = re.compile('|'.join(dic.keys()))
        self._subtitle = pattern.sub(lambda x: dic[x.group()], self._subtitle)

        regex = r"(\d+\s*)\n([\d:,]+)\s+-{2}\>\s+([\d:,]+)\s*\n([\s\S]*?(?=\n{2}|$))"
        self._items = [SubtitleItem(*i) for i in re.findall(regex, self._subtitle, re.IGNORECASE)]

    def save(self, path=None, encoding=None):
        path = path or (self._path + '_new.srt')
        encoding = encoding or self._encoding

        with open(path, 'w', encoding=encoding) as f:
            f.write(self._get_srt())

    def _get_srt(self):
        srt = ''
        linesep = '\r\n'

        for i in self._items:
            srt += linesep.join([str(i.index), self.TIME_SEPARATOR.join([str(i.start), str(i.end)]), i.text])
            srt += linesep * 2

        return srt

    def shift(self, *args, **kwargs):
        for i in self._items:
            i.shift(*args, **kwargs)

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        for i in self._items:
            yield i

    def __str__(self):
        return self._name
