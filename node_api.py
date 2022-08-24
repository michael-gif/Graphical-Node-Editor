import pygame

pygame.font.init()
node_header_font = pygame.font.SysFont("Consolas", 30)
node_connection_name_font = pygame.font.SysFont("Consolas", 20)

PYGAME_SCREEN = None
NODE_LIST = []
SELECTED_NODE = None


class Node:
    def __init__(self, display_name: str):
        self.rect = pygame.Rect(0, 0, 0, 50)
        self.xy = None
        self.custom_wh = None
        self.bg_color = (128, 128, 128)
        self.fg_color = (228, 228, 228)
        self.line_width = 0
        self.border_radius = 5
        self.display_name = display_name
        self.header_color = (129, 52, 75)

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
        self.inputs.append((name, color))
        if len(self.inputs) > len(self.outputs):
            self.rect.height += 50
        return self

    def remove_input(self, index: int):
        if len(self.inputs) > len(self.outputs):
            self.rect.height -= 50
        self.inputs.pop(index)
        return self

    def add_output(self, name: str, color: tuple = (159, 159, 159)):
        self.outputs.append((name, color))
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

    def render(self):
        render_rect = self.rect
        if self.mouse_offset:
            mouse_pos = pygame.mouse.get_pos()
            render_rect.x = mouse_pos[0] - self.mouse_offset[0]
            render_rect.y = mouse_pos[1] - self.mouse_offset[1]

        render_rect.width = node_header_font.size(self.display_name)[0] + 20
        # background rectangle
        pygame.draw.rect(PYGAME_SCREEN, self.bg_color, render_rect, self.line_width, self.border_radius)
        # header rectangle
        pygame.draw.rect(PYGAME_SCREEN, self.header_color,
                         (render_rect.x, render_rect.y, render_rect.width, 50), 0, 0, self.border_radius,
                         self.border_radius, 0, 0)
        # outline rectangle
        #pygame.draw.rect(PYGAME_SCREEN, (0, 0, 0), render_rect, 2, self.border_radius)
        display_text_surface = node_header_font.render(self.display_name, True, self.fg_color)
        PYGAME_SCREEN.blit(display_text_surface, (render_rect[0] + 10, render_rect[1] + 10))

        for i in range(len(self.inputs)):
            input_connection = self.inputs[i]
            pygame.draw.circle(PYGAME_SCREEN, input_connection[1], (render_rect.x, render_rect.y + 50 + 25 + (50 * i)),
                               5)
            PYGAME_SCREEN.blit(node_connection_name_font.render(input_connection[0], True, self.fg_color),
                               (render_rect.x + 10, render_rect.y + 50 + 15 + (50 * i)))

        for i in range(len(self.outputs)):
            output_connection = self.outputs[i]
            pygame.draw.circle(PYGAME_SCREEN, output_connection[1],
                               (render_rect.x + render_rect.width, render_rect.y + 50 + 25 + (50 * i)), 5)
            output_length = node_connection_name_font.size(output_connection[0])[0]
            PYGAME_SCREEN.blit(node_connection_name_font.render(output_connection[0], True, self.fg_color), (render_rect.x + render_rect.width - output_length - 10, render_rect.y + 50 + 15 + (50 * i)))


def init(screen):
    global PYGAME_SCREEN
    PYGAME_SCREEN = screen


def create_node(node: Node):
    NODE_LIST.append(node)


def find_selected_node():
    global SELECTED_NODE
    if SELECTED_NODE:
        return
    potential_nodes = {}
    for i in range(len(NODE_LIST)):
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
    global SELECTED_NODE
    if mouse[0]:
        find_selected_node()
        if SELECTED_NODE:
            SELECTED_NODE.attach_to_mouse()
    else:
        if SELECTED_NODE:
            SELECTED_NODE.detach_from_mouse()
            SELECTED_NODE = None


def render_all():
    for node in NODE_LIST:
        node.render()
