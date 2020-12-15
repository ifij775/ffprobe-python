"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

class FFPacket:
    """
    An object representation of the multimedia frame.
    """

    def __init__(self, data_lines):
        for line in data_lines:
            self.__dict__.update({key: value for key, value, *_ in [line.strip().split('=')]})
            
    def codec_type(self):
        return self.__dict__['codec_type']
    
    def stream_index(self):
        return int(self.__dict__['stream_index'])

    def __repr__(self):
        template = "<Packet: #Media-type: {media_type}, Stream-index: {stream_index} ({pts_time})>"
        return template.format(**self.__dict__)
