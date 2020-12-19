
'''
FFSubtitleStream
'''

from ffprobe.FFStream import FFStream

class FFSubtitleStream(FFStream):
    def language(self):
        return self.__dict__['TAG:language']
