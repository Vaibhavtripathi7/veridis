import miniaudio 
import time



class AudioEngine:
    def __init__(self):
        self.device = miniaudio.PlaybackDevice()
        self.is_paused = False
        self.stream = None
        self.total_frames = 0
        self.sample_rate = 0

        self.start_time = 0
        self.elapsed_before_pause = 0


    def load(self,file_path : str):
        self.stream = miniaudio.stream_file(file_path)
        

    def Play(self, file_path : str):
        if self.device == None:
            raise RuntimeError('Device is not initialized')
        elif self.stream is not None:
            self.device.stop()

        self.reset_state()
        info = miniaudio.get_file_info(file_path)
        self.total_frames = info.num_frames
        self.sample_rate = info.sample_rate

        self.elapsed_before_pause = 0
        self.start_time = time.time()
        self.load(file_path)
        
        # def stream_generator():
            # for chunk in self.stream:
                # self.current_frame +=  len(chunk) //4
                # yield chunk

        # wrapped_stream = self.progress_wrapper(self.stream)
        self.device.start(self.stream)
        self.is_paused = False
        
    def Pause(self):
        if self.device.running and not self.is_paused:
            self.elapsed_before_pause += (time.time() - self.start_time)
            self.pause_time = time.time()
            self.is_paused = True
            self.device.stop()

    def Resume(self):
        if self.is_paused and self.stream:
            self.start_time = time.time()
            self.device.start(self.stream)
            self.is_paused = False

    def close(self):
        self.device.stop()
        self.device.close()

    def get_progress(self):
        if self.total_frames == 0 or not self.device.running:
            return 0
            
        elapsed = self.elapsed_before_pause
        if not self.is_paused:
            elapsed += (time.time() - self.start_time)
            
        duration = self.total_frames / self.sample_rate
        
        # Float math first, then multiply
        percent = (elapsed / duration) * 100
        return min(max(percent, 0), 100)

    def get_time_strings(self):
        """Returns (elapsed_str, total_str)"""

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

    def reset_state(self):
        if self.device.running:
            self.device.stop()
        self.start_time = 0
        self.elapsed_before_pause = 0
        self.total_frames = 0
        self.is_paused = False


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
