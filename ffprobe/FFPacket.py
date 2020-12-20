"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

class FFPacket:
    """
    An object representation of the multimedia stream packet.
    """

    def __init__(self, data_lines):
        self._data = {}
        for line in data_lines:
            self._data.update({key: value for key, value, *_ in [line.strip().split('=')]})
            
    def codec_type(self):
        return self._data['codec_type']
    
    def stream_index(self):
        return int(self._data['stream_index'])
    
    def pts(self):
        return int(self._data['pts'])
    
    def pts_time(self):
        return float(self._data['pts_time'])

    def dts(self):
        return int(self._data['dts'])
    
    def dts_time(self):
        return float(self._data['dts_time'])

    def duration(self):
        return int(self._data['duration'])
    
    def duration_time(self):
        return float(self._data['duration_time'])

    def size(self):
        return int(self._data['size'])
    
    def pos(self):
        return int(self._data['pos'])
    
    def flags(self):
        return self._data['flags']
    
    def __repr__(self):
        template = "<Packet: #Media-type: {codec_type}, Stream-index: {stream_index} ({pts_time})>"
        return template.format(**self._data)
