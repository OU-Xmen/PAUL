import pygame
pygame.init()

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Event Looker")
pygame.event.set_blocked(pygame.TEXTINPUT)
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.event.set_blocked(pygame.ACTIVEEVENT)

event_list = []
break_flag = False
while True:
    for event in pygame.event.get():
        print(pygame.event.event_name(event.type))
        if event.type == pygame.KEYDOWN:
            event_list.append(event.__dict__['key'])
        if event.type == pygame.QUIT:
            break_flag = True
    if break_flag: break

print(event_list)
# up:    1073741906
# down:  1073741905
# left:  1073741904
# right: 1073741903