# coding:utf-8
import pygame
import sys
import os
from moviepy import VideoFileClip
import easygui as eg
from pygame.locals import *
from config import *
from lottery import *
from ui import *

rolling = False
running = True
n = 10


class InterFace():
    def __init__(self):
        pygame.init()
        game_icon = pygame.image.load(get_path('assets/images/icon.png'))
        game_caption = 'Yet Another Lottery for C10'
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption(game_caption)
        self.ratio = GLOBAL_RATIO
        self.size = self.width, self.height = 1920*self.ratio, 1080*self.ratio
        self.canvas = pygame.display.set_mode(self.size)
        self.load_background()
        self.load_init_result_card()

    def load_background(self):
        Image('background.webp').draw(self.canvas, self.width/2, self.height/2)

    def load_init_result_card(self):
        for pos in RESULTCARD_POSX:
            Image("resultcard-bg.webp").draw(self.canvas,
                                             self.width*pos, self.height*0.45)
            Image("placeholder-face.webp", GLOBAL_RATIO*0.8).draw(self.canvas,
                                                                  self.width*pos, self.height*0.45)
            ColorSurface(COLOR.BLACK, 171*GLOBAL_RATIO, 80*GLOBAL_RATIO,
                         170).draw(self.canvas, self.width*pos, self.height*0.6)
            Text("是谁呢", "HYWenHei-85W.ttf", COLOR.WHITE,
                 20).draw(self.canvas, self.width*pos, self.height*0.6)
            ColorSurface(COLOR.BLACK, 171*GLOBAL_RATIO, 40*GLOBAL_RATIO,
                         170).draw(self.canvas, self.width*pos, self.height*0.66)
            Text(f"好期待呢", "HYWenHei-85W.ttf", COLOR.WHITE,
                 10).draw(self.canvas, self.width*pos, self.height*0.66)

    def load_result_card(self, n):
        items = get_items(n)
        for i in range(0, n):
            pos = RESULTCARD_POSX[i]
            Image("resultcard-bg.webp").draw(self.canvas,
                                             self.width*pos, self.height*0.45)
            if items[i].image != '':
                ImageFixed(f"items/{items[i].image}", 171*GLOBAL_RATIO, 357*GLOBAL_RATIO).draw(self.canvas,
                                                                                               self.width*pos, self.height*0.45)
            else:
                Image("placeholder-face.webp", GLOBAL_RATIO*0.8).draw(self.canvas,
                                                                      self.width*pos, self.height*0.45)
            ColorSurface(COLOR.BLACK, 171*GLOBAL_RATIO, 80*GLOBAL_RATIO,
                         170).draw(self.canvas, self.width*pos, self.height*0.6)
            Text(items[i].item, "HYWenHei-85W.ttf", COLOR.WHITE,
                 20).draw(self.canvas, self.width*pos, self.height*0.6)
            ColorSurface(COLOR.BLACK, 171*GLOBAL_RATIO, 40*GLOBAL_RATIO,
                         170).draw(self.canvas, self.width*pos, self.height*0.66)
            Text(f"×{items[i].weight}", "HYWenHei-85W.ttf", COLOR.WHITE,
                 10).draw(self.canvas, self.width*pos, self.height*0.66)
        for i in range(n,10):
            pos = RESULTCARD_POSX[i]
            Image("resultcard-bg.webp").draw(self.canvas,
                                             self.width*pos, self.height*0.45)
            Image("placeholder-face.webp", GLOBAL_RATIO*0.8).draw(self.canvas,
                                                                  self.width*pos, self.height*0.45)
            ColorSurface(COLOR.BLACK, 171*GLOBAL_RATIO, 80*GLOBAL_RATIO,
                         170).draw(self.canvas, self.width*pos, self.height*0.6)
            Text("这里没人", "HYWenHei-85W.ttf", COLOR.WHITE,
                 20).draw(self.canvas, self.width*pos, self.height*0.6)
            ColorSurface(COLOR.BLACK, 171*GLOBAL_RATIO, 40*GLOBAL_RATIO,
                         170).draw(self.canvas, self.width*pos, self.height*0.66)
            Text(f"只抽了{n}人哦", "HYWenHei-85W.ttf", COLOR.WHITE,
                 10).draw(self.canvas, self.width*pos, self.height*0.66)

    def play_gacha_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(get_path("./assets/audios/zzz-gacha.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def play_gacha_video(self):
        movie = VideoFileClip(get_path("./assets/videos/gacha.mp4"))
        frames = movie.iter_frames()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            frame = next(frames, None)
            if frame is None:
                return
            else:
                pygame_frame = pygame.surfarray.make_surface(
                    frame.swapaxes(0, 1))
                self.canvas.blit(pygame_frame, (0, 0))
                clock.tick(movie.fps)
                pygame.display.update()

    def main_interface(self):
        config_button = ButtonImage('button.webp', GLOBAL_RATIO*1.3)
        config_button.draw(self.canvas, self.width*0.3, self.height*0.9)
        Text("更改配置", "HYWenHei-85W.ttf", COLOR.BLACK,
             30).draw(self.canvas, self.width*0.3, self.height*0.9)
        roll_button = ButtonImage('button.webp', GLOBAL_RATIO*1.3)
        roll_button.draw(self.canvas, self.width*0.7, self.height*0.9)
        if rolling:
            Text("停止抽奖", "HYWenHei-85W.ttf", COLOR.BLACK,
                 30).draw(self.canvas, self.width*0.7, self.height*0.9)
        else:
            Text("开始抽奖", "HYWenHei-85W.ttf", COLOR.BLACK,
                 30).draw(self.canvas, self.width*0.7, self.height*0.9)
        while True:
            if rolling == True:
                self.load_result_card(n)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    roll_button.handle_event(self.on_roll_button_clicked)
                    config_button.handle_event(self.on_config_button_clicked)
                    continue
            pygame.time.delay(10)
            pygame.display.update()

    def on_config_button_clicked(self):
        global n
        n = int(eg.integerbox("设置抽取人数","Settings",10,1,10))

    def on_roll_button_clicked(self):
        global rolling
        rolling = not rolling
        if rolling:
            self.play_gacha_audio()
            self.play_gacha_video()
            pygame.time.delay(500)
            self.load_background()
        else:
            pygame.mixer.music.fadeout(500)
        self.main_interface()


if __name__ == '__main__':
    try:
        if not os.path.exists('item.csv'):
            print("Namelist Required. Exiting.")
            sys.exit()
        scene = InterFace()
        scene.main_interface()
    except not SystemExit:
        eg.exceptionbox("Error orrured. Program is exiting.", "Error")
