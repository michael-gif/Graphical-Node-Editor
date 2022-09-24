import pygame
from pygame import gfxdraw


class NodeConnector:
    INPUT = 1
    OUTPUT = 2

    def __init__(self, name: str, color: tuple, text_color: tuple, type: int):
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
        pygame.draw.circle(PYGAME_SCREEN, self.color, self.pos, 5)
        if self.type == NodeConnector.INPUT:
            PYGAME_SCREEN.blit(node_connection_name_font.render(self.get_max_name(), True, self.text_color),
                               (self.pos[0] + 10, self.pos[1] - 10))
        else:
            output_length = node_connection_name_font.size(self.get_max_name())[0]
            PYGAME_SCREEN.blit(node_connection_name_font.render(self.get_max_name(), True, self.text_color),
                               (self.pos[0] - output_length - 10, self.pos[1] - 10))

    def render_hitbox(self):
        pygame.draw.rect(PYGAME_SCREEN, (255, 0, 0), self.get_hitbox(), 1)

    def get_hitbox(self):
        return pygame.Rect(self.pos[0] - 5, self.pos[1] - 5, 10, 10)


class Node:
    def __init__(self, display_name: str):
        self.id = len(NODE_LIST)
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
        self.inputs = []
        self.outputs = []

    def set_xy(self, xy: tuple):
        self.xy = xy
        self.rect.x, self.rect.y = xy
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

    def set_desciption(self, description: str):
        self.description = description
        return self

    def update_height(self):
        if len(self.inputs) > len(self.outputs):
            self.rect.height = self.header_height + (50 * len(self.inputs))
        else:
            self.rect.height = self.header_height + (50 * len(self.outputs))

    def add_input(self, name: str, color: tuple = (159, 159, 159)):
        self.inputs.append(NodeConnector(name, color, self.fg_color, NodeConnector.INPUT))
        self.update_height()
        return self

    def remove_input(self, index: int):
        self.update_height()
        self.inputs.pop(index)
        return self

    def add_output(self, name: str, color: tuple = (159, 159, 159)):
        self.outputs.append(NodeConnector(name, color, self.fg_color, NodeConnector.OUTPUT))
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
        NODE_LIST.append(NODE_LIST.pop(NODE_LIST.index(self)))

    def send_to_back(self):
        NODE_LIST.insert(0, NODE_LIST.pop(NODE_LIST.index(self)))

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

    def render(self):
        render_rect = self.rect
        if self.mouse_offset:
            mouse_pos = pygame.mouse.get_pos()
            render_rect.x = mouse_pos[0] - self.mouse_offset[0]
            render_rect.y = mouse_pos[1] - self.mouse_offset[1]

        render_rect.width = node_header_font.size(self.display_name)[0] + 20 + self.description_max_width + 50
        if render_rect.width < 200:
            render_rect.width = 200
        # background rectangle
        pygame.draw.rect(PYGAME_SCREEN, self.bg_color, render_rect, self.line_width, self.border_radius)
        # header rectangle
        pygame.draw.rect(PYGAME_SCREEN, self.header_color,
                         (render_rect.x, render_rect.y, render_rect.width, self.header_height), 0, 0,
                         self.border_radius, self.border_radius, 0, 0)
        # outline rectangle
        pygame.draw.rect(PYGAME_SCREEN, (0, 0, 0), render_rect, 2, self.border_radius)

        # display name
        display_text_surface = node_header_font.render(self.display_name, True, self.fg_color)
        PYGAME_SCREEN.blit(display_text_surface, (
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
            PYGAME_SCREEN.blit(line_text_surface, line_pos)

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


pygame.font.init()
node_header_font = pygame.font.SysFont("Calibri", 20)
node_connection_name_font = pygame.font.SysFont("Calibri", 20)

PYGAME_SCREEN: pygame.Surface = None
NODE_LIST: list = []
SELECTED_NODE: Node = None
SELECTED_CONNECTOR: NodeConnector = None
CONNECTOR_PARENT: Node = None
CONNECTION_LIST: list = []
MOUSE_DOWN: bool = False


def init(screen):
    global PYGAME_SCREEN
    PYGAME_SCREEN = screen


def create_node(node: Node):
    NODE_LIST.append(node)


def generator_bezier_coords(pos1, pos2):
    a = ((pos1[0] + pos2[0]) * 0.5, pos1[1])
    b = ((pos1[0] + pos2[0]) * 0.5, pos2[1])
    return [pos1, a, b, pos2]


def process_hitboxes():
    global SELECTED_NODE, SELECTED_CONNECTOR, CONNECTOR_PARENT
    if SELECTED_NODE:
        return
    potential_nodes = {}
    for i in range(len(NODE_LIST)):
        for connector in NODE_LIST[i].get_io_connectors():
            if connector.get_hitbox().collidepoint(pygame.mouse.get_pos()):
                SELECTED_CONNECTOR = connector
                CONNECTOR_PARENT = NODE_LIST[i]
                return
        if NODE_LIST[i].rect.collidepoint(pygame.mouse.get_pos()):
            potential_nodes[i] = NODE_LIST[i]
    if potential_nodes:
        sorted_nodes = [v for k, v in sorted(potential_nodes.items(), key=lambda item: item[0], reverse=True)]
    else:
        return
    if not SELECTED_NODE:
        SELECTED_NODE = sorted_nodes[0]
        SELECTED_NODE.bring_to_front()


def update(mouse: tuple):
    global SELECTED_NODE, SELECTED_CONNECTOR, MOUSE_DOWN
    if mouse[0]:
        if not MOUSE_DOWN:
            MOUSE_DOWN = True
            process_hitboxes()
            if SELECTED_NODE:
                SELECTED_NODE.attach_to_mouse()
    else:
        MOUSE_DOWN = False
        if SELECTED_NODE:
            SELECTED_NODE.detach_from_mouse()
            SELECTED_NODE = None
        if SELECTED_CONNECTOR:
            for node in NODE_LIST:
                connectors = node.inputs if SELECTED_CONNECTOR.type == NodeConnector.OUTPUT else node.outputs
                for conn in connectors:
                    if conn.get_hitbox().collidepoint(pygame.mouse.get_pos()):
                        connection_element = (CONNECTOR_PARENT.id, node.id, SELECTED_CONNECTOR, conn)
                        if connection_element not in CONNECTION_LIST:
                            CONNECTION_LIST.append(connection_element)
        SELECTED_CONNECTOR = None


def render_all():
    for connection in CONNECTION_LIST:
        gfxdraw.bezier(PYGAME_SCREEN, generator_bezier_coords(connection[2].pos, connection[3].pos), 2, (255, 255, 255))
    for node in NODE_LIST:
        node.render()
    if SELECTED_CONNECTOR:
        gfxdraw.bezier(PYGAME_SCREEN, generator_bezier_coords(SELECTED_CONNECTOR.pos, pygame.mouse.get_pos()), 2,
                       (255, 255, 255))
