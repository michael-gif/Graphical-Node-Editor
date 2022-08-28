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

    def render(self):
        pygame.draw.circle(PYGAME_SCREEN, self.color, self.pos, 5)
        if self.type == NodeConnector.INPUT:
            PYGAME_SCREEN.blit(node_connection_name_font.render(self.name, True, self.text_color),
                               (self.pos[0] + 10, self.pos[1] - 10))
        else:
            output_length = node_connection_name_font.size(self.name)[0]
            PYGAME_SCREEN.blit(node_connection_name_font.render(self.name, True, self.text_color),
                               (self.pos[0] - output_length - 10, self.pos[1] - 10))

    def render_hitbox(self):
        pygame.draw.rect(PYGAME_SCREEN, (255, 0, 0), self.get_hitbox(), 1)

    def get_hitbox(self):
        return pygame.Rect(self.pos[0] - 5, self.pos[1] - 5, 10, 10)


class Node:
    def __init__(self, display_name: str):
        self.id = len(NODE_LIST)
        self.rect = pygame.Rect(0, 0, 0, 50)
        self.xy = None
        self.custom_wh = None
        self.bg_color = (128, 128, 128)
        self.fg_color = (228, 228, 228)
        self.line_width = 0
        self.border_radius = 5
        self.display_name = display_name
        self.header_color = (129, 52, 75)
        self.header_height = node_header_font.size(display_name)[1]

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

    def add_input(self, name: str, color: tuple = (159, 159, 159)):
        self.inputs.append(NodeConnector(name, color, self.fg_color, NodeConnector.INPUT))
        if len(self.inputs) > len(self.outputs):
            self.rect.height += 50
        return self

    def remove_input(self, index: int):
        if len(self.inputs) > len(self.outputs):
            self.rect.height -= 50
        self.inputs.pop(index)
        return self

    def add_output(self, name: str, color: tuple = (159, 159, 159)):
        self.outputs.append(NodeConnector(name, color, self.fg_color, NodeConnector.OUTPUT))
        if len(self.outputs) > len(self.inputs):
            self.rect.height += 50
        return self

    def remove_output(self, index: int):
        if len(self.outputs) > len(self.inputs):
            self.rect.height -= 50
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

    def render(self):
        render_rect = self.rect
        if self.mouse_offset:
            mouse_pos = pygame.mouse.get_pos()
            render_rect.x = mouse_pos[0] - self.mouse_offset[0]
            render_rect.y = mouse_pos[1] - self.mouse_offset[1]

        render_rect.width = node_header_font.size(self.display_name)[0] + 20
        if render_rect.width < 200:
            render_rect.width = 200
        # background rectangle
        pygame.draw.rect(PYGAME_SCREEN, self.bg_color, render_rect, self.line_width, self.border_radius)
        # header rectangle
        pygame.draw.rect(PYGAME_SCREEN, self.header_color,
                         (render_rect.x, render_rect.y, render_rect.width, 20 + self.header_height), 0, 0,
                         self.border_radius, self.border_radius, 0, 0)
        # outline rectangle
        pygame.draw.rect(PYGAME_SCREEN, (0, 0, 0), render_rect, 2, self.border_radius)

        # draw node display name
        display_text_surface = node_header_font.render(self.display_name, True, self.fg_color)
        PYGAME_SCREEN.blit(display_text_surface, (render_rect[0] + 10, render_rect[1] + 10))

        # draw all inputs
        for i in range(len(self.inputs)):
            i_connection = self.inputs[i]
            i_connection.pos = (render_rect.x, render_rect.y + 50 + 25 + (50 * i))
            i_connection.render()

        # draw all outputs
        for i in range(len(self.outputs)):
            o_connection = self.outputs[i]
            o_connection.pos = (render_rect.x + render_rect.width, render_rect.y + 50 + 25 + (50 * i))
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
