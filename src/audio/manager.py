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
        self.autoplay_enabled = True
        self._thread_started = False

    def start_playlist(self, index):
        self.audio_engine.Pause()
        song_path = self.music_files.get_full_path(index)
        # print(song_path)
        self.current_index = index
        self.audio_engine.Play(str(song_path))
        self.is_playing = True
    

    def next_song(self):
        total_songs = len(self.music_files.all_files)
        if total_songs > 0 :
            new_index = ( self.current_index + 1 ) % total_songs
            self.start_playlist(new_index)

    def pause_song(self):
        if self.audio_engine.device.running:

            self.audio_engine.Pause()
        else:
            self.audio_engine.Resume()


    def start_thread(self):
        if not self._thread_started:

            t_thread = threading.Thread(target = self.watch_out, daemon = True)
            t_thread.start()
            self._thread_started = True 

    def watch_out(self):
        while True:
            if self.is_playing: 
                if not self.audio_engine.device.running and not self.audio_engine.is_paused:
                    self.is_playing = False
                    self.audio_engine.reset_state()
                    if self.autoplay_enabled:
                        self.next_song() 
            time.sleep(0.3)

    def get_progress_percentage(self):
        return self.audio_engine.get_progress()

    def play_by_path(self, path):
        """Play a specific file path directly from the browser."""
        self.audio_engine.Play(str(path))
        self.is_playing = True
        # Note: You'll need to update self.current_index logic 
        # if you still want 'next_song' to work from here.
        
if __name__ == '__main__':
    object1 = Manager()
    object1.start_playlist(1)
    object1.start_thread()
    input("enter to exit!")
    object1.audio_engine.close()
