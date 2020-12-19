'''
FFAudioStream
'''

from ffprobe.FFStream import FFStream

class FFAudioStream(FFStream):
    def language(self):
        return self.__dict__['TAG:language']
    
    def sample_fmt(self):
        return self.__dict__['sample_fmt']
    
    def sample_rate(self):
        return int(self.__dict__['sample_rate'])
    
    def channels(self):
        return int(self.__dict__['channels'])
    
    def channel_layout(self):
        return self.__dict__['channel_layout']
