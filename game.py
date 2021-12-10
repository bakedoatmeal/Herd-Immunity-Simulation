import pygame

from gameObject import GameObject
from virus import Virus
from simulation2 import Simulation

class Game():
    def __init__(self):    
        self.virus = Virus('Covid', 0.05, 0.5)
        self.sim = Simulation(self.virus, 120, 0.04, 5)
        self.all_sprites = pygame.sprite.Group()
        self.draw_population()

    def play(self):
        clock = pygame.time.Clock()
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode([600, 600])
        font = pygame.font.SysFont('helvetica', 20)
        data1 =  f'Population size: {self.sim.pop_size}, Total vaccinated: {self.sim.vaccinated}'
        data2 = f'Total dead: {self.sim.total_dead}, Currently Infected: {self.sim.current_infected}'
        line1 = font.render(data1, True, (255, 255, 255))
        line2 = font.render(data2, True, (255, 255, 255))

        running = True
        while running: 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.sim.time_step()
                    self.sim.infect_newly_infected()
                    self.draw_population()
                    for entity in self.all_sprites: 
                        entity.render(screen)
                    data1 =  f'Population size: {self.sim.pop_size}, Total vaccinated: {self.sim.vaccinated}'
                    data2 = f'Total dead: {self.sim.total_dead}, Currently Infected: {self.sim.current_infected}'
                    line1 = font.render(data1, True, (255, 255, 255))
                    line2 = font.render(data2, True, (255, 255, 255))

            screen.fill((51, 0, 102))
            screen.blit(line1, (0, 550))
            screen.blit(line2, (0, 575))
            for entity in self.all_sprites: 
                entity.render(screen)
            
            pygame.display.flip()    
            clock.tick(60)

    def draw_population(self):
        self.all_sprites.empty()
        x_pos = 0
        y_pos = 0
        for person in self.sim.population:
            if person.is_alive:
                if person.infection is not None:
                    self.all_sprites.add(GameObject(x_pos, y_pos, 'sick'))
                    if x_pos < 500:
                        x_pos += 50
                    else:
                        x_pos = 0 
                        y_pos += 50
                    
                    # draw sick
                elif person.is_vaccinated:
                    self.all_sprites.add(GameObject(x_pos, y_pos, 'vaccinated'))
                    # draw vaccinated person
                    if x_pos < 500:
                        x_pos += 50
                    else:
                        x_pos = 0 
                        y_pos += 50
                    
                else:
                    self.all_sprites.add(GameObject(x_pos, y_pos, 'normal'))
                    # draw normal person
                    if x_pos < 500:
                        x_pos += 50
                    else:
                        x_pos = 0 
                        y_pos += 50
                    
            else:
                self.all_sprites.add(GameObject(x_pos, y_pos, 'dead'))
                # draw dead person
                if x_pos < 500:
                    x_pos += 50
                else:
                    x_pos = 0 
                    y_pos += 50
                

    def run_game(self):
        self.sim.create_population()
        self.draw_population()
        self.play()
        




if __name__ == "__main__":
    game = Game()
    game.run_game()
