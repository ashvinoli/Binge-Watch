import re
import os

class c_list(list):
    def __init__(self,*args):
        if len(args)==1 and isinstance(args[0],list):
            super().__init__(args[0])
        else:
            super().__init__(args)

    def __getitem__(self,key):
        if key > len(self)-1:
            return self[key % len(self)]
        else:
            return super().__getitem__(key)
            
class episode:
    def __init__(self,episode,episode_number):
        self.episode_name = episode
        self.episode_number = episode_number

class util_functions:
    @classmethod
    def sort_them(cls,list_of_episodes):
        all_episodes = []
        all_numbers = True
        for _ in list_of_episodes:
            episode_name = _
            last_piece = os.path.split(episode_name)[-1]

            #Look for numbers in the episode's name if found use them to sort else just use the default i.e string name
            episode_number = re.findall("[0-9]+",last_piece)
            if len(episode_number)>0:
                actual_number = int("".join(episode_number))
                temp = episode(episode_name,actual_number)
                all_episodes.append(temp)
                all_numbers = True
            else:
                all_numbers = False
        if not all_numbers:
            all_episodes.sort(key = lambda x:x.episode_name)
        else:
            all_episodes.sort(key = lambda x:x.episode_number)
        return [x.episode_name for x in all_episodes]
        

    @classmethod
    def isvideo(cls,file_name):
        formats = (".webm",".mp4",".avi",".flv",".mkv",".m4v",".mov",".wmv")
        if file_name.endswith(formats):
            return True
        return False


