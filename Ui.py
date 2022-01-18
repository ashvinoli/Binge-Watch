from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from playlist_rp import playlist, video_file
from util_fun import util_functions
import sys
import os

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Playlist_UI.ui', self)
        self.filename = "series.txt"
        self.movie_list = None
        self.threads = {}
        self.connect_functions()
        self.show()
        
    def connect_functions(self):
        self.reset_listbox()
        self.scrollarea_list.setWidget(self.list_locations)
        self.scroll_list_sub_locations.setWidget(self.list_sub_locations)
        self.list_locations.itemClicked.connect(self.list_locations_clicked)
        self.list_sub_locations.itemClicked.connect(self.list_sub_locations_clicked)
        self.button_add.clicked.connect(self.add_me)
        self.button_deleteall.clicked.connect(self.delete_all)
        self.button_resume.clicked.connect(self.resume)
        self.button_prev.clicked.connect(self.play_prev)
        self.button_next.clicked.connect(self.play_next)
        self.button_deleteselected.clicked.connect(self.delete_selected)
        self.entry_watchfrom.textChanged.connect(self.text_changed)
        
    def list_locations_clicked(self):
        selected_items = self.list_locations.selectedItems()
        self.list_sub_locations.clear()
        if len(selected_items)>0:
            location = selected_items[0].text().rstrip("\n")
            location = self.prepare_for_windows(location)
            if location!="":
                if os.path.exists(location):
                    subdirs = [os.path.join(location,dir) for dir in os.listdir(location) if os.path.isdir(os.path.join(location,dir))]
                    subdirs = util_functions.sort_them(subdirs)
                    self.list_sub_locations.addItems(subdirs)        
                    self.save_last_loc(location)

    def list_sub_locations_clicked(self):
        items_list_sub = self.list_sub_locations.selectedItems()
        if len(items_list_sub)>0:
            self.save_last_loc(items_list_sub[0].text())
        
    
    def save_last_loc(self,location):
        with open("last_location.txt","w") as f:
            f.write(location)
                            
    def read_series(self):
        if os.path.exists(self.filename):
            with open(self.filename,"r") as series_file:
                all_lines = [line for line in series_file.readlines() if os.path.exists(line.rstrip("\n"))]
            with open(self.filename,"w") as series_file:
                series_file.writelines(all_lines)
            return [line.rstrip("\n") for line in all_lines]
        else:
            series_file = open(self.filename,"w")
            series_file.close()
            return []	
		

    def reset_listbox(self):
        self.list_locations.clear()
        self.list_locations.addItems(self.read_series())
        
    def add_me(self):
        file_open = open(self.filename,"a")
        file_name =QFileDialog.getExistingDirectory(self,"Choose Directory")
        file_open.write(file_name+"\n")
        file_open.close()
        self.reset_listbox()

    def delete_all(self):
        file_open = open(self.filename,"w")
        file_open.close()
        self.reset_listbox()

    def delete_selected(self):
        selected_items = self.list_locations.selectedItems()
        if len(selected_items)>0:
            all_items = [self.list_locations.item(i) for i in range(self.list_locations.count())]
            file_open = open(self.filename,"w")
            for item in all_items:
                if item.text() != selected_items[0].text():
                    file_open.write(item.text()+"\n")
            file_open.close()
            self.reset_listbox()
            
    def prepare_for_windows(self,item):
        if os.name == 'nt':
            return item.replace("/","\\")
        else:
            return item

    def get_items(self):
        try:
            with open("last_location.txt","r") as f:
                return f.readline()
        except FileNotFoundError:
            return ""

    def movie_select(self):
        self.entry_curplay.setText("No movie/series selected. Please select one above.")

    def resume(self):
        file_path = self.get_items()
        if file_path != "":
            location = self.prepare_for_windows(file_path)
            play = playlist(location)
            start_at = self.entry_watchfrom.text()
            self.entry_watchfrom.setText("")
            if start_at != "":
                start_at = int(start_at)-1
            file_name = play.play_it(start_at)
            if file_name is not None:
                file_name = os.path.split(file_name)[-1]
                self.entry_curplay.setText(file_name)
            else:
                self.entry_curplay.setText("No video files in the directory!")
        else:
            self.movie_select()

    def play_next(self):
        items = self.get_items()
        if len(items)>0:
            location = self.prepare_for_windows(items)
            play = playlist(location)
            play.play_next()
            self.resume()
        else:
            self.movie_select()
            
    def play_prev(self):
        items = self.get_items()
        if len(items)>0:
            location = self.prepare_for_windows(items)
            play = playlist(location)
            play.play_prev()
            self.resume()
        else:
            self.movie_select()

    def text_changed(self):
        if not self.entry_watchfrom.text().isdigit():
            if self.entry_watchfrom.text()!="":
                self.entry_watchfrom.setText(self.entry_watchfrom.text()[:-1])
        
def run_function():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == "__main__":
    run_function()
