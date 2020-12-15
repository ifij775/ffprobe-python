"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

class FFFrame:
    """
    An object representation of the multimedia frame.
    """

    def __init__(self, data_lines):
        for line in data_lines:
            self.__dict__.update({key: value for key, value, *_ in [line.strip().split('=')]})
    
    def media_type(self):
        return self.__dict__['media_type']
    
    def stream_index(self):
        return int(self.__dict__['stream_index'])
    
    def is_key_frame(self):
        return self.__dict__['key_frame']=='1'
    
    def pkt_pts(self):
        return int(self.__dict__['pkt_pts'])
    
    def pkt_pts_time(self):
        return float(self.__dict__['pkt_pts_time'])
    
    def pkt_dts(self):
        return int(self.__dict__['pkt_dts'])
    
    def pkt_dts_time(self):
        return float(self.__dict__['pkt_dts_time'])
    
    def pkt_duration(self):
        return int(self.__dict__['pkt_duration'])
    
    def pkt_duration_time(self):
        return float(self.__dict__['pkt_duration_time'])
    
    def pkt_pos(self):
        return int(self.__dict__['pkt_pos'])
    
    def pkt_size(self):
        return int(self.__dict__['pkt_size'])

    def __repr__(self):
        template = "<Frame: #Media-type: {media_type}, Stream-index: {stream_index} ({pkt_pts_time})>"
        return template.format(**self.__dict__)
