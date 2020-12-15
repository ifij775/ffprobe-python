"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

class FFPacket:
    """
    An object representation of the multimedia stream packet.
    """

    def __init__(self, data_lines):
        for line in data_lines:
            self.__dict__.update({key: value for key, value, *_ in [line.strip().split('=')]})
            
    def codec_type(self):
        return self.__dict__['codec_type']
    
    def stream_index(self):
        return int(self.__dict__['stream_index'])
    
    def pts(self):
        return int(self.__dict__['pts'])
    
    def pts_time(self):
        return float(self.__dict__['pts_time'])

    def dts(self):
        return int(self.__dict__['dts'])
    
    def dts_time(self):
        return float(self.__dict__['dts_time'])

    def duration(self):
        return int(self.__dict__['duration'])
    
    def duration_time(self):
        return float(self.__dict__['duration_time'])

    def size(self):
        return int(self.__dict__['size'])
    
    def pos(self):
        return int(self.__dict__['pos'])
    
    def __repr__(self):
        template = "<Packet: #Media-type: {media_type}, Stream-index: {stream_index} ({pts_time})>"
        return template.format(**self.__dict__)
