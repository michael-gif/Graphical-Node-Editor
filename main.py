import os
import pygame
import tkinter as tk
import node_api as na
import string

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

def create_new_node():
    new_node_window = tk.Toplevel(root)
    new_node_window.title("Create new node")
    w, h = 370, 370
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    new_node_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    content = tk.Frame(new_node_window, relief='sunken')
    content.place(x=10, y=10, width=350, height=350)

    name_label = tk.Label(content, text="Display Name", anchor='w')
    name_label.place(x=0, y=0, height=30)
    name_entry = tk.Entry(content)
    name_entry.place(x=125, y=0, width=225, height=25)

    description_label = tk.Label(content, text="Description", anchor='w')
    description_label.place(x=0, y=30, height=30)
    description_entry = tk.Entry(content)
    description_entry.place(x=125, y=30, width=225, height=25)

    def input_edit(event):
        value = svar.get()
        if event.char in string.printable:
            if inputs_listbox.curselection() and int(inputs_listbox.curselection()[0]) != 0:
                selected_item_index = int(inputs_listbox.curselection()[0])
                inputs_listbox.focus_set()
                inputs_listbox.delete(selected_item_index, selected_item_index)
                inputs_listbox.insert(selected_item_index, value)
                selected_input.focus_set()
                inputs_listbox.select_set(selected_item_index)

    def input_select(event):
        w = event.widget
        if w.curselection():
            selected_input.delete(0, tk.END)
            selected_input.insert(0, w.get(int(w.curselection()[0])))

    def output_select(event):
        w = event.widget
        if w.curselection():
            selected_output.delete(0, tk.END)
            selected_output.insert(0, w.get(int(w.curselection()[0])))

    def add_input():
        inputs_listbox.insert(tk.END, svar.get())
        selected_input.delete(0, tk.END)

    def remove_inputs():
        selection = inputs_listbox.curselection()
        if selection and selection[0] != 0:
            inputs_listbox.delete(selection[0], selection[-1])
            selected_input.delete(0, tk.END)
            inputs_listbox.select_set(selection[0])

    def remove_outputs():
        selection = outputs_listbox.curselection()
        if selection and selection[0] != 0:
            outputs_listbox.delete(selection[0], selection[-1])
            selected_output.delete(0, tk.END)
            outputs_listbox.select_set(selection[0])

    svar = tk.StringVar()
    #svar.trace('w', input_edit)

    inputs_label = tk.Label(content, text="Inputs")
    inputs_label.place(x=0, y=75, width=170, height=25)
    inputs_listbox = tk.Listbox(content)
    inputs_listbox.bind('<<ListboxSelect>>', input_select)
    inputs_listbox.place(x=0, y=100, width=170, height=165)
    selected_input = tk.Entry(content, textvariable=svar)
    selected_input.place(x=0, y=270, width=120, height=25)
    selected_input.bind("<KeyRelease>", input_edit)
    add_input_button = tk.Button(content, text="+", command=add_input)
    add_input_button.place(x=120, y=270, width=25, height=25)
    remove_input_button = tk.Button(content, text="-", command=remove_inputs)
    remove_input_button.place(x=145, y=270, width=25, height=25)

    outputs_label = tk.Label(content, text="Outputs")
    outputs_label.place(x=180, y=75, width=170, height=25)
    outputs_listbox = tk.Listbox(content)
    outputs_listbox.bind('<<ListboxSelect>>', output_select)
    outputs_listbox.place(x=180, y=100, width=170, height=165)
    selected_output = tk.Entry(content)
    selected_output.place(x=180, y=270, width=120, height=25)
    add_output_button = tk.Button(content, text="+")
    add_output_button.place(x=300, y=270, width=25, height=25)
    remove_output_button = tk.Button(content, text="-", command=remove_outputs)
    remove_output_button.place(x=325, y=270, width=25, height=25)

    create_node_button = tk.Button(content, text="Create Node")
    create_node_button.place(x=0, y=310, width=350, height=40)

    inputs_listbox.insert(0, '')
    outputs_listbox.insert(0, '')
    for i in range(10):
        inputs_listbox.insert(tk.END, i)
    for i in range(10):
        outputs_listbox.insert(tk.END, i)


root.protocol("WM_DELETE_WINDOW", confirm_quit)
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=False)
menubar.add_command(label="Exit", command=confirm_quit)
menubar.add_command(label="New Node", command=create_new_node)
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
