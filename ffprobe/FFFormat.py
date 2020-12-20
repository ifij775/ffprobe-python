"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""

class FFFormat:
    """
    An object representation of the multimedia file format.
    """

    def __init__(self, data_lines):
        for line in data_lines:
            if line.find("TAG:") >= 0:
                line = line[line.find(":")+1:]

            self._data.update({key: value for key, value, *_ in [line.strip().split('=')]})

    def __repr__(self):
        template = "<Format: #Streams: {nb_streams}, format: {format_name} ({format_long_name})>"
        return template.format(**self._data)
