import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, status):
        super(GameObject, self).__init__()
        # self.surf = pygame.Surface((30, 30))
        if status == 'normal':
            # self.surf.fill((255, 255, 0))
            self.surf = pygame.image.load('./img/normal.png')
        elif status == 'sick':
            # self.surf.fill((204, 0, 0))
            self.surf = pygame.image.load('./img/sick.png')
        elif status == 'dead':
            # self.surf.fill((0, 0, 0))
            self.surf = pygame.image.load('./img/dead.png')
        elif status == 'vaccinated': 
            # self.surf.fill((0, 153, 0))
            self.surf = pygame.image.load('./img/vaccinated.png')
        # self.rect = self.surf.get_rect()
        self.x = x
        self.y = y

    def render(self, screen):  
        screen.blit(self.surf, (self.x, self.y))

