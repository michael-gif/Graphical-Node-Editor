import pygame

pygame.font.init()
node_name_font = pygame.font.SysFont("Arial", 20)

PYGAME_SCREEN = None
NODE_LIST = []
SELECTED_NODE = None

class Node:
    def __init__(self, display_name: str, x: int, y: int, width: int, height: int, bg_color: tuple = (0, 0, 0), line_width: int = 0, border_radius: int = 5):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.line_width = line_width
        self.border_radius = border_radius
        self.display_name = display_name
        self.mouse_offset = None

    def attach_to_mouse(self):
        if self.mouse_offset:
            return
        mouse = pygame.mouse.get_pos()
        self.mouse_offset = [mouse[0] - self.rect[0], mouse[1] - self.rect[1]]

    def detach_from_mouse(self):
        if self.mouse_offset:
            mouse_pos = pygame.mouse.get_pos()
            self.rect = pygame.Rect(mouse_pos[0] - self.mouse_offset[0], mouse_pos[1] - self.mouse_offset[1], self.rect[2], self.rect[3])
            self.mouse_offset = None
        
    def bring_to_front(self):
        NODE_LIST.append(NODE_LIST.pop(NODE_LIST.index(self)))

    def send_to_back(self):
        NODE_LIST.insert(0, NODE_LIST.pop(NODE_LIST.index(self)))

    def render(self):
        render_rect = self.rect
        if self.mouse_offset:
            mouse_pos = pygame.mouse.get_pos()
            render_rect = pygame.Rect(mouse_pos[0] - self.mouse_offset[0], mouse_pos[1] - self.mouse_offset[1], self.rect[2], self.rect[3])
        pygame.draw.rect(PYGAME_SCREEN, self.bg_color, render_rect, self.line_width, self.border_radius)
        display_text_surface = node_name_font.render(self.display_name, False, (0, 0, 0))
        PYGAME_SCREEN.blit(display_text_surface, (render_rect[0] + 10, render_rect[1] + 10))

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
    if sorted_nodes:
        sorted_nodes = [v for k, v in sorted(potential_nodes.items(), key=lambda item: item[0], reverse=True)]
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
