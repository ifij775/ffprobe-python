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
        self.__dict__.update(data_dict)

        try:
            self.__dict__['framerate'] = round(
                functools.reduce(
                    operator.truediv, map(int, self.__dict__.get('avg_frame_rate', '').split('/'))
                )
            )

        except ValueError:
            self.__dict__['framerate'] = None
        except ZeroDivisionError:
            self.__dict__['framerate'] = 0

    def __repr__(self):
        if self.is_video():
            template = "<Stream: #{index} [{codec_type}] {codec_long_name}, {framerate}, ({width}x{height})>"

        elif self.is_audio():
            template = "<Stream: #{index} [{codec_type}] {codec_long_name}, channels: {channels} ({channel_layout}), " \
                       "{sample_rate}Hz> "

        elif self.is_subtitle() or self.is_attachment():
            template = "<Stream: #{index} [{codec_type}] {codec_long_name}>"

        else:
            template = ''

        return template.format(**self.__dict__)
    
    def stream_index(self):
        """
        The stream index
        """
        return int(self.__dict__['index'])

    def is_audio(self):
        """
        Is this stream labelled as an audio stream?
        """
        return self.__dict__.get('codec_type', None) == 'audio'

    def is_video(self):
        """
        Is the stream labelled as a video stream.
        """
        return self.__dict__.get('codec_type', None) == 'video'

    def is_subtitle(self):
        """
        Is the stream labelled as a subtitle stream.
        """
        return self.__dict__.get('codec_type', None) == 'subtitle'

    def is_attachment(self):
        """
        Is the stream labelled as a attachment stream.
        """
        return self.__dict__.get('codec_type', None) == 'attachment'

    def frame_rate(self):
        """
        Calculates and returns the frame rate as a float if the stream is a video stream.
        Returns None if it is not a video stream.
        """
        if self.is_video():
            if self.duration_seconds() > 0.0:
                frame_rate = self.frames() / self.duration_seconds()
            else:
                frame_rate = self.__dict__['framerate']
            return frame_rate
        else:
            return None

    def frame_size(self):
        """
        Returns the pixel frame size as an integer tuple (width,height) if the stream is a video stream.
        Returns None if it is not a video stream.
        """
        size = None
        if self.is_video():
            width = self.__dict__['width']
            height = self.__dict__['height']

            if width and height:
                try:
                    size = (int(width), int(height))
                except ValueError:
                    raise FFProbeError("None integer size {}:{}".format(width, height))
        else:
            return None

        return size

    def pixel_format(self):
        """
        Returns a string representing the pixel format of the video stream. e.g. yuv420p.
        Returns none is it is not a video stream.
        """
        return self.__dict__.get('pix_fmt', None)

    def frames(self):
        """
        Returns the length of a video stream in frames. Returns 0 if not a video stream.
        """
        if self.is_video() or self.is_audio():
            if self.__dict__.get('nb_frames', '') != 'N/A':
                try:
                    frame_count = int(self.__dict__.get('nb_frames', ''))
                except ValueError:
                    raise FFProbeError('None integer frame count')
            else:
                # When N/A is returned, set frame_count to 0 too
                frame_count = 0
        else:
            frame_count = 0

        return frame_count

    def duration_seconds(self):
        """
        Returns the runtime duration of the video stream as a floating point number of seconds.
        Returns 0.0 if not a video stream.
        """
        if self.is_video() or self.is_audio():
            if self.__dict__.get('duration', '') != 'N/A':
                try:
                    duration = float(self.__dict__.get('duration', ''))
                except ValueError:
                    raise FFProbeError('None numeric duration')
            else:
                # When N/A is returned, set duration to 0 too
                duration = 0.0
        else:
            duration = 0.0

        return duration

    def codec(self):
        """
        Returns a string representation of the stream codec.
        """
        return self.__dict__.get('codec_name', None)

    def codec_description(self):
        """
        Returns a long representation of the stream codec.
        """
        return self.__dict__.get('codec_long_name', None)

    def codec_tag(self):
        """
        Returns a short representative tag of the stream codec.
        """
        return self.__dict__.get('codec_tag_string', None)

    def bit_rate(self):
        """
        Returns bit_rate as an integer in bps
        """
        try:
            return int(self.__dict__.get('bit_rate', ''))
        except ValueError:
            raise FFProbeError('None integer bit_rate')
            
    def language(self):
        return self.__dict__['TAG:language']
