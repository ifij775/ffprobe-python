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

    def __repr__(self):
        template = "<Frame: #Media-type: {media_type}, Stream-index: {stream_index} ({pkt_pts_time})>"
        return template.format(**self.__dict__)
