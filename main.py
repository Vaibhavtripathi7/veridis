import miniaudio

stream = miniaudio.stream_file('/home/vaibahv/Downloads/samajwadi.mp3')
with miniaudio.PlaybackDevice() as device:
    device.start(stream)
    input("enter to stop!")
