"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""
import functools
import operator

class FFStream:
    """
    An object representation of an individual stream in a multimedia file.
    """

    def __init__(self, data_dict):
        self._data = data_dict

    def __repr__(self):
        #if self.is_video():
        #    template = "<Stream: #{index} [{codec_type}] {codec_long_name}, {framerate}, ({width}x{height})>"

        #elif self.is_audio():
        #    template = "<Stream: #{index} [{codec_type}] {codec_long_name}, channels: {channels} ({channel_layout}), " \
        #               "{sample_rate}Hz> "

        #elif self.is_subtitle() or self.is_attachment():
        #    template = "<Stream: #{index} [{codec_type}] {codec_long_name}>"

        #else:
        #    template = ''

        template = "<Stream: #{index} [{codec_type}] {codec_long_name}>"
        return template.format(**self._data)
    
    def stream_index(self):
        """
        The stream index
        """
        return int(self._data['index'])

    def frames(self):
        """
        Returns the length of a video stream in frames. Returns 0 if not a video stream.
        """
        if self._data.get('nb_frames', '') != 'N/A':
            try:
                frame_count = int(self._data.get('nb_frames', ''))
            except ValueError:
                raise FFProbeError('None integer frame count')
        else:
            # When N/A is returned, set frame_count to 0 too
            frame_count = 0
        
        return frame_count

    def duration_seconds(self):
        """
        Returns the runtime duration of the video stream as a floating point number of seconds.
        Returns 0.0 if not a video stream.
        """
        if self._data.get('duration', '') != 'N/A':
            try:
                duration = float(self._data.get('duration', ''))
            except ValueError:
                raise FFProbeError('None numeric duration')
        else:
            # When N/A is returned, set duration to 0 too
            duration = 0.0

        return duration

    def codec(self):
        """
        Returns a string representation of the stream codec.
        """
        return self._data.get('codec_name', None)

    def codec_description(self):
        """
        Returns a long representation of the stream codec.
        """
        return self._data.get('codec_long_name', None)

    def codec_tag(self):
        """
        Returns a short representative tag of the stream codec.
        """
        return self._data.get('codec_tag_string', None)

    def bit_rate(self):
        """
        Returns bit_rate as an integer in bps
        """
        try:
            return int(self._data.get('bit_rate', ''))
        except ValueError:
            raise FFProbeError('None integer bit_rate')
            
    def language(self):
        return self._data['TAG:language']
    
    def frame_count(self):
        return int(self._data['nb_read_frames'])
    
    def packet_count(self):
        return int(self._data['nb_read_packets'])
