from ffprobe.FFFrame import FFFrame

class FFVideoFrame(FFFrame):
    def width(self):
        return int(self.__dict__['width'])
    def height(self):
        return int(self.__dict__['height'])
    def pix_fmt(self):
        return self.__dict__['pix_fmt']
    def sample_aspect_ratio(self):
        return self.__dict__['sample_aspect_ratio']
    def pict_type(self):
        return self.__dict__['pict_type']
    def coded_picture_number(self):
        return int(self.__dict__['coded_picture_number'])
    def display_picture_number(self):
        return int(self.__dict__['display_picture_number'])
    def interlaced(self):
        return (self.__dict__['interlaced']=='1')
    def top_field_first(self):
        return (self.__dict__['top_field_first']=='1')
    def repeat_pict(self):
        return (self.__dict__['repeat_pict']=='1')
    def chroma_location(self):
        return self.__dict__['chroma_location']
