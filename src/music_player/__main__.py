from .interface.tui import VeridisTune
import time 
def main():
    time.sleep(0.1)
    try:
        app = VeridisTune()
        app.run()
    except Exception as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
