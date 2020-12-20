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
from ffprobe.FFAudioStream import FFAudioStream
from ffprobe.FFVideoStream import FFVideoStream
from ffprobe.FFSubtitleStream import FFSubtitleStream
from ffprobe.FFAttachmentStream import FFAttachmentStream
from ffprobe.FFFrame import FFFrame
from ffprobe.FFPacket import FFPacket
from ffprobe.exceptions import FFProbeError


class FFProbe:
    """
    FFProbe wraps the ffprobe command and pulls the data into an object form::
        metadata=FFProbe('multimedia-file.mov')
    """

    def __init__(self,
                 path_to_video,
                 show_format=True,
                 show_streams=True,
                 show_frames=False,
                 show_packets=False,
                 select_streams='',
                 show_format_entries={},
                 show_stream_entries={},
                 show_stream_tags_entries={},
                 show_packet_entries={},
                 show_frame_entries={},
                 count_packets=False,
                 count_frames=False,
                 timeout=None):
        
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
                
            show_entries = []
            if show_format_entries:
                show_entries.append('format=' + ','.join(show_format_entries))
            if show_stream_entries:
                show_entries.append('stream=' + ','.join(show_stream_entries.add('codec_type')))
            if show_stream_tags_entries:
                show_entries.append('stream=' + ','.join(show_stream_tags_entries))
            if show_packet_entries:
                show_entries.append('packet=' + ','.join(show_packet_entries))
            if show_frame_entries:
                show_entries.append('frame=' + ','.join(show_frame_entries.add('codec_type')))
            if show_entries:
                cmd.extend(["-show_entries",':'.join(show_entries)])
            if select_streams:
                cmd.extend(["-select_streams",select_streams])
            if count_packets:
                cmd.extend(["-count_packets"])
            if count_frames:
                cmd.extend(["-count_frames"])
            cmd.append(self.path_to_video)

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stream = False
            ignore_line = False
            format_ = False
            frame = False
            packet = False
            
            self.format_data = None
            self.streams_data = []
            self.video_data = []
            self.audio_data = []
            self.subtitle_data = []
            self.attachment_data = []
            self.packets_data = []
            self.frames_data = []

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
                    data_dict = FFProbe.parse_data(data_lines)
                    if data_dict['codec_type'] == 'audio':
                        stream_obj = FFAudioStream(data_dict)
                        self.streams_data.append(stream_obj)
                        self.audio_data.append(stream_obj)
                    elif data_dict['codec_type'] == 'video':
                        stream_obj = FFVideoStream(data_dict)
                        self.streams_data.append(stream_obj)
                        self.video_data.append(stream_obj)
                    elif data_dict['codec_type'] == 'subtitle':
                        stream_obj = FFSubtitleStream(data_dict)
                        self.streams_data.append(stream_obj)
                        self.subtitle_data.append(stream_obj)
                    elif data_dict['codec_type'] == 'attachment':
                        stream_obj = FFAttachmentStream(data_dict)
                        self.streams_data.append(stream_obj)
                        self.attachment_data.append(stream_obj)
                    else:
                        print('stream_type unknown')
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
                    self.format_data = FFFormat(data_lines)
                elif line.startswith('[FRAME]'):
                    frame = True
                    data_lines = []
                elif frame and line.startswith('[/FRAME]'):
                    frame = False
                    # noinspection PyUnboundLocalVariable
                    self.frames_data.append(FFFrame(data_lines))
                elif line.startswith('[PACKET]'):
                    packet = True
                    ignore_line = False
                    data_lines = []
                elif packet and line.startswith('[/PACKET]'):
                    packet = False
                    ignore_line = False
                    # noinspection PyUnboundLocalVariable
                    self.packets_data.append(FFPacket(data_lines))
                elif packet:
                    if line.startswith('[SIDE_DATA]'):
                        ignore_line = True
                    elif line.startswith('[/SIDE_DATA]'):
                        ignore_line = False
                    elif not ignore_line:
                        data_lines.append(line)
                elif format_ or frame:
                    data_lines.append(line)

            self.metadata_data = {}
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
                            self.metadata_data[m.groups()[0]] = m.groups()[1].strip()
                            
            p.wait(timeout)

            p.stdout.close()
            p.stderr.close()
        else:
            raise IOError('No such media file or stream is not responding: ' + self.path_to_video)
            
    @staticmethod
    def parse_data(data_lines):
        data_dict = {}
        for line in data_lines:
            data_dict.update({key: value for key, value, *_ in [line.strip().split('=')]})
        return data_dict
            
    def format(self):
        return self.format_data
    def streams(self):
        return self.streams_data
    def audio_streams(self):
        return self.audio_data
    def video_streams(self):
        return self.video_data
    def packets(self):
        return self.packets_data
    def frames(self):
        return self.frames_data
    
    def get_packets_by_stream(self):
        packets_by_stream = {}
        for packet in self.packets_data:
            packets_by_stream.setdefault(packet.stream_index(),[]).append(packet)
        return packets_by_stream
    def get_frames_by_stream(self):
        frames_by_stream = {}
        for frame in self.frames_data:
            frames_by_stream.setdefault(frame.stream_index(),[]).append(frame)
        return frames_by_stream
        

    def __repr__(self):
        return "<FFprobe: {metadata_data}, {video_data}, {audio_data}, {subtitle_data}, {attachment_data}>".format(**vars(self))
    
    @staticmethod
    def check_ffprobe():
        try:
            with open(os.devnull, 'w') as tempf:
                subprocess.check_call(["ffprobe", "-h"], stdout=tempf, stderr=tempf)
        except FileNotFoundError:
            return False
        return True
