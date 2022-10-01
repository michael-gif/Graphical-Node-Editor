import pygame
import ctypes

from pygame import gfxdraw
from events import events


class NodeConnector:
    INPUT = 1
    OUTPUT = 2

    def __init__(self, id, name: str, color: tuple, text_color: tuple, type: int):
        self.id = id
        self.name = name
        self.color = color
        self.text_color = text_color
        self.type = type
        self.pos = None
        self.name_max_width = 75

    def get_max_name(self):
        '''
        Ensures the name will not exceed the name_max_width
        :return: name
        '''
        line = ""
        for char in self.name:
            line_size = node_connection_name_font.size(line)
            char_size = node_connection_name_font.size(char)
            if char_size[0] + line_size[0] <= self.name_max_width:
                line += char
            else:
                line = line[:-3]
                line += '...'
                break
        return line

    def render(self):
        pygame.draw.circle(Enums.PYGAME_SCREEN, self.color, self.pos, 5)
        if self.type == NodeConnector.INPUT:
            Enums.PYGAME_SCREEN.blit(node_connection_name_font.render(self.get_max_name(), True, self.text_color),
                                     (self.pos[0] + 10, self.pos[1] - 10))
        else:
            output_length = node_connection_name_font.size(self.get_max_name())[0]
            Enums.PYGAME_SCREEN.blit(node_connection_name_font.render(self.get_max_name(), True, self.text_color),
                                     (self.pos[0] - output_length - 10, self.pos[1] - 10))

    def render_hitbox(self):
        pygame.draw.rect(Enums.PYGAME_SCREEN, (255, 0, 0), self.get_hitbox(), 1)

    def get_hitbox(self):
        return pygame.Rect(self.pos[0] - 5, self.pos[1] - 5, 10, 10)


class Node:
    def __init__(self, display_name: str):
        self.id = len(Enums.NODE_LIST)
        self.rect = pygame.Rect(0, 0, 0, 50)
        self.xy = (0, 0)
        self.custom_wh = None
        self.bg_color = (52, 52, 52)
        self.fg_color = (228, 228, 228)
        self.line_width = 0
        self.border_radius = 5
        self.display_name = display_name
        self.description = ""
        self.description_max_width = 100
        self.header_color = (129, 52, 75)
        self.header_height = node_header_font.size(display_name)[1] + 30

        self.mouse_offset = None
        self.grid_offset = None
        self.inputs = []
        self.outputs = []

        self.update_grid_offset()

    def set_id(self, id):
        self.id = id
        return self

    def set_xy(self, pos: tuple):
        self.xy = pos
        self.rect.x, self.rect.y = pos[0], pos[1]
        return self

    def set_wh(self, wh: tuple):
        self.custom_wh = wh
        return self

    def set_bg(self, color: tuple):
        self.bg_color = color
        return self

    def set_fg(self, color: tuple):
        self.fg_color = color
        return self

    def set_line_width(self, width: int):
        self.line_width = width
        return self

    def set_border_radius(self, radius: int):
        self.border_radius = radius
        return self

    def set_header_color(self, color: tuple):
        self.header_color = color
        return self

    def set_description(self, description: str):
        self.description = description
        return self

    def update_height(self):
        if len(self.inputs) > len(self.outputs):
            self.rect.height = self.header_height + (50 * len(self.inputs))
        else:
            self.rect.height = self.header_height + (50 * len(self.outputs))

    def add_input(self, name: str, color: tuple = (159, 159, 159)):
        connector = NodeConnector(len(self.inputs), name, color, self.fg_color, NodeConnector.INPUT)
        connector.pos = [self.xy[0], self.xy[1] + self.header_height + 25 + (50 * len(self.inputs))]
        self.inputs.append(connector)
        self.update_height()
        return self

    def remove_input(self, index: int):
        self.update_height()
        self.inputs.pop(index)
        return self

    def add_output(self, name: str, color: tuple = (159, 159, 159)):
        connector = NodeConnector(len(self.outputs), name, color, self.fg_color, NodeConnector.OUTPUT)
        connector.pos = [self.xy[0], self.xy[1] + self.header_height + 25 + (50 * len(self.outputs))]
        self.outputs.append(connector)
        self.update_height()
        return self

    def remove_output(self, index: int):
        self.update_height()
        self.outputs.pop(index)
        return self

    def attach_to_mouse(self):
        if self.mouse_offset:
            return
        mouse = pygame.mouse.get_pos()
        self.mouse_offset = [mouse[0] - self.rect[0], mouse[1] - self.rect[1]]

    def detach_from_mouse(self):
        if self.mouse_offset:
            mouse_pos = pygame.mouse.get_pos()
            self.rect = pygame.Rect(mouse_pos[0] - self.mouse_offset[0], mouse_pos[1] - self.mouse_offset[1],
                                    self.rect[2], self.rect[3])
            self.mouse_offset = None

    def bring_to_front(self):
        Enums.NODE_LIST.append(Enums.NODE_LIST.pop(Enums.NODE_LIST.index(self)))

    def send_to_back(self):
        Enums.NODE_LIST.insert(0, Enums.NODE_LIST.pop(Enums.NODE_LIST.index(self)))

    def get_io_connectors(self):
        return self.inputs + self.outputs

    def split_description(self, description: str):
        '''
        Splits the node description into multiple lines, with each line not exceeding the max width for the description
        :param description:
        :return: lines
        '''
        lines = []
        line = ""
        words = [chunk + " " for chunk in description.split(" ")]
        for word in words:
            line_surface = node_connection_name_font.render(line, True, self.fg_color)
            word_surface = node_connection_name_font.render(word, True, self.fg_color)
            word_width, word_height = word_surface.get_size()
            line_width, line_height = line_surface.get_size()
            if line_width + word_width <= self.description_max_width:
                line += word
            else:
                lines.append(line.strip())
                line = word
        lines.append(line.strip())
        return lines

    def update_grid_offset(self):
        self.grid_offset = [Enums.GRID_ORIGIN[0] - self.rect.x, Enums.GRID_ORIGIN[1] - self.rect.y]

    def render(self):
        render_rect = self.rect
        mouse_pos = pygame.mouse.get_pos()
        render_rect.x = Enums.GRID_ORIGIN[0] - self.grid_offset[0]
        render_rect.y = Enums.GRID_ORIGIN[1] - self.grid_offset[1]
        if self.mouse_offset:
            render_rect.x = mouse_pos[0] - self.mouse_offset[0]
            render_rect.y = mouse_pos[1] - self.mouse_offset[1]
        self.xy = render_rect.x, render_rect.y
        tmp = 0
        if self.inputs:
            tmp += node_connection_name_font.size(self.inputs[0].name)[0] + 10
        if self.description:
            tmp += self.description_max_width + 50
        else:
            tmp += 25
        if self.outputs:
            tmp += node_connection_name_font.size(self.outputs[0].name)[0] + 10
        render_rect.width = node_header_font.size(self.display_name)[0] + 20
        if tmp > render_rect.width:
            render_rect.width = tmp
        if render_rect.width < 100:
            render_rect.width = 100
        # background rectangle
        pygame.draw.rect(Enums.PYGAME_SCREEN, self.bg_color, render_rect, self.line_width)  # , self.border_radius)
        # header rectangle
        pygame.draw.rect(Enums.PYGAME_SCREEN, self.header_color,
                         (render_rect.x, render_rect.y, render_rect.width, self.header_height), 0)  # , 0,
        # self.border_radius, self.border_radius, 0, 0)
        # outline rectangle
        if Enums.ACTIVE_NODE == self:
            pygame.draw.rect(Enums.PYGAME_SCREEN, (217, 152, 22), render_rect, 2)  # , self.border_radius)
        else:
            pygame.draw.rect(Enums.PYGAME_SCREEN, (0, 0, 0), render_rect, 2)  # , self.border_radius)

        # display name
        display_text_surface = node_header_font.render(self.display_name, True, self.fg_color)
        Enums.PYGAME_SCREEN.blit(display_text_surface, (
            render_rect[0] + 10, render_rect[1] + (self.header_height - display_text_surface.get_size()[1]) / 2))

        # description
        lines = self.split_description(self.description)
        description_height = node_connection_name_font.size(lines[0])[1] * len(lines)
        full_height = self.header_height + 25 + description_height + 10
        if full_height > render_rect.height:
            render_rect.height = full_height
        for x in range(len(lines)):
            line_text_surface = node_connection_name_font.render(lines[x], True, self.fg_color)
            line_size = line_text_surface.get_size()
            line_pos = [0, 0]
            if len(self.inputs):
                input_size = node_connection_name_font.size(self.inputs[0].name)
                line_pos[0] = render_rect.x + 10 + input_size[0] + 25
                line_pos[1] = render_rect.y + self.header_height + 25 + (x * input_size[1]) - 10
            else:
                line_pos[0] = render_rect.x + 25
                line_pos[1] = render_rect.y + self.header_height + 25 + (x * line_size[1]) - 10
            Enums.PYGAME_SCREEN.blit(line_text_surface, line_pos)

        # draw all inputs
        for i in range(len(self.inputs)):
            i_connection = self.inputs[i]
            i_connection.pos = (render_rect.x, render_rect.y + self.header_height + 25 + (50 * i))
            i_connection.render()

        # draw all outputs
        for i in range(len(self.outputs)):
            o_connection = self.outputs[i]
            o_connection.pos = (render_rect.x + render_rect.width, render_rect.y + self.header_height + 25 + (50 * i))
            o_connection.render()


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

pygame.font.init()
node_header_font = pygame.font.SysFont("Calibri", 20)
node_connection_name_font = pygame.font.SysFont("Calibri", 20)


class Enums:
    PYGAME_SCREEN: pygame.Surface = None
    NODE_LIST: list = []
    SELECTED_NODE: Node = None
    SELECTED_CONNECTOR: NodeConnector = None
    ACTIVE_NODE: Node = None
    CONNECTOR_PARENT: Node = None
    CONNECTION_LIST: list = []
    MOUSE_DOWN: bool = False
    GRID_ORIGIN: list = [screensize[0] // 2, screensize[1] // 2]
    GRID_OFFSET: list = None


def init(screen):
    Enums.PYGAME_SCREEN = screen


def create_node(node: Node):
    Enums.NODE_LIST.append(node)


def generator_bezier_coords(pos1, pos2):
    a = ((pos1[0] + pos2[0]) * 0.5, pos1[1])
    b = ((pos1[0] + pos2[0]) * 0.5, pos2[1])
    return [pos1, a, b, pos2]


def process_hitboxes():
    if Enums.SELECTED_NODE:
        return
    potential_nodes = {}
    for i in range(len(Enums.NODE_LIST)):
        for connector in Enums.NODE_LIST[i].get_io_connectors():
            if connector.get_hitbox().collidepoint(pygame.mouse.get_pos()):
                Enums.SELECTED_CONNECTOR = connector
                Enums.CONNECTOR_PARENT = Enums.NODE_LIST[i]
                return
        if Enums.NODE_LIST[i].rect.collidepoint(pygame.mouse.get_pos()):
            potential_nodes[i] = Enums.NODE_LIST[i]
    if potential_nodes:
        sorted_nodes = [v for k, v in sorted(potential_nodes.items(), key=lambda item: item[0], reverse=True)]
    else:
        Enums.ACTIVE_NODE = None
        return
    if not Enums.SELECTED_NODE:
        Enums.SELECTED_NODE = sorted_nodes[0]
        Enums.SELECTED_NODE.bring_to_front()


def update(mouse: tuple):
    for i in range(events.qsize()):
        item = events.get()
        print(type(item))
        if item == "CLEAR_SCREEN":
            Enums.NODE_LIST = []
            Enums.CONNECTION_LIST = []
        events.task_done()
    if mouse[0]:
        if not Enums.MOUSE_DOWN:
            Enums.MOUSE_DOWN = True
            process_hitboxes()
            if Enums.SELECTED_NODE:
                Enums.SELECTED_NODE.attach_to_mouse()
                Enums.ACTIVE_NODE = Enums.SELECTED_NODE
    elif mouse[1]:
        mouse_pos = pygame.mouse.get_pos()
        if not Enums.GRID_OFFSET:
            Enums.GRID_OFFSET = mouse_pos[0] - Enums.GRID_ORIGIN[0], mouse_pos[1] - Enums.GRID_ORIGIN[1]
        Enums.GRID_ORIGIN = mouse_pos[0] - Enums.GRID_OFFSET[0], mouse_pos[1] - Enums.GRID_OFFSET[1]
    else:
        Enums.MOUSE_DOWN = False
        Enums.GRID_OFFSET = None
        if Enums.SELECTED_NODE:
            Enums.SELECTED_NODE.detach_from_mouse()
            Enums.SELECTED_NODE = None
        if Enums.SELECTED_CONNECTOR:
            for node in Enums.NODE_LIST:
                connectors = node.inputs if Enums.SELECTED_CONNECTOR.type == NodeConnector.OUTPUT else node.outputs
                for conn in connectors:
                    if conn.get_hitbox().collidepoint(pygame.mouse.get_pos()):
                        connection_element = (Enums.CONNECTOR_PARENT.id, node.id, Enums.SELECTED_CONNECTOR, conn)
                        if connection_element not in Enums.CONNECTION_LIST:
                            Enums.CONNECTION_LIST.append(connection_element)
        Enums.SELECTED_CONNECTOR = None
    for node in Enums.NODE_LIST:
        node.update_grid_offset()


def render_all():
    size = Enums.PYGAME_SCREEN.get_size()
    pygame.draw.line(Enums.PYGAME_SCREEN, (128, 0, 0), (0, Enums.GRID_ORIGIN[1]), (size[0], Enums.GRID_ORIGIN[1]))
    pygame.draw.line(Enums.PYGAME_SCREEN, (0, 128, 0), (Enums.GRID_ORIGIN[0], 0), (Enums.GRID_ORIGIN[0], size[1]))
    for connection in Enums.CONNECTION_LIST:
        gfxdraw.bezier(Enums.PYGAME_SCREEN, generator_bezier_coords(connection[2].pos, connection[3].pos), 5,
                       (255, 255, 255))
    for node in Enums.NODE_LIST:
        node.render()
    if Enums.SELECTED_CONNECTOR:
        gfxdraw.bezier(Enums.PYGAME_SCREEN,
                       generator_bezier_coords(Enums.SELECTED_CONNECTOR.pos, pygame.mouse.get_pos()), 5,
                       (255, 255, 255))


def clear_screen():
    events.append("CLEAR_SCREEN")
