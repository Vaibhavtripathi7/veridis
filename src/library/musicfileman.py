from pathlib import Path

class MusicFiles:
    def __init__(self):
        self.file_path = Path('/home/vaibahv/py-cli-music-player/src/library')

    def scanfiles(self):
        file_list = [str(x) for x in self.file_path.iterdir() if x.suffix == '.mp3' ]
        return file_list

    def music_file(self):
        file_name= {}
        music_list = self.scanfiles()
        for i,j in enumerate(music_list):
            string = j
            path_obj = Path(string)
            k = path_obj.name
            file_name.update({i : k})
        return file_name

    def get_file(self, index):
        list_of_file_path = self.scanfiles()
        return list_of_file_path[index]      

    
if __name__ == '__main__':
    mp3 = MusicFiles()
    list1 = mp3.scanfiles()
    list2 = mp3.music_file()
    print(list2, list1)

