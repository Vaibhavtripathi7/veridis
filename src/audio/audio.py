import miniaudio 
import time
from typing import Tuple


class AudioEngine:

    """ 
    High perforance audio backend using miniaudio and system-time tracking,
    This class hanldes low-level playback, state management and time calculations.
    """
    def __init__(self):
        self.device = miniaudio.PlaybackDevice()
        self.stream = None
        self.total_frames = 0
        self.sample_rate = 0
        self.is_paused = False
        self.start_time = 0.0
        self.elapsed_before_pause = 0.0

    def Play(self, file_path : str) -> None:
        """Loads and starts playback for a specific file using its file path"""

        self.reset_state()

        try: 

            info = miniaudio.get_file_info(file_path)
            self.total_frames = info.num_frames
            self.sample_rate = info.sample_rate
            self.elapsed_before_pause = 0.0

            self.stream = miniaudio.stream_file(file_path)
            self.start_time = time.time()
            self.device.start(self.stream)

            self.is_paused = False

        except FileNotFoundError: 
            raise FileNotFoundError(f"Audio file not found")
        except Exception as e:
            raise RuntimeError(f"Could not play: {e}")
        
    def Pause(self) -> None:
        """Pauses Playback and saves the time passed"""
        if self.device.running and not self.is_paused:
            self.elapsed_before_pause += (time.time() - self.start_time)
            # self.pause_time = time.time()
            self.is_paused = True
            self.device.stop()

    def Resume(self) -> None:
        """ Resumes the playback from the point that it was paused"""
        if self.is_paused and self.stream:
            self.start_time = time.time()
            self.device.start(self.stream)
            self.is_paused = False
        
    def reset_state(self):
        if self.device.running:
            self.device.stop()
        self.start_time = 0
        self.elapsed_before_pause = 0
        self.total_frames = 0
        self.is_paused = False


    def close(self) -> None:
        """ Releases Playbackdevice"""
        self.device.stop()
        self.device.close()

    def get_progress(self) -> float:
        """Returns playback progress in percentage"""
        if self.total_frames == 0 or not self.device.running:
            return 0
            
        elapsed = self.elapsed_before_pause
        if not self.is_paused:
            elapsed += (time.time() - self.start_time)
            
        duration = self.total_frames / self.sample_rate
        
        percent = (elapsed / duration) * 100
        return min(max(percent, 0), 100)

    def get_time_strings(self):
        """Returns (elapsed_str, total_str) -- for UI"""

        if self.total_frames == 0 or self.sample_rate == 0:
            return "00:00", "00:00"

        total_seconds = int(self.total_frames / self.sample_rate) if self.sample_rate > 0 else 0
        
        if self.is_paused:
            curr = int(self.elapsed_before_pause)
        else:
            curr = int(self.elapsed_before_pause + (time.time() - self.start_time))

        if curr > total_seconds:
            curr = total_seconds

        def fmt(seconds):
            seconds = max(0, int(seconds))
            mins, secs = divmod(seconds, 60)
            return f"{mins:02}:{secs:02}"
            
        return fmt(curr), fmt(total_seconds)


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
