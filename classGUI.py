import pygame

import pygame_gui
from pygame_gui import *
from pygame_gui.elements import UITextBox
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage

class BasicWindow(UIWindow):
    def __init__(self, position, ui_manager):
        super().__init__(pygame.Rect(position, (800, 600)), ui_manager,
                         window_display_title="Basic Window",
                         object_id='#basic_window')

        self.interior_size = self.get_container().get_size()
        self.image_element = UIImage(pygame.Rect((0, 0), self.interior_size),
                                     pygame.Surface(self.interior_size).convert(),
                                     manager=ui_manager,
                                     container=self,
                                     parent_element=self)

        self.image_colour = pygame.Color("#FF0000")

        self.is_active = False

    def update(self, time_delta):
        super().update(time_delta)

        self.image_element.image.fill(self.image_colour)

    def process_event(self, event: pygame.event.Event) -> bool:
        processed_event = super().process_event(event)

        if not processed_event and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.image_colour = pygame.Color("#FF00FF")
            processed_event = True

        return processed_event

class MedicalFolders(pygame_gui.elements.UIWindow):
    def __init__(self, manager):
        super().__init__(pygame.Rect((600, 50), (640, 480)),
                         manager,
                         window_display_title='Medical Folders',
                         object_id="#medical_folders_window")

        search_bar_top_margin = 2
        search_bar_bottom_margin = 2
        self.search_box = pygame_gui.elements.UITextEntryLine(pygame.Rect((150,
                                                                           search_bar_top_margin),
                                                                          (230, 30)),
                                                              manager=manager,
                                                              container=self,
                                                              parent_element=self)

        self.search_label = pygame_gui.elements.UILabel(pygame.Rect((90,
                                                                     search_bar_top_margin),
                                                                    (56,
                                                                     self.search_box.rect.height)),
                                                        "Search:",
                                                        manager=manager,
                                                        container=self,
                                                        parent_element=self)

        self.home_button = pygame_gui.elements.UIButton(pygame.Rect((5, search_bar_top_margin),
                                                                    (57, 29)),
                                                        'Home',
                                                        manager=manager,
                                                        container=self,
                                                        parent_element=self,
                                                        object_id='#home_button')

        self.remaining_window_size = (self.get_container().get_size()[0],
                                      (self.get_container().get_size()[1] -
                                       (self.search_box.rect.height +
                                        search_bar_top_margin +
                                        search_bar_bottom_margin)))
        
        allDataPacients = getDBPacients()
        print("All Data : ",allDataPacients)
        self.pages = allDataPacients
        index_page = self.pages['1']
        self.page_y_start_pos = (self.search_box.rect.height +
                                 search_bar_top_margin +
                                 search_bar_bottom_margin)
        self.page_display = UITextBox(index_page,
                                      pygame.Rect((0, self.page_y_start_pos),
                                                  self.remaining_window_size),
                                      manager=manager,
                                      container=self,
                                      parent_element=self)

    def process_event(self, event):
        handled = super().process_event(event)

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            self.open_new_page(event.link_target)
            handled = True

        if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_element == self.search_box):
            results = self.search_pages(event.text)
            if results != '':
                self.create_search_results_page(results)
            self.open_new_page('results')
            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#medical_folders_window.#home_button'):
            self.open_new_page('1')
            handled = True

        return handled

    def search_pages(self, search_string: str):
        results = {}
        words = search_string.split()

        for page in self.pages.keys():
            total_occurances_of_search_words = 0
            for word in words:
                word_occurances = self.search_text_for_occurrences_of_word(word, self.pages[page])
                total_occurances_of_search_words += word_occurances
            if total_occurances_of_search_words > 0:
                results[page] = total_occurances_of_search_words

        sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
        return OrderedDict(sorted_results)

    @staticmethod
    def search_text_for_occurrences_of_word(word_to_search_for: str, text_to_search: str) -> int:
        return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word_to_search_for),
                                          text_to_search,
                                          flags=re.IGNORECASE))

    def open_new_page(self, page_link: str):
        self.page_display.kill()
        self.page_display = None
        if page_link in self.pages:
            text = self.pages[page_link]

            self.page_display = UITextBox(text,
                                          pygame.Rect((0,
                                                       self.page_y_start_pos),
                                                      self.remaining_window_size),
                                          manager=self,
                                          container=self,
                                          parent_element=self)

    def create_search_results_page(self, results):
        results_text = '<font size=5>Search pacients results</font>'
        if len(results) == 0:
            results_text += '<br> No pacient found!'
        else:
            results_text += '<br>' + str(len(results)) + ' results found:'
            for result in results.keys():
                results_text += '<br><a href=\"' + result + '\">Index pacient found is : ' + result + '</a>'
        self.pages['results'] = results_text        