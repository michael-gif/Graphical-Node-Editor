import pygame
import node_api as na

pygame.init()

screen = pygame.display.set_mode((800, 800))
na.init(screen)
clock = pygame.time.Clock()

na.create_node(na.Node("Image Texture")
               .set_xy((100, 100))
               .set_bg((255, 0, 0))
               .add_input("input 1")
               .add_input("input 2")
               .add_output("output 1")
               .add_output("output 2")
               )
na.create_node(na.Node("Dilate/Erode")
               .set_xy((100, 100))
               .set_bg((0, 255, 0))
               .add_input("input 1")
               .add_input("input 2")
               .add_output("output 1")
               .add_output("output 2")
               )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    mouse = pygame.mouse.get_pressed()
    na.update(mouse)
    na.render_all()
    pygame.display.update()

pygame.quit()
