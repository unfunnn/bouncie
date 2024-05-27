import math
import random
import time

import pygame
from pygame.locals import *
import os
import mouse
import win32api
import win32con
import win32gui

screen_w, screen_h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
size = 2

class Bonnie:
    def __init__(self, x, y, spin_speed, velocity, angle, sprite):
        self.x = int(x)
        self.y = int(y)
        self.spin_speed = spin_speed
        self.velocity = velocity
        self.angle = angle
        self.sprite = sprite
        self.timer = 0

    def draw(self):
        print(self.x, self.y)
        screen.blit(self.sprite, (self.x-(bonnie_w/2), self.y-(bonnie_h/2)))

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if self.sprite == bonnie_img_2:
            self.timer += 1
        if self.timer >= 30:
            self.timer = 0
            self.sprite = bonnie_img

    def rot_center(self):
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)

        screen.blit(rotated_image, rotated_image.get_rect(center=self.sprite.get_rect(topleft=(self.x-(bonnie_w/2), self.y-(bonnie_h/2))).center).topleft)

    def bounce(self):
        if self.x <= 0+(bonnie_w*0.5):
            self.velocity[0]*=-(random.randint(8,12)/10)
            self.sprite = bonnie_img_2
        if self.x+(bonnie_w*0.5) >= screen_w:
            self.velocity[0]*=-(random.randint(8,12)/10)
            self.sprite = bonnie_img_2
        if self.y <= 0+(bonnie_h*0.5):
            self.velocity[1]*=-(random.randint(8,12)/10)
            self.sprite = bonnie_img_2
        if self.y+(bonnie_h*0.5) >= screen_h:
            self.velocity[1]*=-(random.randint(8,12)/10)
            self.sprite = bonnie_img_2


def always_on_top():
    win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def make_transparent():
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

fuchsia = (255, 0, 128)

screen = pygame.display.set_mode((screen_w, screen_h), NOFRAME)

bonnie_img = pygame.image.load("bonnie.png").convert_alpha()
#bonnie_img.set_colorkey((255, 2, 129))
bonnie_w = bonnie_img.get_width()
bonnie_h = bonnie_img.get_height()
bonnie_img = pygame.transform.scale(bonnie_img, (size*bonnie_w, size*bonnie_h))
bonnie_w = bonnie_img.get_width()
bonnie_h = bonnie_img.get_height()

bonnie_img_2 = pygame.image.load("bonnie2.png").convert_alpha()
bonnie_w2 = bonnie_img.get_width()
bonnie_h2 = bonnie_img.get_height()
bonnie_img_2 = pygame.transform.scale(bonnie_img_2, (size*bonnie_w2*(1/size), size*bonnie_h2*(1/size)))
bonnie_w2 = bonnie_img.get_width()
bonnie_h2 = bonnie_img.get_height()

bonnie = Bonnie(screen_w/2, screen_h/2, 5, [random.randint(-5, 5), random.randint(-5, 5)],0,bonnie_img)
while bonnie.velocity[0] == 0 or bonnie.velocity[1] == 0:
    bonnie.velocity = [random.randint(-5, 5), random.randint(-5, 5)]

pygame.display.set_caption("FISH HEADS!!")
pygame.display.set_icon(bonnie_img)

make_transparent()
screen.fill(fuchsia)
always_on_top()
bounce_timer = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0] and (bonnie.x-(0.5*bonnie_w) < pygame.mouse.get_pos()[0] < bonnie.x+(0.5*bonnie_w)) and (bonnie.y-(0.5*bonnie_h) < pygame.mouse.get_pos()[1] < bonnie.y+(0.5*bonnie_h)):
            bonnie.x, bonnie.y = pygame.mouse.get_pos()
            bonnie.velocity[0], bonnie.velocity[1] = pygame.mouse.get_rel()
            bonnie.velocity[0]*=0.5
            bonnie.velocity[1]*=0.5
            bonnie.spin_speed = int(math.sqrt((bonnie.velocity[0]**2) + (bonnie.velocity[1]**2)))

    screen.fill(fuchsia)
    #bonnie.draw()
    bonnie.move()
    bonnie.rot_center()
    bonnie.angle+=1
    bonnie.bounce()
    time.sleep(1/30)
    #print(bonnie.velocity)
    pygame.display.flip()
    pygame.display.update()