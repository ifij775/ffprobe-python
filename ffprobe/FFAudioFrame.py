from ffprobe.FFFrame import FFFrame

class FFAudioFrame(FFFrame):
    def sample_fmt(self):
        return self._data['sample_fmt']
    def nb_samples(self):
        return int(self._data['nb_samples'])
    def channels(self):
        return int(self._data['channels'])
    def channel_layout(self):
        return self._data['channel_layout']
