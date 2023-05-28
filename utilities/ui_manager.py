from typing import Any
from typing import List
from typing import Optional

import pygame

from constants import KEY_NAV


def handle_input(game: Any) -> bool:
    key_con = game.control_config.keyboard_controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.check_clicks(event.pos)
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == key_con["FULLSCREEN"]:
                game.toggle_fullscreen()
            if event.key == key_con["MENU"]:
                return False
            if event.key == key_con["UNDO"]:
                game.undo_move()

    keys = pygame.key.get_pressed()
    game.grid_sprite.show_reachable = keys[key_con["REACHABLE"]]

    return True
    # joy_con = game.control_config.joystick_controls
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         return False
    #     if event.type == pygame.KEYDOWN and game.control_config.wait_for_key:
    #         game.control_config.update_key(event.key)
    #         continue
    #     elif event.type == pygame.KEYDOWN and event.key == key_con["MENU"]:
    #         if game.game_started:
    #             if not game.paused:
    #                 game.pause()
    #         elif game.showing_intro:
    #             game.navigate_menu(KEY_NAV.ESC)
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == key_con["FULLSCREEN"] and not game.showing_intro:
    #             game.toggle_fullscreen()
    #         if event.key == pygame.K_t:
    #             game.kill_enemies()
    #         if event.key == pygame.K_h:
    #             game.reset_player_health()
    #         if event.key == pygame.K_k:
    #             game.kill_player()
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         game.ui_manager.check_clicks(event.pos)
    #     elif event.type == pygame.JOYBUTTONDOWN:
    #         if event.button == joy_con["MENU"]:
    #             if game.game_started:
    #                 if not game.paused:
    #                     game.pause()
    #             elif game.showing_intro:
    #                 game.navigate_menu(KEY_NAV.ESC)
    #         if event.button == joy_con["BACK"]:
    #             game.ui_manager.check_clicks([0, 0])

    #     # If game is started and not paused, no need to process menu input
    #     # if (game.game_started or game.showing_intro) and not game.paused:
    #     #     continue

    #     show_cursor = False
    #     # Controls for menus
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_UP:
    #             game.navigate_menu(KEY_NAV.UP)
    #         if event.key == pygame.K_DOWN:
    #             game.navigate_menu(KEY_NAV.DOWN)
    #         if event.key == pygame.K_LEFT:
    #             game.navigate_menu(KEY_NAV.LEFT)
    #         if event.key == pygame.K_RIGHT:
    #             game.navigate_menu(KEY_NAV.RIGHT)
    #         if event.key == pygame.K_RETURN:
    #             game.navigate_menu(KEY_NAV.RETURN)
    #         if event.key == pygame.K_ESCAPE:
    #             game.navigate_menu(KEY_NAV.ESC)
    #     elif event.type == pygame.JOYBUTTONDOWN:
    #         if event.button == joy_con["ACCEPT"]:
    #             game.navigate_menu(KEY_NAV.RETURN)
    #         if event.button in [joy_con["MENU"]]:
    #             game.navigate_menu(KEY_NAV.ESC)
    #     elif event.type == pygame.JOYHATMOTION:
    #         if event.value[0] < 0:
    #             game.navigate_menu(KEY_NAV.LEFT)
    #         if event.value[0] > 0:
    #             game.navigate_menu(KEY_NAV.RIGHT)
    #         if event.value[1] > 0:
    #             game.navigate_menu(KEY_NAV.UP)
    #         if event.value[1] < 0:
    #             game.navigate_menu(KEY_NAV.DOWN)
    #     else:
    #         show_cursor = True
    #     pygame.mouse.set_visible(show_cursor)

    # if hasattr(game, "player"):
    #     game.player.check_keystates()

    # return True


class UIManager(object):

    """
    Pass all buttons on screen and this class will check if they have been clicked
    """

    def __init__(self, game: Any, buttons: Optional[List[Any]] = None):
        self.game = game
        self.buttons = buttons or []
        self.selected_button = self.buttons[0] if len(self.buttons) > 0 else None
        self.previous_selected_button = self.selected_button
        self.cursor_pos = pygame.mouse.get_pos()
        self.previous_cursor_pos = self.cursor_pos

    def add_button(self, button: int) -> None:
        self.buttons.append(button)

    @property
    def index(self) -> int:
        if self.selected_button in self.buttons:
            return self.buttons.index(self.selected_button)
        return 0

    def check_clicks(self, cursor_pos: List[float]) -> None:
        for button in self.buttons:
            if button.rect.collidepoint(cursor_pos):
                button.run_callback()
                return

    def check_mouse_over(self, cursor_pos: List[float]) -> None:
        if cursor_pos == self.previous_cursor_pos:
            return
        self.previous_cursor_pos = cursor_pos
        for button in self.buttons:
            if button.rect.collidepoint(cursor_pos):
                button.set_hover()
                self.selected_button = button
            elif button.is_hover and not button == self.selected_button:
                button.reset_hover()
            elif not button.hold_hover:
                button.reset_hover()

    def change_selected_button(self) -> None:
        for button in self.buttons:
            if not button.alive():
                continue
            if not button.is_arrow and not button.disable_key_nav:
                self.selected_button = button
                break

    def flush_buttons(self) -> None:
        buttons_to_remove = []
        for button in self.buttons:
            if not button.alive():
                if button == self.selected_button:
                    self.selected_button = None
                    self.change_selected_button()
                buttons_to_remove.append(button)
        for button in buttons_to_remove:
            self.buttons.remove(button)
            del button

    def update(self) -> None:
        self.flush_buttons()
        cursor_pos = pygame.mouse.get_pos()
        self.check_mouse_over(cursor_pos)
        if self.selected_button:
            if self.previous_selected_button != self.selected_button:
                self.selected_button.set_hover()
                self.previous_selected_button = self.selected_button
            for button in self.buttons:
                if button != self.selected_button:
                    button.reset_hover()

    def navigate_menu(self, key_press: str) -> None:
        selected_button = self.selected_button
        if not self.buttons:
            return
        if not selected_button:
            self.selected_button = self.buttons[0]
            return

        # Change highlighted button
        if selected_button in self.buttons:
            index = self.buttons.index(selected_button)
        else:
            index = -1

        # Do not differentiate between left and right for now
        if key_press == KEY_NAV.LEFT:
            key_press == KEY_NAV.UP
        if key_press == KEY_NAV.RIGHT:
            key_press == KEY_NAV.DOWN
        # Cycle index
        if key_press in [KEY_NAV.UP, KEY_NAV.LEFT]:
            index -= 1
            if index < 0:
                index = len(self.buttons) - 1
            selected_button = self.buttons[index]
            original_index = index
            counter = 0
            while getattr(selected_button, "disable_key_nav", False):
                selected_button = self.buttons[index]
                index -= 1
                if index < 0:
                    index = len(self.buttons) - 1
                counter += 0
                if counter > len(self.buttons):
                    selected_button = self.buttons[original_index]
                    break
            self.selected_button = selected_button
            if getattr(self.selected_button, "is_arrow", False):
                self.selected_button.run_callback()
                self.change_selected_button()
        elif key_press in [KEY_NAV.DOWN, KEY_NAV.RIGHT]:
            index += 1
            if index == len(self.buttons):
                index = 0
            selected_button = self.buttons[index]
            original_index = index
            counter = 0
            while getattr(selected_button, "disable_key_nav", False):
                selected_button = self.buttons[index]
                index += 1
                if index == len(self.buttons):
                    index = 0
                counter += 0
                if counter > len(self.buttons):
                    selected_button = self.buttons[original_index]
                    break
            self.selected_button = selected_button
            if getattr(self.selected_button, "is_arrow", False):
                self.selected_button.run_callback()
                self.change_selected_button()
        elif key_press == KEY_NAV.RETURN:
            self.selected_button.run_callback()
