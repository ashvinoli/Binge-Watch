import os
import platform
import subprocess
from util_fun import util_functions, c_list

class video_file:
    def __init__(self,file_name ="",file_status = ""):
        self.file_name = file_name
        self.file_status = file_status

class playlist:
    def __init__(self,cur_dir ="",list_of_videos=None):
        if list_of_videos==None:
            self.list_of_videos = c_list()
        else:
            self.list_of_videos = list_of_videos
        self.cur_dir = cur_dir
        self.file_name = os.path.join(self.cur_dir,"playlist.txt")
        self.create_file()

    def init_play_status(self,start_at):
        if len(self.list_of_videos)>0:
            if (start_at < len(self.list_of_videos)):
                self.list_of_videos[start_at].file_status = "True"
            else:
                self.list_of_videos[0].file_status = "True"
                
    def save_file_status(self):
        my_file = open(self.file_name,"w")
        for item in self.list_of_videos:
            item.file_name = item.file_name.replace('\u200b',"")
            my_file.write(item.file_name + "|" +item.file_status+"\n")
        my_file.close()

    def create_file(self):
        if not os.path.exists(os.path.join(self.cur_dir,self.file_name)):
            my_file = open(self.file_name,"w")
            my_file.close()
        
    def read_file(self,start_at=0):
        my_file = open(self.file_name,"r")
        all_lines = my_file.readlines()
        length = len(all_lines)
        self.list_of_videos = c_list()
        if length>0:
            for line in all_lines:
                line = line.strip('\n')
                all_them = line.split("|")
                temp = video_file(all_them[0],all_them[1])
                self.list_of_videos.append(temp)
            my_file.close()
        else:
            my_file.close()
            all_files = map(lambda x:os.path.join(self.cur_dir,x),os.listdir(self.cur_dir))
            video_files = []
            for file_name in all_files:
                if util_functions.isvideo(file_name):
                    video_files.append(file_name)
            video_files = util_functions.sort_them(video_files)
            self.list_of_videos = c_list([video_file(x,"False") for x in video_files])
            self.init_play_status(start_at)
            self.save_file_status()

    def play_it(self,start_at):
        if start_at == "":
            self.read_file(0)
        else:
            self.read_file(start_at)
        if len(self.list_of_videos)>0:
            if start_at != "" and (start_at < len(self.list_of_videos)):
                for i in range(len(self.list_of_videos)):
                    if i==start_at:
                        self.list_of_videos[i].file_status = "True"
                    else:
                        self.list_of_videos[i].file_status = "False"
                self.save_file_status()
            for item in self.list_of_videos:
                if item.file_status=="True":
                    subprocess.Popen(["vlc.exe", item.file_name])
                    return item.file_name

    def play_custom(self,custom):
        self.read_file()
        if len(self.list_of_videos)>0:
            for i in range(len(self.list_of_videos)):
                if self.list_of_videos[i].file_status == "True":
                    self.list_of_videos[i].file_status = "False"
                    self.list_of_videos[i+custom].file_status = "True"
                    break
            self.save_file_status()
    
    def play_next(self):
        self.play_custom(1)

    def play_prev(self):
        self.play_custom(-1)
        
    








