import pygame

class Pad:

    def __init__(self, pilas):
        pygame.init()
        self.joystick = None

        for i in range(0, pygame.joystick.get_count()):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()

        self.x = 0
        self.y = 0

        self.x1 = 0
        self.y1 = 0

    def actualizar(self):

        for e in pygame.event.get():
            if e.type == pygame.JOYBUTTONDOWN:
                print "joybotton", e
            elif e.type == pygame.JOYAXISMOTION:
                if e.axis == 0:
                    self.x = e.value
                elif e.axis == 1:
                    self.y = -e.value
                elif e.axis == 2:
                    self.x1 = e.value
                elif e.axis == 3:
                    self.y1 = -e.value
