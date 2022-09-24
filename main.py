import os
import pygame
import tkinter as tk
import ctypes
import node_api as na

from threading import Thread

user32 = ctypes.windll.user32
display_res = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

root = tk.Tk()
root.state('zoomed')
pygame_embed = tk.Frame(root, width=display_res[0], height=display_res[1])
pygame_embed.pack()

# embed pygame window
os.environ['SDL_WINDOWID'] = str(pygame_embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode(display_res)
pygame.display.init()
pygame.display.update()
na.init(screen)

na.create_node(na.Node("Image Texture")
               .set_xy((100, 100))
               .set_desciption("testing the description mechanic with a lot of text")
               .add_input("input 1")
               .add_input("input 2")
               .add_output("output 1")
               .add_output("output 2")
               )
na.create_node(na.Node("Dilate/Erode")
               .set_xy((100, 100))
               .add_input("input 1")
               .add_input("input 2")
               .add_output("output 1")
               .add_output("output 2")
               )
na.create_node(na.Node("ATC")
               .set_desciption("atc")
               .add_output("")
               )


def pygame_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((34, 34, 34))

        mouse = pygame.mouse.get_pressed()
        na.update(mouse)
        na.render_all()
        pygame.display.update()
    pygame.quit()


pygame_thread = Thread(target=pygame_loop, daemon=True)
pygame_thread.start()
root.mainloop()
