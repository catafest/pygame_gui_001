import pygame

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage

import testGUI

class BasicWindowApp:
    def __init__(self):
        pygame.init()

        self.root_window_surface = pygame.display.set_mode((1280, 720))
        self.background_surface = pygame.Surface((1280, 720)).convert()
        self.background_surface.fill(pygame.Color('#505050'))
        self.ui_manager = UIManager((1280, 720))
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.basic_window = classGUI.BasicWindow((25, 25), self.ui_manager)
        self.medicalFolders = testGUI.Testing(manager=self.ui_manager)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.root_window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.root_window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = BasicWindowApp()
    app.run()
