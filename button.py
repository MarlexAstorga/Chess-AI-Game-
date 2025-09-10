import pygame
pygame.init()
test_font = pygame.font.SysFont("Arial", 30, False, False)

class Button:
    def __init__(self, x, y, surf):
        #co ordinates on screen
        self.x = x
        self.y = y
        self.surf = surf #surface
        self.text_surf = test_font.render((self.surf), False, (0, 0, 0)) #rendering text, and colour
        self.text_rect = self.text_surf.get_rect(center = (self.x, self.y)) #rectangle on surface, gets position
        
        

    def update(self, screen):
        screen.blit(self.text_surf, self.text_rect) #printing on screen

    def collide(self, event):
        if self.text_rect.collidepoint(event.pos):
            return True #if collides with button returns True
        
    def paraText(self, size, text, x, y, screen):
        #text for screen
        font_size = size
        font = pygame.font.Font(None, font_size)
        font.set_bold(True)
        text_surf = font.render((text), False, (0, 0, 0))
        text_rect = text_surf.get_rect(center = (x, y))
        screen.blit(text_surf, text_rect)


