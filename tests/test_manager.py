from unittest.mock import MagicMock
from music_player.audio.manager import Manager
from unittest.mock import patch

@patch('music_player.audio.manager.AudioEngine')
@patch('music_player.audio.manager.MusicFiles')

def test_manager_init(mock_files, mock_engine):
    manager = Manager()
    assert manager.is_playing is False

def test_pause():
    manager = Manager()
    manager.audio_engine = MagicMock()
    manager.audio_engine.device.running = True

    manager.pause_song()

    assert manager.is_playing is False
    manager.audio_engine.Pause.assert_called_once()

def test_next_song():
    manager = Manager()
    manager.audio_engine = MagicMock()
    manager.music_files.all_files = ["song0.mp3", "song1.mp3", "song2.mp3"]
    manager.current_index = 0
    manager.next_song()

    assert manager.current_index == 1
    manager.audio_engine.Play.assert_called()

def test_stop_state():
    manager = Manager()
    manager.audio_engine = MagicMock()
    manager.is_playing = True

    manager.audio_engine.device.running = False
    manager.audio_engine.is_paused = False

    assert manager.is_playing is True