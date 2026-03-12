import textual
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Footer, Header, Button
from textual.widgets import Static, ListItem, ListView, Label, ProgressBar 
from src.music_player.audio.manager import Manager
from textual.reactive import reactive
import random



class AudioPlayer(App):

    current_dir_items = reactive([])

    BINDINGS = [
    ("d", "toggle_dark", "Toggle Dark Mode"),
    ("space", "pause_play", "Pause/Play"),
    ("n", "next_song", "Next Track"),
    ]

    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.manager = Manager()
        self.manager.start_thread()
        self.navigate_to(self.manager.music_files.root_path)
        self.set_interval(0.5, self.update_progress)

    def navigate_to(self, path):
        self.current_dir_items = self.manager.music_files.get_view_for_path(path)
        try:
            sidebar = self.query_one("#sidebar")
            sidebar.border_title = f"{path.name if path.name else '/'}"
        except:
            pass 
            
    
    def watch_current_dir_items(self, items: list) -> None:
            """Reactive watcher that repopulates the ListView whenever items change."""
            list_view = self.query_one('#song-list', ListView)
            list_view.clear()
            for item in items:
                list_view.append(ListItem(Label(item["name"])))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
            index = event.list_view.index
            selected_item = self.current_dir_items[index]

            if selected_item["is_dir"]:
                self.navigate_to(selected_item["path"])
            else:
                self.manager.play_by_path(selected_item["path"])
                self.query_one("#now-playing").update(f"🎶 {selected_item['path'].name}")

    def compose(self) -> ComposeResult:
        yield Header() 
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Your library", id='sidebar-title')
                yield ListView(id='song-list')       
        
            with Vertical(id="main-zone"):
                yield Visualizer(id="Visualizer")
                yield Label("No song playing", id="now-playing")
            with Container(id="footer-zone"):
                yield Label("00:00", id="time-elapsed") 
                yield ProgressBar(total=100, show_eta = False, show_bar=True, id="progress")
                yield Label("00:00", id="time-total")   
        yield Footer()
        

    def update_progress(self):
            if hasattr(self, 'manager'):
                if not self.manager.is_playing:
                    self.query_one("#progress", ProgressBar).progress = 0
                    self.query_one("#time-elapsed").update("00:00")
                    self.query_one("#time-total").update("00:00")
                    return 
                self.query_one("#progress", ProgressBar).progress = self.manager.get_progress_percentage()
                elapsed_str, total_str = self.manager.audio_engine.get_time_strings()
                self.query_one("#time-elapsed").update(elapsed_str)
                self.query_one("#time-total").update(total_str)

    def action_pause_play(self) -> None:
        self.manager.pause_song()
        status = "Paused" if not self.manager.audio_engine.device.running else "Playing"
        self.notify(f"Music {status}")
        
    def action_next_song(self)-> None:
        self.manager.next_song()

class Visualizer(Static):
    def on_mount(self):
        self.set_interval(0.1, self.update_bars)

    def update_bars(self):
        if hasattr(self.app, "manager") and self.app.manager.is_playing:
            bars = ["▂", "▃", "▄", "▅", "▆", "▇", "█"]
            viz_str = "".join(random.choice(bars) for _ in range(40))
            self.update(viz_str)

        else:
            self.update("_" * 50)

if __name__ == "__main__":

    app = AudioPlayer()
    app.run()