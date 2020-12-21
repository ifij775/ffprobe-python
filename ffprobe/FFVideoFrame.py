from ffprobe.FFFrame import FFFrame

class FFVideoFrame(FFFrame):
    def width(self):
        return int(self._data['width'])
    def height(self):
        return int(self._data['height'])
    def frame_size(self):
        return (self.width(), self.height())
    def pixel_format(self):
        return self._data['pix_fmt']
    def sample_aspect_ratio(self):
        return self._data['sample_aspect_ratio']
    def pict_type(self):
        return self._data['pict_type']
    def coded_picture_number(self):
        return int(self._data['coded_picture_number'])
    def display_picture_number(self):
        return int(self._data['display_picture_number'])
    def interlaced(self):
        return (self._data['interlaced']=='1')
    def top_field_first(self):
        return (self._data['top_field_first']=='1')
    def repeat_pict(self):
        return (self._data['repeat_pict']=='1')
    def chroma_location(self):
        return self._data['chroma_location']
