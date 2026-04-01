# Veridis: High-Performance CLI Audio Engine

[![PyPI version](https://badge.fury.io/py/veridis.svg)](https://badge.fury.io/py/veridis)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

Veridis is a fast,  lightweight Terminal User Interface (TUI) music player designed for low-latency audio playback and flexible resource management.

## Technical Architecture

Veridis has a separate, **multi-threaded structure**. This design keeps the user interface responsive while delivering high-quality audio output:

* **Concurrency Model:** It uses a dual-thread architecture. A background daemon thread manages the C-bound **Miniaudio** backend. The main event loop handles the reactive TUI. This setup prevents UI jerkiness during hardware-intensive playback.
* **Memory Optimization:** Uses Python **generators** to index libraries, which keeps memory use at **O(1)** while traversing the filesystem. This makes sure that boot times are almost instant, even with libraries that have more than 10,000 files.
* **Reactive Design System:** Made with the **Textual** framework and a custom CSS-in-TUI design system. It uses dynamic layout reflows to change the way it looks based on the size of the terminal without messing up the visual hierarchy.

## Tech Stack

* **Core:** Python 3.13+
* **Audio Engine:** [Miniaudio](https://pypi.org/project/miniaudio/) 
* **UI Framework:** [Textual](https://textual.textualize.io/)
* **Build System:** [Poetry](https://python-poetry.org/)
* **Testing:** [Pytest](https://pytest.org/) & [Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## Installation & Setup

Veridis is packaged as a standard Python module.

### 1.System Dependencies
Depending on your OS, you may need the following audio developement headers:

#### Linux(Debian/Ubuntu/EndeavourOS)
```bash
# Debian/Ubuntu
sudo apt-get install python3-dev libasound2-dev build-essential

#Arch/EndeavourOS
sudo pacman -S alsa-lib base-devel
```

#### MacOS(untested)
```bash
brew install pkg-config
```

#### Windows(untested)
```powershell
# Install via Chocolatey
# Requires C++ build tools for miniaudio compilation
choco install visualcpp-build-tools
```

### 2. Option A: Quick install (via PyPI)
```bash

pip install veridis

# If environment confilct problem occurs then try (recommended):
# Install pipx, if you don't have that:

sudo pacman -S python-pipx  # EndeavourOS/Arch
sudo apt install pipx       # Debian/Ubuntu

pipx install veridis
# After installation, launch by simply typing:
veridis
```

### 3. Option B: Build and Install (Dev Mode)

Ensure you have **Poetry** installed.

```bash
# Clone the repository
git clone https://github.com/Vaibhavtripathi7/veridis.git
cd veridis
# Install dependencies using poetry
poetry install
```
### 4. Execution 
```Bash
poetry run veridis 
```

## Control Interface

| Key | Function |
| :---: | :---: |
| `Space`| Play/Pause |
| `N`| Increment to Next Track |
| `Enter`| Select Directory/Initialize Playback |
| `D` | Toggle Dark/Light mode |
| `Q`| Shutdown |


## Verification(Unit testing)

We use Mocking to simulate the audio engine, allowing tests to run in headless CI environments.

```Bash
poetry run pytest -v
```

## License 

[MIT License](https://github.com/Vaibhavtripathi7/veridis/blob/master/LICENSE)
