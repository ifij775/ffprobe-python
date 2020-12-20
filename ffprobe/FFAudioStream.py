'''
FFAudioStream
'''

from ffprobe.FFStream import FFStream

class FFAudioStream(FFStream):
    
    def sample_fmt(self):
        return self._data['sample_fmt']
    
    def sample_rate(self):
        return int(self._data['sample_rate'])
    
    def channels(self):
        return int(self._data['channels'])
    
    def channel_layout(self):
        return self._data['channel_layout']

    def bits_per_sample(self):
        return int(self._data['bits_per_sample'])
    
