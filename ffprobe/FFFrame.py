"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

class FFFrame:
    """
    An object representation of the multimedia frame.
    """

    def __init__(self, data_lines):
        self._data = {}
        for line in data_lines:
            self._data.update({key: value for key, value, *_ in [line.strip().split('=')]})
    
    def media_type(self):
        return self._data['media_type']
    
    def stream_index(self):
        return int(self._data['stream_index'])
    
    def is_key_frame(self):
        return self._data['key_frame']=='1'
    
    def pkt_pts(self):
        return int(self._data['pkt_pts'])
    
    def pkt_pts_time(self):
        return float(self._data['pkt_pts_time'])
    
    def pkt_dts(self):
        return int(self._data['pkt_dts'])
    
    def pkt_dts_time(self):
        return float(self._data['pkt_dts_time'])
    
    def pkt_duration(self):
        return int(self._data['pkt_duration'])
    
    def pkt_duration_time(self):
        return float(self._data['pkt_duration_time'])
    
    def pkt_pos(self):
        return int(self._data['pkt_pos'])
    
    def pkt_size(self):
        return int(self._data['pkt_size'])

    def __repr__(self):
        template = "<Frame: #Media-type: {media_type}, Stream-index: {stream_index} ({pkt_pts_time})>"
        return template.format(**self._data)
