import os
import platform
import subprocess

class video_file:
    def __init__(self,file_name ="",file_status = ""):
        self.file_name = file_name
        self.file_status = file_status

class playlist:
    def __init__(self,cur_dir ="",list_of_videos=None):
        if list_of_videos==None:
            self.list_of_videos = []
        else:
            self.list_of_videos = list_of_videos
        
        self.cur_dir = cur_dir
        self.file_name = os.path.join(self.cur_dir,"playlist.txt")
        self.create_file()

    def init_play_status(self,start_at):
        if len(self.list_of_videos)>0:
            self.list_of_videos[start_at].file_status = "True"

    def save_file_status(self):
        my_file = open(self.file_name,"w")
        for item in self.list_of_videos:
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
        self.list_of_videos = []
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
            for file_name in all_files:
                if self.isvideo(file_name):
                    temp = video_file(file_name,"False")
                    self.list_of_videos.append(temp)
            self.init_play_status(start_at)
            self.save_file_status()

    def play_it(self,start_at=0):
        self.read_file(start_at)
        if len(self.list_of_videos)>0:
            for item in self.list_of_videos:
                if item.file_status=="True":
                    subprocess.Popen(["vlc.exe", item.file_name])
                    return item.file_name
    
    def play_next(self):
        self.read_file()
        if len(self.list_of_videos)>0:
            if self.list_of_videos[-1].file_status == "True":
                self.list_of_videos[-1].file_status = "False"
                self.list_of_videos[0].file_status = "True"
            else:
                for i in range(len(self.list_of_videos)-1):
                    if self.list_of_videos[i].file_status == "True":
                        self.list_of_videos[i].file_status = "False"
                        self.list_of_videos[i+1].file_status = "True"
                        break
            self.save_file_status()

    def play_prev(self):
        self.read_file()
        if len(self.list_of_videos)>0:
            if self.list_of_videos[0].file_status == "True":
                self.list_of_videos[0].file_status = "False"
                self.list_of_videos[-1].file_status = "True"
            else:
                for i in range(1,len(self.list_of_videos)):
                    if self.list_of_videos[i].file_status == "True":
                        self.list_of_videos[i].file_status = "False"
                        self.list_of_videos[i-1].file_status = "True"
                        break
            self.save_file_status()
        
    def isvideo(self,file_name):
        formats = (".webm",".mp4",".avi",".flv",".mkv")
        if file_name.endswith(formats):
            return True
        return False








