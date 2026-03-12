from .audio import AudioEngine
from ..library.musicfileman import MusicFiles
import threading
import time
from typing import Optional
from pathlib import Path 

class Manager:
    def __init__(self):

        """
        Connects the audio engine, file system and user interface, manages playlist logic 
        and background monitoring
        """
        self.audio_engine = AudioEngine()
        self.music_files = MusicFiles()
        self.current_index = None
        self.is_playing = False 
        self.autoplay_enabled = True
        self._thread_started = False

    def start_playlist(self, index) -> None:
        """Plays a song based on its index in current library"""
        self.audio_engine.Pause()
        song_path = self.music_files.get_full_path(index)
        self.current_index = index
        self.audio_engine.Play(str(song_path))
        self.is_playing = True
    

    def next_song(self) -> None:
        """It plays next audio by using updated index"""
        total_songs = len(self.music_files.all_files)
        if total_songs > 0 :
            new_index = ( self.current_index + 1 ) % total_songs
            self.start_playlist(new_index)

    def pause_song(self) -> None:
        """Pauses the song"""
        if self.audio_engine.device.running:

            self.audio_engine.Pause()
        else:
            self.audio_engine.Resume()


    def start_thread(self) -> None:
        """Starts the thread for monitring the playback"""
        if not self._thread_started:

            t_thread = threading.Thread(target = self.watch_out, daemon = True)
            t_thread.start()
            self._thread_started = True 

    def watch_out(self) -> None:
        """ lo0p to handle song ending and autoplay"""
        while True:
            if self.is_playing: 
                if not self.audio_engine.device.running and not self.audio_engine.is_paused:
                    self.is_playing = False
                    self.audio_engine.reset_state()
                    if self.autoplay_enabled:
                        self.next_song() 
            time.sleep(0.3)

    def get_progress_percentage(self) -> float:
        """Returns percetange value of how much song completed using get progress method"""
        return self.audio_engine.get_progress()

    def play_by_path(self, path):
        """Play a specific file path directly from the browser."""
        self.audio_engine.Play(str(path))
        self.is_playing = True
        self.current_index = self.music_files.get_index_by_path(path)
        
if __name__ == '__main__':
    object1 = Manager()
    object1.start_playlist(1)
    object1.start_thread()
    input("enter to exit!")
    object1.audio_engine.close()
