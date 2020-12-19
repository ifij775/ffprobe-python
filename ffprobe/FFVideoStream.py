
'''
FFVideoStream
'''

from ffprobe.FFStream import FFStream

class FFVideoStream(FFStream):
    def width(self):
        return int(self.__dict__['width'])
    
    def height(self):
        return int(self.__dict__['height'])
    
    def coded_width(self):
        return int(self.__dict__['coded_width'])
    
    def coded_height(self):
        return int(self.__dict__['coded_height'])
    
    def has_b_frames(self):
        return (self.__dict__['has_b_frames']=='1')
    
    def sample_aspect_ratio(self):
        return self.__dict__['sample_aspect_ratio']
    
    def display_aspect_ratio(self):
        return self.__dict__['display_aspect_ratio']
    
    def pix_fmt(self):
        return self.__dict__['pix_fmt']
    
    def level(self):
        return self.__dict__['level']
    
    def chroma_location(self):
        return self.__dict__['chroma_location']
    
    def refs(self):
        return int(self.__dict__['refs'])
    
    def is_avc(self):
        return (self.__dict__['is_avc']=='true')
