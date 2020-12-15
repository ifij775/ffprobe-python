import FFFrame

class FFAudioFrame(FFFrame):
    def sample_fmt(self):
        return self.__dict__['sample_fmt']
    def nb_samples(self):
        return int(self.__dict__['nb_samples'])
    def channels(self):
        return int(self.__dict__['channels'])
    def channel_layout(self):
        return self.__dict__['channel_layout']
        
