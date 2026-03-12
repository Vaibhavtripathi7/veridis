from .interface.tui import AudioPlayer
import time 
def main():
    time.sleep(0.1)
    try:
        app = AudioPlayer()
        app.run()
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
