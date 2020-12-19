
'''
FFVideoStream
'''

from ffprobe.FFStream import FFStream

class FFVideoStream(FFStream):
    def width(self):
        return int(self.__dict__['width'])
    
    def height(self):
        return int(self.__dict__['height'])
    
    def frame_size(self):
        """
        Returns the pixel frame size as an integer tuple (width,height) if the stream is a video stream.
        Returns None if it is not a video stream.
        """
        width = int(self.__dict__['width'])
        height = int(self.__dict__['height'])
        return (width,height)
    
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
    
    def color_range(self):
        return self.__dict__['color_range']
    
    def color_space(self):
        return self.__dict__['color_space']
    
    def color_transfer(self):
        return self.__dict__['color_transfer']
    
    def color_primaries(self):
        return self.__dict__['color_primaries']
    
    def bits_per_raw_sample(self):
        return int(self.__dict__['bits_per_raw_sample'])
    
    
    def chroma_location(self):
        return self.__dict__['chroma_location']
    
    def refs(self):
        return int(self.__dict__['refs'])
    
    def is_avc(self):
        return (self.__dict__['is_avc']=='true')
    
    def nal_length_size(self):
        return int(self.__dict__['nal_length_size'])
    
