
'''
FFVideoStream
'''

from ffprobe.FFStream import FFStream

class FFVideoStream(FFStream):
    def width(self):
        return int(self._data['width'])
    
    def height(self):
        return int(self._data['height'])
    
    def frame_size(self):
        """
        Returns the pixel frame size as an integer tuple (width,height) if the stream is a video stream.
        Returns None if it is not a video stream.
        """
        return (self.width(),self.height())
    
    def coded_width(self):
        return int(self._data['coded_width'])
    
    def coded_height(self):
        return int(self._data['coded_height'])
    
    def has_b_frames(self):
        return (self._data['has_b_frames']=='1')
    
    def sample_aspect_ratio(self):
        return self._data['sample_aspect_ratio']
    
    def display_aspect_ratio(self):
        return self._data['display_aspect_ratio']
    
    def pixel_format(self):
        return self._data['pix_fmt']
    
    def level(self):
        return self._data['level']
    
    def color_range(self):
        return self._data['color_range']
    
    def color_space(self):
        return self._data['color_space']
    
    def color_transfer(self):
        return self._data['color_transfer']
    
    def color_primaries(self):
        return self._data['color_primaries']
    
    def bits_per_raw_sample(self):
        return int(self._data['bits_per_raw_sample'])
    
    
    def chroma_location(self):
        return self._data['chroma_location']
    
    def refs(self):
        return int(self._data['refs'])
    
    def is_avc(self):
        return (self._data['is_avc']=='true')
    
    def nal_length_size(self):
        return int(self._data['nal_length_size'])
    
