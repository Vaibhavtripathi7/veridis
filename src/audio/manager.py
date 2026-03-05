from src.audio.audio import AudioEngine
from src.library.musicfileman import MusicFiles
import threading
import time 

class Manager:
    def __init__(self):
        self.audio_engine = AudioEngine()
        self.music_files = MusicFiles()
        self.current_index = None
        self.is_playing = False 
        # self.thread_ = threading.Thread()

    def start_playlist(self, index):
        list_of_files = self.music_files.scanfiles()
        song_path = list_of_files[index]
        # print(song_path)
        self.current_index = index
        self.audio_engine.Play(str(song_path))
        self.is_playing = True
    
    def start_thread(self, watch_out):
        t_thread = threading.Thread(target = self.watch_out, daemon = True)
        t_thread.start()

    def watch_out(self):
        while True:
            if self.is_playing and not self.audio_engine.device.is_running:
                next_index = current_index + 1 
                self.start_playlist(next_index)
                # time.time.sleep(1)  # import time
            else:
                print("end of playlist")
                self.is_playing = False 
            
            time.time.sleep(1)
if __name__ == '__main__':
    object1 = Manager()
    object1.start_playlist(1)
    # object1.audio_engine.Play('/home/vaibahv/Downloads/samajwadi.mp3')
    input("enter to exit!")
    object1.audio_engine.close()
