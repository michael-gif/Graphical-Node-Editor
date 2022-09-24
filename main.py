import os
import pygame
import tkinter as tk
import node_api as na

from threading import Thread

root = tk.Tk()
root.title("Node Editor")
root.state('zoomed')


def confirm_quit():
    quit_window = tk.Toplevel(root)
    quit_window.title("Close Application")
    w, h = 200, 50
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    quit_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    label = tk.Label(quit_window, text="Are you sure you want to quit?")
    button = tk.Button(quit_window, text="Quit", command=quit)
    label.pack()
    button.pack()


root.protocol("WM_DELETE_WINDOW", confirm_quit)
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_command(label="Exit", command=confirm_quit)
root.config(menu=menubar)

# embed pygame window
pygame_embed = tk.Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
pygame_embed.pack()
os.environ['SDL_WINDOWID'] = str(pygame_embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((root.winfo_screenwidth(), root.winfo_screenheight()))
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
