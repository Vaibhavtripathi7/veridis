from pathlib import Path
import glob
import json
from typing import List, Dict, Union, Optional, Generator 

class MusicFiles:

    """
    Handles files system, metadata caching and directory navigation,
    Optimized for low-latency browsing in large directories
    """

    def __init__(self):
        self.root_path = Path.cwd()
        self.cache_file = self.root_path / ".vibe_cache.json"
        self.all_files = []
        self.allowed = ('.mp3', '.wav', '.flac', '.ogg')
        self.load_cache()

    def scanfiles(self) -> list:
        """ Recursive generator that yeilds path of audio files """

        try: 
            for path in self.root_path.rglob("*"):
                if path.is_file() and path.suffix.lower() in self.allowed:
                    yield str(path.relative_to(self.root_path))
        except PermissionError:
            pass
    

    def get_full_path(self,index:int) -> Optional[Path]:
        """ Retrives absolute path object"""
        if 0 <= index < len(self.all_files):
            relative_path_str = self.all_files[index]
            return self.root_path / relative_path_str
        return None

    def save_cache(self) -> None:
        """ Saves current library data in a JSON file"""
        try: 
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_files, f, indent=4)
        except Exception as e:
            print(f"erro saving cache: {e}")


    def load_cache(self, force_rescan = False) -> None:
        """ Loads cached paths """
        if self.cache_file.exists() and not force_rescan: 
            try:
                with open(self.cache_file, 'r', encoding= 'utf-8') as f:
                    self.all_files= json.load(f)
                if not self.all_files:
                    self.load_cache(force_rescan = True)
            except (json.JSONDecodeError, IOError):
                self.load_cache(force_rescan=True)
        else:
            self.all_files = list(self.scanfiles())
            self.save_cache()


    def get_full_path(self,index) -> Optional[Path]:
        """Retrives absolute Path object of using index"""
        if 0 <= index < len(self.all_files):
            relative_path_str = self.all_files[index]
            return self.root_path / relative_path_str
        return None

    def get_view_for_path(self, target_path: Path) -> List[Dict[str, Union[str, Path, bool]]]:
        """Returns a list of folders and music files in the target directory."""
        folders = []
        files = []
        
        if target_path != self.root_path:
            folders.append({
                "name": "⬅ .. [Back]", 
                "path": target_path.parent, 
                "is_dir": True
            })

        try:
            for p in sorted(target_path.iterdir()):
                if p.name.startswith('.'): continue
                
                if p.is_dir():
                    folders.append({
                        "name": f"📁 {p.name}", 
                        "path": p, 
                        "is_dir": True
                    })
                elif p.suffix.lower() in self.allowed:
                    files.append({
                        "name": f"🎵 {p.name}", 
                        "path": p, 
                        "is_dir": False
                    })
        except PermissionError:
            pass
            
        return folders + files
    
    def get_index_by_path(self, path) -> Optional[int]:
        """Finds where a file sits in playlist(CWD)"""
        try:
            rel_path = str(path.resolve().relative_to(self.root_path))
            return self.all_files.index(rel_path)
        except (ValueError, RuntimeError):
            return None 


if __name__ == '__main__':
    mp3 = MusicFiles()
    # list1 = mp3.scanfiles()
    # list2 = mp3.music_file()
    songs = mp3.get_file()
    print(songs)

