import textual
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button
from textual.widgets import Static, ListItem, ListView


class AudioPlayer(App):
    Bindings = [("d", 'toggle_dark', 'Toggle dark mode')]

    def compose(self) -> ComposeResult:
        yield Button("Music player lodaing", id= 'start')
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == 'textual-light' else "textual-light"
        )
        
if __name__ == "__main__":

    app = AudioPlayer()
    app.run()