from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from playlist_rp import playlist, video_file
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
            location = selected_items[0].text().rstrip("\n").replace("/","\\")
            if location!="":
                subdirs = [os.path.join(location,dir) for dir in os.listdir(location) if os.path.isdir(os.path.join(location,dir))]
                if len(subdirs)>0:
                    self.list_sub_locations.addItems(subdirs)        
        

    def read_series(self):
        if os.path.exists(self.filename):
            series_file = open(self.filename,"r")
            all_lines = series_file.readlines()
            series_file.close()
            return all_lines
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
            all_items = [self.list_locations.item(i) for i in range(self.list_locations.count()-1)]
            file_open = open(self.filename,"w")
            for item in all_items:
                if item != selected_items[0]:
                    file_open.write(item.text())
            file_open.close()
            self.reset_listbox()
            
            
    def resume(self):
        items = self.list_locations.selectedItems()
        items_list_sub = self.list_sub_locations.selectedItems()
        if len(items_list_sub)>0:
            items = items_list_sub
        if len(items)>0:
            location = items[0].text().rstrip("\n").replace("/","\\")
            play = playlist(location)
            start_at = self.entry_watchfrom.text()
            self.entry_watchfrom.setText("")
            if start_at != "":
                start_at = int(start_at)-1
            file_name = play.play_it(start_at)
            if file_name is not None:
                file_name = file_name.split("\\")[-1]
                self.entry_curplay.setText(file_name)
            else:
                self.entry_curplay.setText("No video files in the directory!")

    def play_next(self):
        items = self.list_locations.selectedItems()
        items_list_sub = self.list_sub_locations.selectedItems()
        if len(items_list_sub)>0:
            items = items_list_sub
        if len(items)>0:
            location = items[0].text().rstrip("\n").replace("/","\\")
            play = playlist(location)
            play.play_next()
            self.resume()
            
    def play_prev(self):
        items = self.list_locations.selectedItems()
        items_list_sub = self.list_sub_locations.selectedItems()
        if len(items_list_sub)>0:
            items = items_list_sub
        if len(items)>0:
            location = items[0].text().rstrip("\n").replace("/","\\")
            play = playlist(location)
            play.play_prev()
            self.resume()

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
