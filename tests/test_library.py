import pytest 
from music_player.library.musicfileman import MusicFiles

def test_filteing():

    nf = MusicFiles()
    files = ["song.mp3", "notes.txt", "album.jpg", "beat.wav"]
    filtered = [f for f in files if any(f.endswith(ext) for ext in nf.allowed)]

    assert "song.mp3" in filtered
    assert "beat.wav" in filtered
    assert "notes.txt" not in filtered

def test_music_list():
    nf = MusicFiles()
    assert nf.all_files == []