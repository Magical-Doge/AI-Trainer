# @Environments require:
#
# Package               Version
# --------------------- ---------
# python                3.7.x
# pygame                2.1.2
# keyboard              0.13.5
# os
# random

import random
import os
import pygame


class Musicplayer():
    def __init__(self):
        pygame.mixer.init()
        # 获取当前文件所在的绝对路径
        file_path = os.path.split(os.path.realpath(__file__))[0]
        try:
            os.mkdir(file_path, "MUSIC")  # 无MUSIC文件夹则创建
        except:
            pass
        music_path = os.path.join(file_path, "MUSIC")
        # music_path = './MUSIC'
        self.music_list = []
        f = os.listdir(music_path)  # 获取所有的文件名列表
        for file_name in f:
            file_format = file_name[-4:]
            if file_format.lower() in (".mp3", ".wav"):  # 只将其中的.mp3文件写入music_list
                music = file_name[:-4]
                self.music_list.append(music)


    def music_play(self):
        self.music_name = random.choice(self.music_list)
        try:
            pygame.mixer.music.load(r"MUSIC/%s.mp3" % self.music_name)
            #    print("\n正在播放: %s" % music_name)
            pygame.mixer.music.play()
            return self.music_name
        except Exception as e:
            print(e)

    def pause_music(self):
        print("暂停播放\n")
        pygame.mixer.music.pause()

    def unpause_music(self):
        print("继续播放\n")
        pygame.mixer.music.unpause()

    def stop_music(self):
        print("停止播放\n")
        pygame.mixer.music.stop()

    def skip_music(self):
        i = random.randint(0, len(self.music_list) - 1)
        self.music_name = self.music_list[i]
        self.music_play(self.music_name)



