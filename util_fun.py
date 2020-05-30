import re
import os
class episode:
    def __init__(self,episode,episode_number):
        self.episode_name = episode
        self.episode_number = episode_number

class util_functions:
    @classmethod
    def sort_them(cls,list_of_episodes):
        all_episodes = []
        for _ in list_of_episodes:
            episode_name = _
            last_piece = os.path.split(episode_name)[-1]
            episode_number = re.findall("[0-9]+",last_piece)
            if len(episode_number) >0:
                episode_number = int(episode_number[0])
            else:
                episode_number = 0
            temp = episode(episode_name,episode_number)
            all_episodes.append(temp)
        all_episodes.sort(key = lambda x:x.episode_name)
        all_episodes.sort(key = lambda x:x.episode_number)
        return [x.episode_name for x in all_episodes]



