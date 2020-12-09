"""
Python wrapper for ffprobe command line tool. ffprobe must exist in the path.
"""
import functools
import operator
import os
import pipes
import platform
import re
import subprocess

from ffprobe.exceptions import FFProbeError


class FFProbe:
    """
    FFProbe wraps the ffprobe command and pulls the data into an object form::
        metadata=FFProbe('multimedia-file.mov')
    """

    def __init__(self, path_to_video, show_format=True, show_streams=True, show_frames=True, show_packets=True, select_streams='', timeout=None):
        self.path_to_video = path_to_video

        try:
            with open(os.devnull, 'w') as tempf:
                subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
        except FileNotFoundError:
            raise IOError('ffprobe not found.')

        if os.path.isfile(self.path_to_video) or self.path_to_video.startswith('http'):
            cmd = ["ffprobe","-v","quiet"]
            if show_format:
                cmd.append("-show_format")
            if show_streams:
                cmd.append("-show_streams")
            if show_frames:
                cmd.append("-show_frames")
            if show_packets:
                cmd.append("-show_packets")
            if select_streams:
                cmd.extend(["-select_streams",select_streams])
            cmd.append(self.path_to_video)

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait(timeout)

            stream = False
            ignore_line = False
            format_ = False
            self.format = None
            self.streams = []
            self.video = []
            self.audio = []
            self.subtitle = []
            self.attachment = []

            for line in iter(p.stdout.readline, b''):
                line = line.decode('UTF-8')
                if '[STREAM]' in line:
                    stream = True
                    ignore_line = False
                    data_lines = []
                elif '[/STREAM]' in line and stream:
                    stream = False
                    ignore_line = False
                    # noinspection PyUnboundLocalVariable
                    self.streams.append(FFStream(data_lines))
                elif stream:
                    if '[SIDE_DATA]' in line:
                        ignore_line = True
                    elif '[/SIDE_DATA]' in line:
                        ignore_line = False
                    elif ignore_line is False:
                        data_lines.append(line)
                elif '[FORMAT]' in line:
                    format_ = True
                    data_lines = []
                elif '[/FORMAT]' in line and format_:
                    format_ = False
                    # noinspection PyUnboundLocalVariable
                    self.format = FFFormat(data_lines)
                elif stream or format_:
                    data_lines.append(line)

            self.metadata = {}
            is_metadata = False
            stream_metadata_met = False

            for line in iter(p.stderr.readline, b''):
                line = line.decode('UTF-8')

                if 'Metadata:' in line and not stream_metadata_met:
                    is_metadata = True
                elif 'Stream #' in line:
                    is_metadata = False
                    stream_metadata_met = True
                elif is_metadata:
                    splits = line.split(',')
                    for s in splits:
                        m = re.search(r'(\w+)\s*:\s*(.*)$', s)
                        if m is not None:
                            # print(m.groups())
                            self.metadata[m.groups()[0]] = m.groups()[1].strip()

                if '[STREAM]' in line:
                    stream = True
                    data_lines = []
                elif '[/STREAM]' in line and stream:
                    stream = False
                    self.streams.append(FFFormat(data_lines))
                elif stream:
                    data_lines.append(line)

            p.stdout.close()
            p.stderr.close()

            for stream in self.streams:
                if stream.is_audio():
                    self.audio.append(stream)
                elif stream.is_video():
                    self.video.append(stream)
                elif stream.is_subtitle():
                    self.subtitle.append(stream)
                elif stream.is_attachment():
                    self.attachment.append(stream)
        else:
            raise IOError('No such media file or stream is not responding: ' + self.path_to_video)

    def __repr__(self):
        return "<FFprobe: {metadata}, {video}, {audio}, {subtitle}, {attachment}>".format(**vars(self))
