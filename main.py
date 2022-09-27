import os
import sys
import pygame
import string
import json

import tkinter as tk
import node_api as na

from sys import exit
from threading import Thread
from tkinter.filedialog import asksaveasfilename, askopenfilename

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

icon_file = 'icon.ico'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Editor")
        self.iconbitmap(default=os.path.join(application_path, icon_file))
        self.state("zoomed")
        self.protocol("WM_DELETE_WINDOW", self.confirm_quit)
        toolbar = tk.Menu(self)
        toolbar.add_command(label="Exit", command=self.confirm_quit)
        toolbar.add_command(label="Edit Node", command=self.edit_node)
        toolbar.add_command(label="New Node", command=self.create_new_node)
        toolbar.add_command(label="Import", command=self.import_file)
        toolbar.add_command(label="Export", command=self.export)
        self.config(menu=toolbar)

        # embed pygame window
        pygame_embed = tk.Frame(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        pygame_embed.pack()
        os.environ['SDL_WINDOWID'] = str(pygame_embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.update_idletasks()

        self.export_window = None
        self.export_settings_window = None
        self.import_window_open = False
        self.edit_node_window = None
        self.new_node_window = None

        self.save_path = ""
        self.selected_input_value = None
        self.selected_output_value = None
        self.inputs_listbox = None
        self.outputs_listbox = None
        self.selected_input_entry = None
        self.selected_output_entry = None
        self.name_entry = None
        self.description_entry = None
        self.export_options = {
            'id': ('id', True),
            'name': ('name', True),
            'description': ('description', True),
            'xy': ('xy', True),
            'inputs': ('inputs', True),
            'outputs': ('outputs', True),
            'connections': ('connections', True)
        }

        self.bind('<Control-n>', self.open_new_node_window)
        self.bind('<Control-o>', self.open_import_window)
        self.bind('<Control-s>', self.open_export_window)

    def open_new_node_window(self, event):
        self.create_new_node()

    def open_import_window(self, event):
        self.import_file()

    def open_export_window(self, event):
        self.export()

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
        button = tk.Button(quit_window, text="Quit", command=exit)
        label.pack()
        button.pack()

    def create_new_node(self):
        if self.new_node_window:
            self.new_node_window.focus_set()
            self.new_node_window.lift()
            return

        def destruct():
            self.focus_set()
            self.new_node_window.destroy()
            self.new_node_window = None

        def compile_node():
            new_node = na.Node(name_entry.get()).set_description(description_entry.get())
            for inpt in inputs_listbox.get(1, tk.END):
                if str(inpt) == '<empty>':
                    inpt = ''
                new_node.add_input(str(inpt))
            for otpt in outputs_listbox.get(1, tk.END):
                if str(otpt) == '<empty>':
                    otpt = ''
                new_node.add_output(str(otpt))
            na.create_node(new_node)
            self.new_node_window.lift()

        def input_edit(event):
            value = selected_input_value.get()
            if event.char in string.printable:
                if inputs_listbox.curselection() and int(inputs_listbox.curselection()[0]) != 0:
                    selected_item_index = int(inputs_listbox.curselection()[0])
                    inputs_listbox.focus_set()
                    inputs_listbox.delete(selected_item_index, selected_item_index)
                    inputs_listbox.insert(selected_item_index, value)
                    selected_input_entry.focus_set()
                    inputs_listbox.select_set(selected_item_index)

        def output_edit(event):
            value = selected_output_value.get()
            if event.char in string.printable:
                if outputs_listbox.curselection() and int(outputs_listbox.curselection()[0]) != 0:
                    selected_item_index = int(outputs_listbox.curselection()[0])
                    outputs_listbox.focus_set()
                    outputs_listbox.delete(selected_item_index, selected_item_index)
                    outputs_listbox.insert(selected_item_index, value)
                    selected_output_entry.focus_set()
                    outputs_listbox.select_set(selected_item_index)

        def input_select(event):
            w = event.widget
            if w.curselection():
                selected_input_entry.delete(0, tk.END)
                value = w.get(int(w.curselection()[0]))
                if value == '<empty>':
                    value = ''
                selected_input_entry.insert(0, value)

        def output_select(event):
            w = event.widget
            if w.curselection():
                selected_output_entry.delete(0, tk.END)
                value = w.get(int(w.curselection()[0]))
                if value == '<empty>':
                    value = ''
                selected_output_entry.insert(0, value)

        def add_input():
            value = selected_input_value.get()
            if not value:
                value = '<empty>'
            inputs_listbox.insert(tk.END, value)
            selected_input_entry.delete(0, tk.END)

        def add_output():
            value = selected_input_value.get()
            if not value:
                value = '<empty>'
            outputs_listbox.insert(tk.END, value)
            selected_output_entry.delete(0, tk.END)

        def remove_inputs():
            selection = inputs_listbox.curselection()
            if selection and selection[0] != 0:
                inputs_listbox.delete(selection[0], selection[-1])
                selected_input_entry.delete(0, tk.END)
                inputs_listbox.select_set(selection[0])

        def remove_outputs():
            selection = outputs_listbox.curselection()
            if selection and selection[0] != 0:
                outputs_listbox.delete(selection[0], selection[-1])
                selected_output_entry.delete(0, tk.END)
                outputs_listbox.select_set(selection[0])

        self.new_node_window = tk.Toplevel(self)
        self.new_node_window.title("Create new node")
        self.new_node_window.protocol("WM_DELETE_WINDOW", destruct)
        w, h = 370, 370
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.new_node_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        content = tk.Frame(self.new_node_window, relief='sunken')
        content.place(x=10, y=10, width=350, height=350)

        name_label = tk.Label(content, text="Display Name", anchor='w')
        name_label.place(x=0, y=0, height=30)
        name_entry = tk.Entry(content)
        name_entry.place(x=125, y=0, width=225, height=25)

        description_label = tk.Label(content, text="Description", anchor='w')
        description_label.place(x=0, y=30, height=30)
        description_entry = tk.Entry(content)
        description_entry.place(x=125, y=30, width=225, height=25)

        selected_input_value = tk.StringVar()
        selected_output_value = tk.StringVar()

        inputs_label = tk.Label(content, text="Inputs")
        inputs_label.place(x=0, y=75, width=170, height=25)
        inputs_listbox = tk.Listbox(content)
        inputs_listbox.bind('<<ListboxSelect>>', input_select)
        inputs_listbox.place(x=0, y=100, width=170, height=165)
        selected_input_entry = tk.Entry(content, textvariable=selected_input_value)
        selected_input_entry.place(x=0, y=270, width=120, height=25)
        selected_input_entry.bind("<KeyRelease>", input_edit)
        add_input_button = tk.Button(content, text="+", command=add_input)
        add_input_button.place(x=120, y=270, width=25, height=25)
        remove_input_button = tk.Button(content, text="-", command=remove_inputs)
        remove_input_button.place(x=145, y=270, width=25, height=25)

        outputs_label = tk.Label(content, text="Outputs")
        outputs_label.place(x=180, y=75, width=170, height=25)
        outputs_listbox = tk.Listbox(content)
        outputs_listbox.bind('<<ListboxSelect>>', output_select)
        outputs_listbox.place(x=180, y=100, width=170, height=165)
        selected_output_entry = tk.Entry(content, textvariable=selected_output_value)
        selected_output_entry.place(x=180, y=270, width=120, height=25)
        selected_output_entry.bind("<KeyRelease>", output_edit)
        add_output_button = tk.Button(content, text="+", command=add_output)
        add_output_button.place(x=300, y=270, width=25, height=25)
        remove_output_button = tk.Button(content, text="-", command=remove_outputs)
        remove_output_button.place(x=325, y=270, width=25, height=25)

        create_node_button = tk.Button(content, text="Create Node", command=compile_node)
        create_node_button.place(x=0, y=310, width=350, height=40)

        inputs_listbox.insert(0, '')
        outputs_listbox.insert(0, '')

    def edit_node(self):
        if self.edit_node_window:
            self.edit_node_window.focus_set()
            self.edit_node_window.lift()
            return

        def destruct():
            self.focus_set()
            self.edit_node_window.destroy()
            self.edit_node_window = None

        def save_node():
            inpts = inputs_listbox.get(1, tk.END)
            active = na.ACTIVE_NODE
            active.display_name = name_entry.get()
            active.description = name_entry.get()
            for i in range(len(inpts)):
                if i < len(active.inputs):
                    active.inputs[i].name = inpts[i]
                else:
                    active.add_input(inpts[i])
            if len(inpts) < len(active.inputs):
                active.inputs = active.inputs[:len(inpts)]
            otpts = outputs_listbox.get(1, tk.END)
            for i in range(len(otpts)):
                if i < len(active.outputs):
                    active.outputs[i].name = otpts[i]
                else:
                    active.add_output(otpts[i])
            if len(otpts) < len(active.outputs):
                active.outputs = active.outputs[:len(otpts)]
            self.edit_node_window.lift()

        def input_edit(event):
            value = selected_input_value.get()
            if event.char in string.printable:
                if inputs_listbox.curselection() and int(inputs_listbox.curselection()[0]) != 0:
                    selected_item_index = int(inputs_listbox.curselection()[0])
                    inputs_listbox.focus_set()
                    inputs_listbox.delete(selected_item_index, selected_item_index)
                    inputs_listbox.insert(selected_item_index, value)
                    selected_input_entry.focus_set()
                    inputs_listbox.select_set(selected_item_index)

        def output_edit(event):
            value = selected_output_value.get()
            if event.char in string.printable:
                if outputs_listbox.curselection() and int(outputs_listbox.curselection()[0]) != 0:
                    selected_item_index = int(outputs_listbox.curselection()[0])
                    outputs_listbox.focus_set()
                    outputs_listbox.delete(selected_item_index, selected_item_index)
                    outputs_listbox.insert(selected_item_index, value)
                    selected_output_entry.focus_set()
                    outputs_listbox.select_set(selected_item_index)

        def input_select(event):
            w = event.widget
            if w.curselection():
                selected_input_entry.delete(0, tk.END)
                value = w.get(int(w.curselection()[0]))
                if value == '<empty>':
                    value = ''
                selected_input_entry.insert(0, value)

        def output_select(event):
            w = event.widget
            if w.curselection():
                selected_output_entry.delete(0, tk.END)
                value = w.get(int(w.curselection()[0]))
                if value == '<empty>':
                    value = ''
                selected_output_entry.insert(0, value)

        def add_input():
            value = selected_input_value.get()
            if not value:
                value = '<empty>'
            inputs_listbox.insert(tk.END, value)
            selected_input_entry.delete(0, tk.END)

        def add_output():
            value = selected_input_value.get()
            if not value:
                value = '<empty>'
            outputs_listbox.insert(tk.END, value)
            selected_output_entry.delete(0, tk.END)

        def remove_inputs():
            selection = inputs_listbox.curselection()
            if selection and selection[0] != 0:
                inputs_listbox.delete(selection[0], selection[-1])
                selected_input_entry.delete(0, tk.END)
                inputs_listbox.select_set(selection[0])

        def remove_outputs():
            selection = outputs_listbox.curselection()
            if selection and selection[0] != 0:
                outputs_listbox.delete(selection[0], selection[-1])
                selected_output_entry.delete(0, tk.END)
                outputs_listbox.select_set(selection[0])

        self.edit_node_window = tk.Toplevel(self)
        self.edit_node_window.title("Create new node")
        self.edit_node_window.protocol("WM_DELETE_WINDOW", destruct)
        w, h = 370, 370
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.edit_node_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        content = tk.Frame(self.edit_node_window, relief='sunken')
        content.place(x=10, y=10, width=350, height=350)

        name_label = tk.Label(content, text="Display Name", anchor='w')
        name_label.place(x=0, y=0, height=30)
        name_entry = tk.Entry(content)
        name_entry.place(x=125, y=0, width=225, height=25)

        description_label = tk.Label(content, text="Description", anchor='w')
        description_label.place(x=0, y=30, height=30)
        description_entry = tk.Entry(content)
        description_entry.place(x=125, y=30, width=225, height=25)

        selected_input_value = tk.StringVar()
        selected_output_value = tk.StringVar()

        inputs_label = tk.Label(content, text="Inputs")
        inputs_label.place(x=0, y=75, width=170, height=25)
        inputs_listbox = tk.Listbox(content)
        inputs_listbox.bind('<<ListboxSelect>>', input_select)
        inputs_listbox.place(x=0, y=100, width=170, height=165)
        selected_input_entry = tk.Entry(content, textvariable=selected_input_value)
        selected_input_entry.place(x=0, y=270, width=120, height=25)
        selected_input_entry.bind("<KeyRelease>", input_edit)
        add_input_button = tk.Button(content, text="+", command=add_input)
        add_input_button.place(x=120, y=270, width=25, height=25)
        remove_input_button = tk.Button(content, text="-", command=remove_inputs)
        remove_input_button.place(x=145, y=270, width=25, height=25)

        outputs_label = tk.Label(content, text="Outputs")
        outputs_label.place(x=180, y=75, width=170, height=25)
        outputs_listbox = tk.Listbox(content)
        outputs_listbox.bind('<<ListboxSelect>>', output_select)
        outputs_listbox.place(x=180, y=100, width=170, height=165)
        selected_output_entry = tk.Entry(content, textvariable=selected_output_value)
        selected_output_entry.place(x=180, y=270, width=120, height=25)
        selected_output_entry.bind("<KeyRelease>", output_edit)
        add_output_button = tk.Button(content, text="+", command=add_output)
        add_output_button.place(x=300, y=270, width=25, height=25)
        remove_output_button = tk.Button(content, text="-", command=remove_outputs)
        remove_output_button.place(x=325, y=270, width=25, height=25)

        create_node_button = tk.Button(content, text="Save Node", command=save_node)
        create_node_button.place(x=0, y=310, width=350, height=40)

        inputs_listbox.insert(0, '')
        outputs_listbox.insert(0, '')

        if not na.ACTIVE_NODE:
            return
        name_entry.insert(0, na.ACTIVE_NODE.display_name)
        description_entry.insert(0, na.ACTIVE_NODE.description)
        for inpt in na.ACTIVE_NODE.inputs:
            inputs_listbox.insert(tk.END, inpt.name)
        for otpt in na.ACTIVE_NODE.outputs:
            outputs_listbox.insert(tk.END, otpt.name)

    def import_file(self):
        if self.import_window_open:
            self.focus_set()
            return
        self.import_window_open = True
        load_path = askopenfilename(title='Open a file')
        if load_path == '':
            self.import_window_open = False
            self.focus_set()
            return
        with open(load_path) as f:
            raw_json = json.load(f)
        na.NODE_LIST = []
        na.CONNECTION_LIST = []
        for node in raw_json['nodes']:
            tmp_node = na.Node(node['name']).set_xy(node['xy']).set_description(node['description']).set_id(node['id'])
            for inpt in node['inputs']:
                tmp_node.add_input(inpt['name'])
            for otpt in node['outputs']:
                tmp_node.add_output(otpt['name'])
            na.create_node(tmp_node)
        for conn in raw_json['connections']:
            start_node_id = int(conn['start_node_id'])
            end_node_id = int(conn['end_node_id'])
            start_connector_id = int(conn['start_connector_id'])
            end_connector_id = int(conn['end_connector_id'])
            start_connector = None
            end_connector = None
            for node in na.NODE_LIST:
                if node.id == start_node_id:
                    start_connector = node.outputs[start_connector_id]
                if node.id == end_node_id:
                    end_connector = node.inputs[end_connector_id]
            na.CONNECTION_LIST.append((start_node_id, end_node_id, start_connector, end_connector))
        self.import_window_open = False

    def export_settings(self):
        if self.export_settings_window:
            self.export_settings_window.focus_set()
            self.export_settings_window.lift()
            return
        temp_options = {option[0]: None for option in self.export_options.items()}

        def close_export_settings():
            for key, value in temp_options.items():
                if value:
                    self.export_options[key] = (value.get(), True)
                else:
                    self.export_options[key] = (self.export_options[key][0], False)
            self.export_settings_window.destroy()
            self.export_settings_window = None

        def update_export_options(key: str, var: tk.StringVar):
            if temp_options[key]:
                temp_options[key] = None
            else:
                temp_options[key] = var

        self.export_settings_window = tk.Toplevel(self)
        self.export_settings_window.title("Export settings")
        self.export_settings_window.protocol("WM_DELETE_WINDOW", close_export_settings)
        w, h = 270, 225
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.export_settings_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        content = tk.Frame(self.export_settings_window, relief='sunken')
        content.place(x=10, y=10, width=250, height=215)

        attribute_label = tk.Label(content, text='Attributes')
        attribute_label.place(x=0, y=0, width=125)
        name_in_file_label = tk.Label(content, text='Name in file')
        name_in_file_label.place(x=125, y=0, width=125)

        node_id_var = tk.StringVar(value=self.export_options['id'][0])
        node_id_check = tk.Checkbutton(content, text='ID',
                                       command=lambda: update_export_options('id', node_id_var))
        node_id_check.place(x=0, y=25)
        if self.export_options['id'][1]:
            temp_options['id'] = node_id_var
            node_id_check.select()
        node_id_entry = tk.Entry(content, textvariable=node_id_var)
        node_id_entry.place(x=125, y=25, width=125, height=20)

        display_name_var = tk.StringVar(value=self.export_options['name'][0])
        display_name_check = tk.Checkbutton(content, text='Display Name',
                                            command=lambda: update_export_options('name', display_name_var))
        display_name_check.place(x=0, y=50)
        if self.export_options['name'][1]:
            temp_options['name'] = display_name_var
            display_name_check.select()
        display_name_entry = tk.Entry(content, textvariable=display_name_var)
        display_name_entry.place(x=125, y=50, width=125, height=20)

        node_description_var = tk.StringVar(value=self.export_options['description'][0])
        node_description_check = tk.Checkbutton(content, text='Description',
                                                command=lambda: update_export_options('description',
                                                                                      node_description_var))
        node_description_check.place(x=0, y=75)
        if self.export_options['description'][1]:
            temp_options['description'] = node_description_var
            node_description_check.select()
        node_description_entry = tk.Entry(content, textvariable=node_description_var)
        node_description_entry.place(x=125, y=75, width=125, height=20)

        node_position_var = tk.StringVar(value=self.export_options['xy'][0])
        node_position_check = tk.Checkbutton(content, text='XY',
                                             command=lambda: update_export_options('xy', node_position_var))
        node_position_check.place(x=0, y=100)
        if self.export_options['xy'][1]:
            temp_options['xy'] = node_position_var
            node_position_check.select()
        node_position_entry = tk.Entry(content, textvariable=node_position_var)
        node_position_entry.place(x=125, y=100, width=125, height=20)

        node_inputs_var = tk.StringVar(value=self.export_options['inputs'][0])
        node_inputs_check = tk.Checkbutton(content, text='Inputs',
                                           command=lambda: update_export_options('inputs', node_inputs_var))
        node_inputs_check.place(x=0, y=125)
        if self.export_options['inputs'][1]:
            temp_options['inputs'] = node_inputs_var
            node_inputs_check.select()
        node_inputs_entry = tk.Entry(content, textvariable=node_inputs_var)
        node_inputs_entry.place(x=125, y=125, width=125, height=20)

        node_outputs_var = tk.StringVar(value=self.export_options['outputs'][0])
        node_outputs_check = tk.Checkbutton(content, text='Outputs',
                                            command=lambda: update_export_options('outputs', node_outputs_var))
        node_outputs_check.place(x=0, y=150)
        if self.export_options['outputs'][1]:
            temp_options['outputs'] = node_outputs_var
            node_outputs_check.select()
        node_outputs_entry = tk.Entry(content, textvariable=node_outputs_var)
        node_outputs_entry.place(x=125, y=150, width=125, height=20)

        connections_var = tk.StringVar(value=self.export_options['connections'][0])
        connections_check = tk.Checkbutton(content, text='Connections',
                                           command=lambda: update_export_options('connections', connections_var))
        connections_check.place(x=0, y=175)
        if self.export_options['connections'][1]:
            temp_options['connections'] = connections_var
            connections_check.select()
        connections_entry = tk.Entry(content, textvariable=connections_var)
        connections_entry.place(x=125, y=175, width=125, height=20)

    def export_to_file(self, file_type: str):
        with open(self.save_path, 'w') as f:
            if file_type == 'json':
                output = {}
                output_nodes = []
                for node in na.NODE_LIST:
                    tmp = {
                        "id": node.id,
                        "name": node.display_name,
                        "description": node.description,
                        "xy": node.xy,
                        "inputs": [
                            {"id": inpt.id, "name": inpt.name} for inpt in node.inputs
                        ],
                        "outputs": [
                            {"id": otpt.id, "name": otpt.name} for otpt in node.outputs
                        ]
                    }
                    to_append = {}
                    for key, value in self.export_options.items():
                        if key not in tmp:
                            continue
                        if value[1]:
                            to_append[value[0]] = tmp[key]
                    output_nodes.append(to_append)
                output['nodes'] = output_nodes

                if 'connections' not in [opt[0] for opt in self.export_options]:
                    f.write(json.dumps(output, indent=4))
                    return

                output_connections = []
                for conn in na.CONNECTION_LIST:
                    output_connections.append({
                        "start_node_id": conn[0],
                        "end_node_id": conn[1],
                        "start_connector_id": conn[2].id,
                        "end_connector_id": conn[3].id
                    })
                output['connections'] = output_connections
                f.write(json.dumps(output, indent=4))

    def export(self):
        if self.export_window:
            self.export_window.focus_set()
            self.export_window.lift()
            return

        def close_export_window():
            self.focus_set()
            self.export_window.destroy()
            self.export_window = None

        def browse():
            self.save_path = asksaveasfilename(initialfile=f"untitled.{selected_format.get()}",
                                               defaultextension=f'.{selected_format.get()}',
                                               filetypes=[
                                                   (f'{selected_format.get().upper()}', f'.{selected_format.get()}')])
            self.export_window.lift()
            destination_entry.insert(0, self.save_path)

        def destruct():
            self.export_to_file(selected_format.get())
            close_export_window()

        self.export_window = tk.Toplevel(self)
        self.export_window.title("Export")
        self.export_window.protocol("WM_DELETE_WINDOW", close_export_window)
        w, h = 270, 225
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.export_window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        selected_format = tk.StringVar(value='json')

        content = tk.Frame(self.export_window, relief='sunken')
        content.place(x=10, y=10, width=250, height=215)
        line_break = tk.Label(content, text="______________________________________________________")
        line_break.place(x=0, y=-5, width=250)
        destination_label = tk.Label(content, text='Destination  ')
        destination_label.place(x=0, y=0, height=25)
        destination_entry = tk.Entry(content)
        destination_entry.place(x=0, y=30, width=215, height=25)
        browse_button = tk.Button(content, text='...', command=browse)
        browse_button.place(x=225, y=30, width=25, height=25)
        line_break_2 = tk.Label(content, text="______________________________________________________")
        line_break_2.place(x=0, y=55, width=250)
        format_label = tk.Label(content, text='Export format  ''')
        format_label.place(x=0, y=60)
        json_type = tk.Radiobutton(content, text='JSON', value='json', variable=selected_format)
        json_type.place(x=0, y=80)
        ini_type = tk.Radiobutton(content, text='INI', value='ini', variable=selected_format)
        ini_type.place(x=0, y=105)
        settings_button = tk.Button(content, text='Export settings', command=self.export_settings)
        settings_button.place(x=0, y=135, width=250, height=30)
        export_button = tk.Button(content, text='Export', command=destruct)
        export_button.place(x=0, y=175, width=250, height=30)


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
