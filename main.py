import pygame, sys
from slider import Slider
from particle import Particle


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 960))
        self.clock = pygame.time.Clock()
        self.mass_slider = Slider(self, 100, self.screen.get_height() - 50, length=300)
        self.orbit_length_slider = Slider(self, self.screen.get_width() - 400, self.screen.get_height() - 50,
                                          length=300, value=0.2)
        self.font = pygame.font.Font(None, 40)
        self.particles = []
        self.creating_new_particle = False
        self.mass_creation_pos = None
        self.paused = False

    def run(self):
        mouse_pressed = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Pause
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    # Reset screen
                    if event.key == pygame.K_r:
                        self.particles = []

            # Get mouse state
            previously_mouse_pressed = mouse_pressed
            mouse_pressed = pygame.mouse.get_pressed()[0]
            mouse_just_clicked = mouse_pressed and not previously_mouse_pressed
            mouse_just_released = previously_mouse_pressed and not mouse_pressed
            mouse_pos = pygame.mouse.get_pos()

            # Set mass of next particle
            new_particle_mass = 10 ** (self.mass_slider.value * 3)
            orbit_length = int(self.orbit_length_slider.value * 1000)

            # Check for slider usage
            not_using_sliders = (not self.mass_slider.rect().collidepoint(mouse_pos)
                                 and not self.mass_slider.grabbed
                                 and not self.orbit_length_slider.rect().collidepoint(mouse_pos)
                                 and not self.orbit_length_slider.grabbed)

            # Create a new particle
            if not_using_sliders:
                if mouse_just_clicked:
                    self.creating_new_particle = True
                    self.mass_creation_pos = pygame.mouse.get_pos()
                if mouse_just_released:
                    new_particle = Particle(self, self.mass_creation_pos, mouse_pos, new_particle_mass)
                    self.particles.append(new_particle)
                    self.creating_new_particle = False

            # Update sliders
            self.mass_slider.update(mouse_just_clicked)
            self.orbit_length_slider.update(mouse_just_clicked)

            if not self.paused:
                for particle in self.particles:
                    # Check for particles out of screen
                    if (particle.pos[0] < -1000 or particle.pos[0] > self.screen.get_width() + 1000
                            or particle.pos[1] < -1000 or particle.pos[1] > self.screen.get_height() + 1000):
                        particle.to_delete = True

                    # Interactions between particles
                    if not particle.to_delete:
                        for other_particle in self.particles:
                            if particle is not other_particle:
                                # Check for collisions
                                if particle.collided_with(other_particle):
                                    mass_ratio = particle.mass / other_particle.mass
                                    if mass_ratio > 8:
                                        other_particle.to_delete = True
                                    elif mass_ratio < 1/8:
                                        particle.to_delete = True
                                    else:
                                        particle.to_delete = True
                                        other_particle.to_delete = True

                                # Calculate gravity force
                                if not other_particle.to_delete:
                                    particle.calculate_gravity_from(other_particle)

                for particle in self.particles[:]:
                    if particle.to_delete:
                        self.particles.remove(particle)

                for particle in self.particles:
                    particle.update(orbit_length)

            self.screen.fill((0, 0, 0))

            for particle in self.particles:
                particle.render()

            if self.creating_new_particle:
                pygame.draw.line(self.screen, "white", self.mass_creation_pos, mouse_pos)

            self.mass_slider.render()
            self.orbit_length_slider.render()

            text = self.font.render(f"Next particle mass: {new_particle_mass:.0f}", False, "white")
            self.screen.blit(text, (100, self.screen.get_height() - 100))
            text = self.font.render(f"Orbit line length: {orbit_length:.0f}", False, "white")
            self.screen.blit(text, (self.screen.get_width() - 400, self.screen.get_height() - 100))
            
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()