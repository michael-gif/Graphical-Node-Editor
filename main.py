import os
import pygame
import string
import json

import tkinter as tk
import node_api as na

from threading import Thread
from tkinter.filedialog import asksaveasfilename


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Editor")
        self.state("zoomed")
        self.protocol("WM_DELETE_WINDOW", self.confirm_quit)
        toolbar = tk.Menu(self)
        toolbar.add_command(label="Exit", command=self.confirm_quit)
        toolbar.add_command(label="New Node", command=self.create_new_node)
        toolbar.add_command(label="Export", command=self.export)
        self.config(menu=toolbar)

        # embed pygame window
        pygame_embed = tk.Frame(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        pygame_embed.pack()
        os.environ['SDL_WINDOWID'] = str(pygame_embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.save_path = ""
        self.selected_input_value = None
        self.selected_output_value = None
        self.inputs_listbox = None
        self.outputs_listbox = None
        self.selected_input_entry = None
        self.selected_output_entry = None
        self.name_entry = None
        self.description_entry = None

    def confirm_quit(self):
        quit_window = tk.Toplevel(self)
        quit_window.title("Close Application")
        w, h = 200, 50
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        quit_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        label = tk.Label(quit_window, text="Are you sure you want to quit?")
        button = tk.Button(quit_window, text="Quit", command=quit)
        label.pack()
        button.pack()

    def input_edit(self, event):
        value = self.selected_input_value.get()
        if event.char in string.printable:
            if self.inputs_listbox.curselection() and int(self.inputs_listbox.curselection()[0]) != 0:
                selected_item_index = int(self.inputs_listbox.curselection()[0])
                self.inputs_listbox.focus_set()
                self.inputs_listbox.delete(selected_item_index, selected_item_index)
                self.inputs_listbox.insert(selected_item_index, value)
                self.selected_input_entry.focus_set()
                self.inputs_listbox.select_set(selected_item_index)

    def output_edit(self, event):
        value = self.selected_output_value.get()
        if event.char in string.printable:
            if self.outputs_listbox.curselection() and int(self.outputs_listbox.curselection()[0]) != 0:
                selected_item_index = int(self.outputs_listbox.curselection()[0])
                self.outputs_listbox.focus_set()
                self.outputs_listbox.delete(selected_item_index, selected_item_index)
                self.outputs_listbox.insert(selected_item_index, value)
                self.selected_output_entry.focus_set()
                self.outputs_listbox.select_set(selected_item_index)

    def input_select(self, event):
        w = event.widget
        if w.curselection():
            self.selected_input_entry.delete(0, tk.END)
            value = w.get(int(w.curselection()[0]))
            if value == '<empty>':
                value = ''
            self.selected_input_entry.insert(0, value)

    def output_select(self, event):
        w = event.widget
        if w.curselection():
            self.selected_output_entry.delete(0, tk.END)
            value = w.get(int(w.curselection()[0]))
            if value == '<empty>':
                value = ''
            self.selected_output_entry.insert(0, value)

    def add_input(self):
        value = self.selected_input_value.get()
        if not value:
            value = '<empty>'
        self.inputs_listbox.insert(tk.END, value)
        self.selected_input_entry.delete(0, tk.END)

    def add_output(self):
        value = self.selected_input_value.get()
        if not value:
            value = '<empty>'
        self.outputs_listbox.insert(tk.END, value)
        self.selected_output_entry.delete(0, tk.END)

    def remove_inputs(self):
        selection = self.inputs_listbox.curselection()
        if selection and selection[0] != 0:
            self.inputs_listbox.delete(selection[0], selection[-1])
            self.selected_input_entry.delete(0, tk.END)
            self.inputs_listbox.select_set(selection[0])

    def remove_outputs(self):
        selection = self.outputs_listbox.curselection()
        if selection and selection[0] != 0:
            self.outputs_listbox.delete(selection[0], selection[-1])
            self.selected_output_entry.delete(0, tk.END)
            self.outputs_listbox.select_set(selection[0])

    def build_node(self):
        new_node = na.Node(self.name_entry.get()).set_desciption(self.description_entry.get())
        for inpt in self.inputs_listbox.get(1, tk.END):
            if str(inpt) == '<empty>':
                inpt = ''
            new_node.add_input(str(inpt))
        for otpt in self.outputs_listbox.get(1, tk.END):
            if str(otpt) == '<empty>':
                otpt = ''
            new_node.add_output(str(otpt))
        na.create_node(new_node)

    def create_new_node(self):

        def destruct():
            self.build_node()
            new_node_window.lift()

        new_node_window = tk.Toplevel(self)
        new_node_window.title("Create new node")
        w, h = 370, 370
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        new_node_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        content = tk.Frame(new_node_window, relief='sunken')
        content.place(x=10, y=10, width=350, height=350)

        name_label = tk.Label(content, text="Display Name", anchor='w')
        name_label.place(x=0, y=0, height=30)
        self.name_entry = tk.Entry(content)
        self.name_entry.place(x=125, y=0, width=225, height=25)

        description_label = tk.Label(content, text="Description", anchor='w')
        description_label.place(x=0, y=30, height=30)
        self.description_entry = tk.Entry(content)
        self.description_entry.place(x=125, y=30, width=225, height=25)

        self.selected_input_value = tk.StringVar()
        self.selected_output_value = tk.StringVar()

        inputs_label = tk.Label(content, text="Inputs")
        inputs_label.place(x=0, y=75, width=170, height=25)
        self.inputs_listbox = tk.Listbox(content)
        self.inputs_listbox.bind('<<ListboxSelect>>', self.input_select)
        self.inputs_listbox.place(x=0, y=100, width=170, height=165)
        self.selected_input_entry = tk.Entry(content, textvariable=self.selected_input_value)
        self.selected_input_entry.place(x=0, y=270, width=120, height=25)
        self.selected_input_entry.bind("<KeyRelease>", self.input_edit)
        add_input_button = tk.Button(content, text="+", command=self.add_input)
        add_input_button.place(x=120, y=270, width=25, height=25)
        remove_input_button = tk.Button(content, text="-", command=self.remove_inputs)
        remove_input_button.place(x=145, y=270, width=25, height=25)

        outputs_label = tk.Label(content, text="Outputs")
        outputs_label.place(x=180, y=75, width=170, height=25)
        self.outputs_listbox = tk.Listbox(content)
        self.outputs_listbox.bind('<<ListboxSelect>>', self.output_select)
        self.outputs_listbox.place(x=180, y=100, width=170, height=165)
        self.selected_output_entry = tk.Entry(content, textvariable=self.selected_output_value)
        self.selected_output_entry.place(x=180, y=270, width=120, height=25)
        self.selected_output_entry.bind("<KeyRelease>", self.output_edit)
        add_output_button = tk.Button(content, text="+", command=self.add_output)
        add_output_button.place(x=300, y=270, width=25, height=25)
        remove_output_button = tk.Button(content, text="-", command=self.remove_outputs)
        remove_output_button.place(x=325, y=270, width=25, height=25)

        create_node_button = tk.Button(content, text="Create Node", command=destruct)
        create_node_button.place(x=0, y=310, width=350, height=40)

        self.inputs_listbox.insert(0, '')
        self.outputs_listbox.insert(0, '')

    def export_to_file(self, type: str):
        with open(self.save_path, 'w') as f:
            if type == 'json':
                output = {}
                output_nodes = []
                for node in na.NODE_LIST:
                    output_nodes.append({
                        "id": node.id,
                        "name": node.display_name,
                        "description": node.description,
                        "xy": node.xy,
                    })
                output['nodes'] = output_nodes
                output_connections = []
                for conn in na.CONNECTION_LIST:
                    output_connections.append({
                        "start_node_id": conn[0],
                        "end_node_id": conn[1],
                        "start_connector": {
                            "id": conn[2].id,
                            "name": conn[2].name,
                        },
                        "end_connector": {
                            "id": conn[3].id,
                            "name": conn[3].name
                        }
                    })
                output['connections'] = output_connections
                f.write(json.dumps(output, indent=4))

    def export(self):
        export_window = tk.Toplevel(self)
        export_window.title("Export")
        w, h = 270, 195
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        export_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        selected_format = tk.StringVar(value='json')

        def browse():
            self.save_path = asksaveasfilename(initialfile=f"untitled.{selected_format.get()}",
                                               defaultextension=f'.{selected_format.get()}',
                                               filetypes=[
                                                   (f'{selected_format.get().upper()}', f'.{selected_format.get()}')])
            export_window.lift()
            destination_entry.insert(0, self.save_path)

        def destruct():
            self.export_to_file(selected_format.get())
            export_window.destroy()

        content = tk.Frame(export_window, relief='sunken')
        content.place(x=10, y=10, width=250, height=175)
        line_break = tk.Label(content, text="______________________________________________________")
        line_break.place(x=0, y=-5, width=250)
        destination_label = tk.Label(content, text="Destination  ")
        destination_label.place(x=0, y=0, height=25)
        destination_entry = tk.Entry(content)
        destination_entry.place(x=0, y=30, width=215, height=25)
        browse_button = tk.Button(content, text='...', command=browse)
        browse_button.place(x=225, y=30, width=25, height=25)
        line_break_2 = tk.Label(content, text="______________________________________________________")
        line_break_2.place(x=0, y=55, width=250)
        format_label = tk.Label(content, text="Export format  ")
        format_label.place(x=0, y=60)
        json_type = tk.Radiobutton(content, text='JSON', value='json', variable=selected_format)
        json_type.place(x=0, y=80)
        ini_type = tk.Radiobutton(content, text='INI', value='ini', variable=selected_format)
        ini_type.place(x=0, y=105)
        export_button = tk.Button(content, text='Export', command=destruct)
        export_button.place(x=0, y=135, width=250, height=40)


app = App()

screen = pygame.display.set_mode((app.winfo_screenwidth(), app.winfo_screenheight()))
pygame.display.init()
pygame.display.update()
na.init(screen)


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
app.mainloop()
