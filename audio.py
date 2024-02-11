import pygame

class Music:
    def __init__(self,file_name):
        self.song = file_name
        pygame.mixer.init()

    def play_on_loop(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def play(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(0.5)

    def stop(self):
        pygame.mixer.music.stop()