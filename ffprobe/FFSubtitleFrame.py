
from ffprobe.FFFrame import FFFrame

class FFSubtitleFrame(FFFrame):
    def pts(self):
        return int(self._data['pts'])
    
    def pts_time(self):
        return float(self._data['pts_time'])
    
    def start_display_time(self):
        return int(self._data['start_display_time'])
    
    def end_display_time(self):
        return int(self._data['end_display_time'])
    
    def format(self):
        return int(self._data['format'])
        
    def num_rects(self):
        return int(self._data['num_rects'])
