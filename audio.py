import pygame

class Music:
    def __init__(self,file_name):
        self.song = file_name

    def play_on_loop(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1)

    def play(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0)

    def stop(self):
        pygame.mixer.music.stop()

class SoundEffect:
    def __init__(self, file_name):
        self.sound = pygame.mixer.Sound(file_name)

    def play(self):
        self.sound.set_volume(0.5)  # Adjust volume as needed
        self.sound.play()

    def stop(self):
        self.sound.stop()