import miniaudio 

class AudioEngine:
    def __init__(self):
        self.device = miniaudio.PlaybackDevice()
        self.is_paused = False
        self.stream = None

    def load(self,file_path):
        self.stream = miniaudio.stream_file(file_path)

    def Play(self, file_path : str):
        if self.device == None:
            raise RuntimeError('Device is not initialized')
        elif self.stream is not None:
            self.device.stop()
        self.load(file_path)
        self.device.start(self.stream)
        self.is_paused = False
        
    def Pause(self):
        self.is_paused = True
        self.device.stop()

    def close(self):
        self.device.stop()
        self.device.close()

if __name__ == '__main__':
    music = AudioEngine()
    music.Play('/home/vaibahv/Downloads/samajwadi.mp3')

    while True:
        cmd = input(">> ")
        if cmd == 'p':
            music.Pause()
            print("stopped for now!")
        elif cmd == 'q':
            music.close()
            break
