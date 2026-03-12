import sys
from pathlib import Path

# This line ensures Python can find your 'src' folder
sys.path.append(str(Path(__file__).parent))

from src.interface.tui import AudioPlayer

if __name__ == "__main__":
    app = AudioPlayer()
    app.run()