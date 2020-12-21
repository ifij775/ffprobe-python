
from ffprobe.FFFrame import FFFrame

class FFSubtitleFrame(FFFrame):
    def format(self):
        return int(self._data['format'])
        
    def num_rects(self):
        return int(self._data['num_rects'])
