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

from ffprobe.FFFormat import FFFormat
from ffprobe.FFStream import FFStream
from ffprobe.FFFrame import FFFrame
from ffprobe.FFPacket import FFPacket
from ffprobe.exceptions import FFProbeError


class FFProbe:
    """
    FFProbe wraps the ffprobe command and pulls the data into an object form::
        metadata=FFProbe('multimedia-file.mov')
    """

    def __init__(self, path_to_video, show_format=True, show_streams=True, show_frames=False, show_packets=False, show_entries='', select_streams='', count_frames=False, timeout=None):
        self.path_to_video = path_to_video

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
            if show_entries:
                cmd.extend(["-show_entries",show_entries])
            if select_streams:
                cmd.extend(["-select_streams",select_streams])
            if count_frames:
                cmd.extend(["-count_frames"])
            cmd.append(self.path_to_video)

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stream = False
            ignore_line = False
            format_ = False
            frame = False
            packet = False
            self.format = None
            self.streams = []
            self.video = []
            self.audio = []
            self.subtitle = []
            self.attachment = []
            self.packets = []
            self.frames = []

            for line in iter(p.stdout.readline, b''):
                line = line.decode('UTF-8')
                if line.startswith('[STREAM]'):
                    stream = True
                    ignore_line = False
                    data_lines = []
                elif stream and line.startswith('[/STREAM]'):
                    stream = False
                    ignore_line = False
                    # noinspection PyUnboundLocalVariable
                    self.streams.append(FFStream(data_lines))
                elif stream:
                    if line.startswith('[SIDE_DATA]'):
                        ignore_line = True
                    elif line.startswith('[/SIDE_DATA]'):
                        ignore_line = False
                    elif not ignore_line:
                        data_lines.append(line)
                elif line.startswith('[FORMAT]'):
                    format_ = True
                    data_lines = []
                elif format_ and line.startswith('[/FORMAT]'):
                    format_ = False
                    # noinspection PyUnboundLocalVariable
                    self.format = FFFormat(data_lines)
                elif line.startswith('[FRAME]'):
                    frame = True
                    data_lines = []
                elif frame and line.startswith('[/FRAME]'):
                    frame = False
                    # noinspection PyUnboundLocalVariable
                    self.frames.append(FFFrame(data_lines))
                elif line.startswith('[PACKET]'):
                    packet = True
                    ignore_line = False
                    data_lines = []
                elif packet and line.startswith('[/PACKET]'):
                    packet = False
                    ignore_line = False
                    # noinspection PyUnboundLocalVariable
                    self.packets.append(FFPacket(data_lines))
                elif packet:
                    if line.startswith('[SIDE_DATA]'):
                        ignore_line = True
                    elif line.startswith('[/SIDE_DATA]'):
                        ignore_line = False
                    elif not ignore_line:
                        data_lines.append(line)
                elif format_ or frame:
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
                            
            p.wait(timeout)

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
            
    def get_format(self):
        return self.format
    def get_streams(self):
        return self.streams
    def get_audio_streams(self):
        return self.audio
    def get_video_streams(self):
        return self.video
    def get_packets(self):
        return self.packets
    def get_frames(self):
        return self.frames
    def get_packets_by_stream(self):
        packets_by_stream = {}
        for stream in self.streams:
            packets_by_stream[stream['index']] = []
        for packet in self.packets:
            packets_by_stream[packet['stream_index']].append(packet)
        return packets_by_stream
    def get_frames_by_stream(self):
        frames_by_stream = {}
        for stream in self.streams:
            frames_by_stream[stream['index']] = []
        for frame in self.frames:
            frames_by_stream[frame['stream_index']].append(frame)
        return frames_by_stream
        

    def __repr__(self):
        return "<FFprobe: {metadata}, {video}, {audio}, {subtitle}, {attachment}>".format(**vars(self))
    
    @staticmethod
    def check_ffprobe():
        try:
            with open(os.devnull, 'w') as tempf:
                subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
        except FileNotFoundError:
            return False
        return True
