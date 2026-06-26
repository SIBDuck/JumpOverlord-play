# Constants are written in CapsLock
from operator import truediv

import pygame
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import winsound
import shutil
import pathlib
import os

FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
TILE_SIZE = 64


coin = 0  # Create coin counter
coins_level = 0  # Coins in a level

Level_path = ""  # Level path

levels = [  # Official levels in the game
    "levels/level 1.json",
    "levels/level 2.json",
    "levels/level 3.json",
    "levels/level 4.json",
    "levels/level 5.json",
    "levels/level 6.json",
    "levels/level 7.json",
    "levels/level 8.json",
    "levels/level 9.json",
    "levels/level 10.json"
]


def load_data():
    global en_flag, custom_levels, custom_levels_dict, is_F1, Debug
    with open("player data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file) # Load the current player configuration
    en_flag = True if data["settings"]["language"] == "en" else False
    is_F1 = True if data["settings"]["F1 mode"] else False
    Debug = True if data["settings"]["debug mode"] else False

    change_lan()

    if not is_F1:
        pygame.display.toggle_fullscreen()

    with open("player data/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) # Load changes

def load_level_txt(LEVEL_PATH):
    global TILE_SIZE, Level_path, levels, coins_level, player_cords
    with open(LEVEL_PATH, "r", encoding='utf-8') as l1:  # Open level file
        level = l1.readlines()  # Load the current level configuration
    level_name = pathlib.Path(LEVEL_PATH).name

    objects = {  # Dictionary of game objects and entities with their coords
        "walls": [],
        "enemies": [],
        "turrets": [],
        "boss": [],
        "platforms": [],
        "j_platforms": [],
        "m_platforms": [],
        "m_j_platforms": [],
        "liquid": [],
        "spikes": [],
        "closed_door": [],
        "money": [],
        "chest": [],
        "FAK": [],  # First aid kit
        "buttons": [],
        "portals": [],
        "start": [],
        "end": [],
        "npc": [],
        "air": [],
        "checkpoint": [],
        "coins": []
    }

    for i, f in enumerate(level):  # Parse the text map and populate game objects with coordinates
        for j, k in enumerate(f):
            if k == "#":
                objects["walls"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "e":
                objects["enemies"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "t":
                objects["turrets"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "b":
                objects["boss"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == ".":
                objects["air"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "p":
                objects["platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "P":
                objects["m_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "=":
                objects["j_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "_":
                objects["m_j_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "~":
                objects["liquid"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "^":
                objects["spikes"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE + 32))
            elif k == "n":
                objects["npc"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "-":
                objects["closed_door"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "*":
                objects["money"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "?":
                objects["chest"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "h":
                objects["FAK"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "!":  # TODO: Implement button functionality
                objects["buttons"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == ">":
                objects["start"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "<":
                objects["end"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "0":
                objects["portals"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "s":
                objects["checkpoint"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "$":
                objects["money"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
            elif k == "@":
                player_cords = [(j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE]
    coins_level = len(objects["money"])
    if player_cords is not None:
        return player_cords, objects
    winsound.MessageBeep(winsound.MB_ICONHAND)
    if en_flag:
        tk.messagebox.showerror("Loading error",
                                f"Failed to load player data. Check the file '{level_name}' for the symbol '@' (player).")
    else:
        tk.messagebox.showerror("Ошибка загрузки",
                                f"не удалось загрузить информацию игрока. Проверьте файл '{level_name}' на наличие символа '@' (игрок).")
    return None, None


def load_level_json(LEVEL_PATH):
    global TILE_SIZE, Level_path, levels, coins_level, player_cords, en_flag
    with open(LEVEL_PATH, "r", encoding="utf-8") as level_js:
        level = json.load(level_js) # Load the current level configuration
    level_name = pathlib.Path(LEVEL_PATH).name
    objects = {  # Dictionary of game objects and entities with their coordinates
        "walls": [],
        "enemies": [],
        "turrets": [],
        "boss": [],
        "platforms": [],
        "j_platforms": [],
        "m_platforms": [],
        "m_j_platforms": [],
        "liquid": [],
        "spikes": [],
        "closed_door": [],
        "money": [],
        "chest": [],
        "FAK": [],  # First aid kit
        "buttons": [],
        "portals": [],
        "start": [],
        "end": [],
        "npc": [],
        "air": [],
        "checkpoint": [],
        "coins": []
    }
    if "map" in level:
        for i, f in enumerate(level["map"]):
            for j, k in enumerate(f):
                if k == "#":
                    objects["walls"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "e":
                    objects["enemies"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "t":
                    objects["turrets"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "b":
                    objects["boss"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == ".":
                    objects["air"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "p":
                    objects["platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "P":
                    objects["m_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "=":
                    objects["j_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "_":
                    objects["m_j_platforms"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "~":
                    objects["liquid"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "^":
                    objects["spikes"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE + 32))
                elif k == "n":
                    objects["npc"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "-":
                    objects["closed_door"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "*":
                    objects["money"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "?":
                    objects["chest"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "h":
                    objects["FAK"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "!":  # TODO: Implement button functionality
                    objects["buttons"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == ">":
                    objects["start"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "<":
                    objects["end"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "0":
                    objects["portals"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "s":
                    objects["checkpoint"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "$":
                    objects["money"].append(((j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                elif k == "@":
                    player_cords = [(j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE]
        coins_level = len(objects["money"])
        if player_cords:
            return player_cords, objects
        winsound.MessageBeep(winsound.MB_ICONHAND)
        if en_flag:
            tk.messagebox.showerror("Loading error",
                                    f"Failed to load player data. Check the file '{level_name}' for the symbol '@' (player).")
        else:
            tk.messagebox.showerror("Ошибка загрузки",
                                    f"не удалось загрузить информацию игрока. Проверьте файл '{level_name}' на наличие символа '@' (игрок).")
        return None, None
    else:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        if en_flag:
            tk.messagebox.showerror("Error",
                                    f"File '{level_name}' does not have a key 'map'. Edit or delete file from the custom level list.")
        else:
            tk.messagebox.showerror("Ошибка",
                                    f"Файл '{level_name}'не имеет ключа 'map'. Измените или удалите файл из списка кастомных уровней.")

        return None, None


def reset_level(level_path):
    global player, level_data, camera, gameplay, pause, death, is_jump, is_go, complete, coin, death_flag, player_cords, Level_path
    Level_path = level_path
    if level_path:

        if pathlib.Path(level_path).suffix == ".json":
            player_cords, level_data = load_level_json(level_path)
        else:
            player_cords, level_data = load_level_txt(level_path)

        # Create camera and player:
        if player_cords and level_data:
            player = Player(player_cords[0], player_cords[1])
            camera = Camera()

            gameplay = True
            pause = False
            death = False
            is_jump = False
            is_go = False
            complete = False
            coin = 0
            if player:
                player.jump_buffer = 0
            death_flag = 0
            return True
        else:

            gameplay = False
            return False
    return False


class Player:
    def __init__(self, x, y):
        # Initialize player attributes and physics parameters
        self.x = x
        self.y = y
        self.width = 32  # hitbox width
        self.height = 56  # hitbox height
        self.speed = 5
        self.direction = "right"  # Current player movement direction
        self.animation_index = 0
        self.animation_timer = 0
        self.HITBOX_OFFSET_X = 7
        self.SPRITE_OFFSET_Y = 5

        self.vy = 0  # Vertical velocity (0 means standing still)
        self.gravity = 1  # Gravity force applied per frame
        self.jump_power = -22  # Initial jump velocity (negative for moving up)
        # Coyote time configuration (allows jumping slightly after leaving a ledge)
        self.coyote_time = 0  # Current coyote time frame counter
        self.coyote_max = 10  # Maximum frames available for a delayed jump
        # Jump buffer configuration (remembers jump input right before landing)
        self.jump_buffer = 0  # Jump buffer frame counter
        self.jump_buffer_max = 10  # Maximum frames to remember early jump input

    def jump(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump_buffer = self.jump_buffer_max  # Trigger jump buffer on input
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.vy < 0:  # if the player is moving upward
                    self.vy *= 0.5  # Reduce vertical velocity

    # Get player's hitbox:
    def get_rect(self):
        return pygame.Rect(self.x - self.HITBOX_OFFSET_X, self.y, self.width, self.height)
        # We subtract "self.HITBOX_OFFSET_X" because of the unknown mistake


    def move(self, keys, level_data):
        global gameplay, death, is_jump, is_go, coin, complete
        old_x = self.x  # Store current X coordinate for collision resolution
        if keys[pygame.K_a]:
            is_go = True
            self.x -= self.speed
            self.direction = "left"

        if keys[pygame.K_d]:
            is_go = True

            self.x += self.speed
            self.direction = "right"

        if keys[pygame.K_a] or keys[pygame.K_d]:
            # Update animation timer and cycle through running frames (0 to 3)
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_index = (
                                               self.animation_index + 1) % 4
                self.animation_timer = 0

        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            is_go = False

        if is_jump:
            is_go = True
            if self.direction == "right":
                self.animation_index = 0
            else:
                self.animation_index = 3
        # Reset to idle animation frame
        if not is_go:
            if self.direction == "right":
                self.animation_index = 1
            else:
                self.animation_index = 2

        player_rect = self.get_rect()
        wall_collision = False
        # Check for collisions with objects
        # Check for horizontal collisions with walls
        for wallx, wally in level_data['walls']:

            wall_rect = pygame.Rect(wallx, wally, TILE_SIZE, TILE_SIZE)  # Create wall hitbox
            if player_rect.colliderect(wall_rect):
                wall_collision = True
                break
        # Check for vertical collisions with platforms
        # TODO: add more types of platforms (passable platforms and their moving versions)
        for plat_x, plat_y in level_data["platforms"] + level_data["m_platforms"] + level_data["j_platforms"] + \
                              level_data["m_j_platforms"]:
            # Create left and right parts of a platform hitbox
            plat_rect_left = pygame.Rect(plat_x - 1, plat_y, 1, TILE_SIZE)
            plat_rect_right = pygame.Rect(plat_x + TILE_SIZE + 1, plat_y, 1, TILE_SIZE)
            if player_rect.colliderect(plat_rect_left) and self.direction == "right":
                self.x = old_x
                break
            elif player_rect.colliderect(plat_rect_right) and self.direction == "left":
                self.x = old_x
                break
        # Check for collisions with spikes
        for s_x, s_y in level_data["spikes"]:
            # Create spike hitbox
            spike_rect = pygame.Rect((s_x, s_y, TILE_SIZE, TILE_SIZE // 2))  # Spikes are smaller

            if player_rect.colliderect(spike_rect):
                death = True
                break

        # Check for collisions with coins
        for c_x, c_y in level_data["money"]:
            coin_rect = pygame.rect.Rect((c_x, c_y, TILE_SIZE // 2, TILE_SIZE // 2))
            if player_rect.colliderect(coin_rect):
                for coin_pos in level_data["money"][:]:  # Use list copy [:] for safe deletion
                    coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], TILE_SIZE, TILE_SIZE)
                    if player_rect.colliderect(coin_rect):
                        level_data["money"].remove(coin_pos)
                        coin += 1
        # Check for collisions with exit level triggers
        for e_x, e_y in level_data["end"]:
            end_rect = pygame.rect.Rect((e_x, e_y, TILE_SIZE, TILE_SIZE))
            if player_rect.colliderect(end_rect):
                complete = True

        if self.y > 2000:  # Prevent the player from falling into the void
            death = True

        if wall_collision:
            self.x = old_x

        old_y = self.y
        self.vy += self.gravity  # Increase speed of fall (the longer the player falls, the faster he falls)
        self.y += self.vy  # Start falling

        self.check_vertical_collision(old_y, level_data)
        on_ground = self.ground_check(level_data)
        if on_ground:
            is_jump = False
            self.coyote_time = self.coyote_max
        else:
            self.coyote_time = max(0, self.coyote_time - 1)  # Decrement coyote time counter
            is_jump = True
            # Tick down jump buffer frame counter
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        # Trigger jump if player is on ground or left ledge recently
        if self.jump_buffer > 0 and (on_ground or self.coyote_time > 0):
            self.vy = self.jump_power
            self.coyote_time = 0
            self.jump_buffer = 0

    def ground_check(self, level_data):
        player_rect = self.get_rect()
        # Create ground detector rectangle
        ground_check_rect = pygame.Rect(player_rect.x,
                                        player_rect.y + player_rect.height,
                                        player_rect.width,
                                        2)

        for plat_x, plat_y in level_data["platforms"] + level_data["j_platforms"] + level_data["m_platforms"] + \
                              level_data["m_j_platforms"]:
            plat_hb = pygame.Rect(plat_x, plat_y, TILE_SIZE, TILE_SIZE)  # Create platform hitbox
            if ground_check_rect.colliderect(plat_hb):
                return True
        return False

    def check_vertical_collision(self, old_y, level_data):
        player_rect = self.get_rect()
        obstacles = (level_data.get("walls", []) +
                     level_data.get("platforms", []) +
                     level_data.get("m_platforms", []))
        for x, y in obstacles:
            block_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)  # Create obstacle hitbox
            if player_rect.colliderect(block_rect):
                self.y = old_y
                self.vy = 0  # Stop falling (encountered an obstacle)
                break

    def draw(self, surface, camera_x, camera_y):  # Draw player function
        screen_x = self.x - camera_x - self.width // 2  # Calculate screen player X coordinate
        screen_y = self.y - camera_y - self.SPRITE_OFFSET_Y  # Calculate screen player Y coordinate

        if self.direction == "right":
            current_frame = player_right[self.animation_index % len(player_right)]
        else:
            current_frame = player_left[self.animation_index % len(player_left)]
        surface.blit(current_frame, (screen_x, screen_y))

        if Debug:
            rect = self.get_rect()
            # Red player hitbox
            debug_rect = pygame.Rect(rect.x - camera_x,
                                     rect.y - camera_y,
                                     rect.width, rect.height)
            pygame.draw.rect(surface, (255, 0, 0), debug_rect, 3)

            # Player hitbox center dot
            center_x = self.x - camera_x + self.width // 4  # Offset by a quarter of the width to center the do
            center_y = self.y - camera_y + self.height // 2
            pygame.draw.circle(surface, (0, 255, 0), (center_x, center_y), 5)
            pygame.draw.circle(surface, (0, 0, 255), (center_x, center_y), 3)

            # Print coordinates and current FPS
            font = pygame.font.Font(None, 24)
            debug_text = font.render(f"X:{self.x:.0f} Y:{self.y:.0f}", True, (255, 255, 255))
            fps = int(clock.get_fps())
            fps_text = font.render(f"FPS: {fps}", True, (255,255,255))
            surface.blit(debug_text, (10, 30))
            surface.blit(fps_text, (10, 50))


class Camera:
    def __init__(self):
        # Initialize camera viewport matching screen dimensions
        self.x = 0  # Camera coordinate X in the game world
        self.y = 0  # Camera coordinate Y in the game world
        # Camera review (640x360)
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

    def update(self, player):  # Calculate camera coordinates in the game world
        self.x = player.x - SCREEN_WIDTH // 2
        self.y = player.y - SCREEN_HEIGHT // 2

    def apply(self, x, y):  # Convert world coordinates into screen ones
        return x - self.x, y - self.y


def draw_level(surface, level_data, camera):
    # TODO: add more objects
    for x, y in level_data["walls"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(wall, (screen_x, screen_y))
    for x, y in level_data["platforms"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(every_platform, (screen_x, screen_y))
    for x, y in level_data["money"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(money, (screen_x, screen_y))
    for x, y in level_data["buttons"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(button, (screen_x, screen_y))
    for x, y in level_data["spikes"]:
        screen_x, screen_y = camera.apply(x, y)
        surface.blit(spikes, (screen_x, screen_y))
    if Debug:
        # Show objects' hitboxes
        for x, y in level_data["walls"]:
            screen_x, screen_y = camera.apply(x, y)
            wall_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, (255, 0, 0), wall_hb, 2)
        for x, y in level_data["platforms"]:
            screen_x, screen_y = camera.apply(x, y)
            plat_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, (0, 0, 255), plat_hb, 2)
        for x, y in level_data["spikes"]:
            screen_x, screen_y = camera.apply(x, y)
            spike_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE // 2)
            pygame.draw.rect(surface, (255, 0, 0), spike_hb, 2)
        for x, y in level_data["money"]:
            screen_x, screen_y = camera.apply(x, y)
            coin_hb = pygame.rect.Rect(screen_x, screen_y, TILE_SIZE // 2, TILE_SIZE // 2)
            pygame.draw.rect(surface, (255, 0, 0), coin_hb, 2)


def change_lan():
    global start_button, levels_label, confirm_exit_label, yes, no, settings_label, my_levels_label, custom_levels_label
    global pause_label, exit_pause, F1_mode, debug_label, lose_label, win, lan_en, en_flag, CC, add_levels_label, delete_this_level
    global us_uk_flag, ru_flag, white
    global font, font1, font2, font3

    # Language settings
    # UI Text dictionary
    texts = {
        "en": {
            "play": "Play",
            "my levels": "My levels",
            "pause": "Pause",
            "win": "You won!",
            "lose": "You lost!",
            "settings": "Settings",
            "levels": "Levels",
            "exit_confirm": "Are you sure you want to exit?",
            "yes": "Yes",
            "no": "No",
            "exit": "Exit",
            "fullscreen": "Fullscreen mode",
            "debug": "Debug",
            "menu": "Menu",
            "coins": "Coins collected",
            "language": "Language",
            "Custom levels label": "Custom Levels",
            "add_levels_label": "Load level",
            "delete_this_level": "Incorrect file"
        },
        "ru": {
            "play": "Играть",
            "my levels": ["Мои", "уровни"],
            "pause": "Пауза",
            "win": "Вы выиграли!",
            "lose": "Вы проиграли!",
            "settings": "Настройки",
            "levels": "Уровни",
            "exit_confirm": "Вы точно хотите выйти?",
            "yes": "Да",
            "no": "Нет",
            "exit": "Выйти",
            "fullscreen": "Полноэкранный режим",
            "debug": "Отладка",
            "menu": "В меню",
            "coins": "Собрано монет",
            "language": "Язык",
            "Custom levels label": "Кастомные уровни",
            "add_levels_label": "Загрузить уровень",
            "delete_this_level": "Некорректный уровень"
        }
    }
    with open("player data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    LANGUAGE = "en" if en_flag else "ru"
    if not en_flag:
        current_flag = ru_flag
        CC = texts["ru"]["coins"]
        my_levels_label = [font3.render(texts[LANGUAGE]["my levels"][0], True, "black"),
                           font3.render(texts[LANGUAGE]["my levels"][1], True, "black")]

        data["settings"]["language"] = "ru"
    else:
        current_flag = us_uk_flag

        CC = texts["en"]["coins"]
        my_levels_label = font3.render(texts[LANGUAGE]["my levels"], True, "black")
        data["settings"]["language"] = "en"

    with open("player data/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    # Update all UI text elements based on current language

    start_button = font.render(texts[LANGUAGE]["play"], True, "black")
    levels_label = font1.render(texts[LANGUAGE]["levels"], True, "white")
    confirm_exit_label = font.render(texts[LANGUAGE]["exit_confirm"], True, "black")
    yes = font.render(texts[LANGUAGE]["yes"], True, "black")
    no = font.render(texts[LANGUAGE]["no"], True, "black")
    settings_label = font.render(texts[LANGUAGE]["settings"], True, "black")
    pause_label = font.render(texts[LANGUAGE]["pause"], True, (255, 255, 255))
    exit_pause = font.render(texts[LANGUAGE]["exit"], True, "black")
    F1_mode = font2.render(texts[LANGUAGE]["fullscreen"], True, "black")
    debug_label = font2.render(texts[LANGUAGE]["debug"], True, "black")
    lose_label = font.render(texts[LANGUAGE]["lose"], True, "black")
    win = font.render(texts[LANGUAGE]["win"], True, "black")
    custom_levels_label = font.render(texts[LANGUAGE]["Custom levels label"], True, "black")
    add_levels_label = font2.render(texts[LANGUAGE]["add_levels_label"], True, "black")


    # Language button text
    lan_en = font2.render(texts[LANGUAGE]["language"], True, "black")
    return current_flag



def draw_settings_menu():
    global white, white_hb, is_F1, Debug
    white.fill((255, 255, 255))  # Surface
    white.blit(exit_button, (290, 5))
    white.blit(settings_label, (120, 10))
    white.blit(g_F1, (45, 70))
    white.blit(g_debug, (45, 83))
    white.blit(F1_mode, (65, 66))
    white.blit(debug_label, (65, 80))
    selected_flag = change_lan()
    white.blit(selected_flag, (45, 40))
    white.blit(lan_en, (80, 45))
    if is_F1:
        white.blit(check, (45, 70))
    if Debug:
        white.blit(check, (45, 83))


def handle_white_click(mouse_pos, rect, callback):
    # Handle mouse clicks on white surface
    # Convert mouse coordinates into white surface ones
    x, y = mouse_pos[0] - 160, mouse_pos[1] - 90
    if rect.collidepoint(x, y):
        callback()


def file_select():
    global en_flag, root, custom_levels
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    if en_flag:
        file_path = tk.filedialog.askopenfilename(title="Select the file",
                                                  filetypes=[
                                                      ("JSON files", "*.json"),
                                                      ("Text files", "*.txt"),
                                                      ("permissible files", "*.txt;*.json")
                                                  ]
                                                  )
    else:
        file_path = tk.filedialog.askopenfilename(title="Выберите файл",
                                                  filetypes=[
                                                      ("JSON файлы", "*.json"),
                                                      ("Текстовые файлы", "*.txt"),
                                                      ("Разрешенные файлы", "*.txt;*.json")
                                                  ])

    if root:
        root.quit()
        root.destroy()
        root = None

    if not file_path:
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        if pathlib.Path(file_path).suffix == ".json":
            level = json.load(file)
        else:
            level = file.readlines()
    if pathlib.Path(file_path).suffix == ".json":
        if "map" not in level:

            winsound.MessageBeep(winsound.MB_ICONHAND)
            if en_flag:
                tk.messagebox.showerror("Error", "key 'map' not found. Edit file and try again")
            else:
                tk.messagebox.showerror("Ошибка", "Ключ 'map' не найден. Отредактируйте файл и попробуйте снова")
            return None
        else:
            for i in level["map"]:
                if "@" in i:
                    return file_path
            else:
                winsound.MessageBeep(winsound.MB_ICONHAND)
                if en_flag:
                    tk.messagebox.showerror("Loading error",
                                            f"Failed to load player data. Check the file '{pathlib.Path(file_path).name}' for the symbol '@' (player).")
                else:
                    tk.messagebox.showerror("Ошибка загрузки",
                                            f"не удалось загрузить информацию игрока. Проверьте файл '{pathlib.Path(file_path).name}' на наличие символа '@' (игрок).")
                return None
    if len(pathlib.Path(file_path).name) > 17:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        if en_flag:
            tk.messagebox.showerror("Error",
                                    "File's name is too long. Rename file and try again. Maximum length of the file is 17 symbols")
        else:
            tk.messagebox.showerror("Ошибка",
                                    "Имя файла слишком длинное. Переименуйте файл и попробуйте снова. Максимальная длина имени файла 17 символов")
        return None

    if pathlib.Path(file_path).name in custom_levels:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        if en_flag:
            tk.messagebox.showerror("Error", "The file is already loaded.")
        else:
            tk.messagebox.showerror("Ошибка", "Файл уже загружен.")
        return None

    return file_path


def save_custom_lvl():
    global custom_levels, en_flag, scroll_needle_update, custom_levels_dict
    path = file_select()

    if path is None:
        return
    path1 = path.replace("\\", "/")
    path = pathlib.Path(path1)
    dest_path = os.path.join("Custom Levels", path.name)

    custom_levels_dict[path.name] = True

    shutil.copy(path, dest_path)
    if path.name not in custom_levels:
        custom_levels.append(path.name)

    scroll_needle_update = True

    load_custom_levels_json()
    check_level()


def update_text_surface():
    global cached_text_surface, scroll_needle_update, custom_levels, line_height, font2, custom_levels_dict, delete_this_level
    global open_CL
    lines = custom_levels
    total_height = len(lines) * line_height
    if not total_height:
        cached_text_surface = pygame.Surface((0, 0))
    else:
        cached_text_surface = pygame.Surface((320 - 40, total_height), pygame.SRCALPHA)
        for i, line in enumerate(lines):
            rendered_line = font2.render(line, True, "black")
            cached_text_surface.blit(open_CL, (220, i * line_height))
            cached_text_surface.blit(trashcan, (190, i * line_height))
            cached_text_surface.blit(rendered_line, (0, i * line_height))

            if not custom_levels_dict.get(line, True):
                cached_text_surface.blit(delete_this_level, (120, i * line_height))

    scroll_needle_update = False


def y_CTS():
    global mouse_pos, scroll_y
    SURF_OFFSET_Y = 60

    return mouse_pos[1] - SURF_OFFSET_Y + scroll_y


def scroll():
    global scroll_y, max_scroll, line_height, custom_levels, cached_text_surface, scroll_needle_update
    # Update if it needs
    if scroll_needle_update or cached_text_surface is None:
        update_text_surface()

    total_height = len(custom_levels) * line_height
    canvas_height = 55
    max_scroll = max(0, total_height - canvas_height)
    scroll_y = max(0, min(scroll_y, max_scroll))


def safe_delete(file_path):
    global en_flag, custom_levels, scroll_needle_update, custom_levels_dict
    if os.path.exists(file_path):
        try:
            file_name = pathlib.Path(file_path).name
            if file_name in custom_levels_dict:
                del custom_levels_dict[file_name]
            if file_name in custom_levels:
                custom_levels.remove(file_name)
            load_custom_levels_json()
            check_level()

            os.remove(file_path)
            winsound.MessageBeep(winsound.MB_ICONHAND)
            if en_flag:
                tk.messagebox.showinfo("Deletion file",
                                       f"File '{file_path}' succesfully deleted from the custom level list.")
            else:
                tk.messagebox.showinfo("Удаление файла",
                                       f"Файл '{file_path}' успешно удален из списка кастомных уровней.")
            # custom_levels.remove(pathlib.Path(file_path).name)
            return True
        except Exception as e:
            winsound.MessageBeep(winsound.MB_ICONHAND)
            if en_flag:
                tk.messagebox.showerror("Deletion file", f"Something went wrong while deleting file '{file_path}'.")
            else:
                tk.messagebox.showerror("Удаление файла", f"Что-то пошло не так во время удаления файла '{file_path}'.")

            """update_text_surface()"""
            scroll_needle_update = True
            update_text_surface()

            return False
    else:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        if en_flag:
            tk.messagebox.showerror("Deletion file", f"File '{file_path}' does not exist")
        else:
            tk.messagebox.showerror("Удаление файла", f"Файл '{file_path}' не существует")
        return False


def delete_level(level_path):
    global cached_text_surface
    level = pathlib.Path(level_path).name
    global scroll_needle_update, en_flag, custom_levels
    winsound.MessageBeep(winsound.MB_ICONHAND)
    if en_flag:
        result = tk.messagebox.askyesno("Deletion file",
                                        f"Are you sure deleting file '{level}' from the custom level list?")
    else:
        result = tk.messagebox.askyesno("Удаление файла",
                                        f"Вы точно хотите удалить файл '{level}' из списка кастомных уровней?")
    if result:
        safe_delete(level_path)
        cached_text_surface = None
        scroll_needle_update = True

        update_text_surface()


# Correct the error checking file
def check_file():
    global custom_levels, en_flag, my_levels, custom_levels_dict, scroll_needle_update, scroll_flag, FT_flag
    if custom_levels:
        for i in custom_levels:
            path = "Custom Levels/" + i
            is_valid = True
            if pathlib.Path(path).suffix == ".json":
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        level = json.load(file)
                    if "map" not in level:
                        is_valid = False

                    else:
                        has_player = False
                        for row in level["map"]:
                            if "@" in row:
                                has_player = True
                                break
                        if not has_player:
                            is_valid = False

                except (FileNotFoundError, json.JSONDecodeError) as e:
                    is_valid = False
                    if not FT_flag:
                        if en_flag:
                            tk.messagebox.showerror("Read file error", f"Check the file '{pathlib.Path(path).name}' for the key 'map'")
                        else:
                            tk.messagebox.showerror("Ошибка чтения файла", f"Check the file '{pathlib.Path(path).name}' for the key 'map'")


                    if custom_levels_dict.get(i, True):
                        custom_levels_dict[i] = False
                    scroll_needle_update = True
            else:
                try:
                    with open(path,"r", encoding="utf-8") as file:
                        level = file.readlines()
                        has_player = False
                        for row in level:
                            if "@" in row:
                                has_player = True
                                break
                        if not has_player:
                            is_valid = False
                except FileNotFoundError:
                    is_valid = False

            if is_valid:
                if custom_levels_dict.get(i, True) == False:
                    custom_levels_dict[i] = True
                    scroll_needle_update = True
            else:
                if custom_levels_dict.get(i, True):
                    custom_levels_dict[i] = False
                    scroll_needle_update = True
                    if not FT_flag:
                        winsound.MessageBeep(winsound.MB_ICONHAND)




def draw_CL_menu():
    global custom_levels, custom_levels_dict
    global screen, white, white_hb, custom_levels_label, exit_button, plus, text_surface, add_levels_label, scroll_needle_update
    global scroll_flag
    white.fill((255, 255, 255))

    custom_levels = os.listdir("Custom Levels")

    if scroll_needle_update:
        update_text_surface()
        scroll_needle_update = False

    load_custom_levels()
    check_file()

    white.blit(add_levels_label, (45, 40))
    white.blit(custom_levels_label, (95, 5))

    white.blit(exit_button, (290, 5))
    white.blit(plus, (20, 40))
    visible_area = pygame.Rect(0, scroll_y, 320 - 40, 132)
    scroll()
    white.blit(cached_text_surface, (20, 60), area=visible_area)



    screen.blit(white, white_hb)
    if scroll_flag:
        load_custom_levels()
        check_file()

        scroll_flag = False


# Convert coordinates between surfaces
# From white surf. to screen
def white_screen(x, y):
    return (x + 160, y + 90)


# From 'cached_text_surface' to 'white'
def CTS_white(x, y):
    global scroll_y
    return (x + 20, y - scroll_y + 60)


# From 'cached_text_surface' to screen
def CTS_screen(x, y):
    global scroll_y
    return (x + 20 + 160, y - scroll_y + 60 + 90)


def load_custom_levels():
    global custom_levels, custom_levels_dict
    if not os.path.exists("Custom Levels"):
        os.makedirs("Custom Levels")

    folder_files = os.listdir("Custom Levels")
    for file in folder_files:
        if file not in custom_levels:
            if file.endswith("~"):
                continue

            custom_levels.append(file)
            custom_levels_dict[file] = True

def toggle_F1():
    global is_F1
    with open("player data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file) # Load the current player configuration
    is_F1 = not is_F1
    pygame.display.toggle_fullscreen()
    data["settings"]["F1 mode"] = is_F1
    with open("player data/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) # Load changes


def toggle_Debug():
    global Debug
    with open("player data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file) # Load the current player configuration
    Debug = not Debug
    data["settings"]["debug mode"] = Debug
    with open("player data/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) # Load changes


def load_custom_levels_json():
    global custom_levels_dict, custom_levels
    with open("player data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file) # Load the current player configuration
    if custom_levels:
        data["Custom Levels"]["list"] = custom_levels
    else:
        data["Custom Levels"]["list"] = []
    if custom_levels_dict:
        data["Custom Levels"]["dict"] = custom_levels_dict
    else:
        data["Custom Levels"]["dict"] = {}
    with open("player data/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) # Load changes

def check_level():
    global custom_levels_dict, custom_levels
    for i in custom_levels:
        with open("Custom Levels/"+i, "r", encoding="utf-8") as file:
            level = json.load(file)
        path = pathlib.Path("Custom Levels/"+i)
        if path.suffix == ".json":
            if "map" in level:
                for j in level["map"]:
                    if "@" in j:
                        custom_levels_dict[i] = True
                        break
                else:
                    custom_levels_dict[i] = False
            else:
                custom_levels_dict[i] = False
def load_data_file():
    global custom_levels, custom_levels_dict
    if os.path.exists("Custom Levels"):
        pass
    else:
        os.mkdir("Custom Levels")
    custom_levels = os.listdir("Custom Levels")
    with open("player data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    if not data:
        data["settings"] = {"language": "en", "F1 mode": True, "debug mode": False}
        data["Custom Levels"] = {"list": custom_levels, "dict": custom_levels_dict}
        with open("player data/data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False) # Load changes


line_height = 15  # Distance between lines
scroll_y = 0  # Current offset (how much scrolled)
scroll_speed = 20  # In pixels per step
max_scroll = None
cached_text_surface = None
scroll_needle_update = True

custom_levels_dict = {}
# Gameplay
# State variables
menu = True  # Main menu flag
pause = False
exit_game_flag = False  # Exit game button pressed flag
gameplay = False
is_open_setting = False
is_open_level_select_menu = False
available_jump = True
is_go = False
is_jump = False
is_F1 = True
Debug = False
death = False
complete = False  # Level complete flag
death_flag = 0
complete_flag = 0
pause_flag = 0
en_flag = True  # English language flag
my_levels = False # Custom Levels menu
scroll_flag = True
text_surface = None
player_cords = None
FT_flag = True

root = None

player = None
camera = None
level_data = None
CC = None  # Label "Coins Collected" in selected language

#custom_levels = []

'''
Formula for converting coordinates from the 'white' surface to the main screen:
x1 = x + 160, y1 = y + 90
x1, y1 - coordinates on the main screen
x, y - coordinates on the white surface
Formula for converting coordinated from the 'cached_text_surface' to the 'white' surface:
> x1 = x+20, y1 = y - scroll_y + 60
x1, y1 - coordinated on the 'white' surface
x, y - coordinates on the 'cached_text_surface'
'''

# Create a screen
pygame.init()
screen = pygame.display.set_mode((640, 360), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("JumpOverlord")
clock = pygame.time.Clock()

pause_bg_alpha = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pause_bg_alpha.set_alpha(128)
pause_bg_alpha.fill((0, 0, 0, 128))

# Load fonts and signs

font = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 20)
font1 = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 36)
font2 = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 12)
font3 = pygame.font.Font("fonts/OpenSans-VariableFont_wdth,wght.ttf", 16)

start_button = font.render("Play", True, "black")
levels_label = font1.render("Levels", True, "white")
confirm_exit_label = font.render("Are you sure you want to leave?", True, "black")
yes = font.render("Yes", True, "black")
no = font.render("No", True, "black")
settings_label = font.render("Settings", True, "black")
pause_label = font.render("Pause", True, (255, 255, 255))
exit_pause = font.render("Exit", True, "black")
F1_mode = font2.render("Fullscreen mode", True, "black")
debug_label = font2.render("Debug", True, "black")
my_levels_label = font2.render("My levels", True, "black")
custom_levels_label = font.render("Custom Levels", True, "black")
add_levels_label = font2.render("Load level", True, "black")
delete_this_level = font2.render("Incorrect file", True, "red")

lose_label = font.render("You lost!", True, "black")
restart = font.render("return to Main Menu", True, "black")
win = font.render("You won!", True, "black")
lan_en = font2.render("Language", True, "black")

# Load images
back = pygame.image.load("images/back.png").convert_alpha()
exit_button = pygame.image.load("images/exit_button.png").convert_alpha()
exit_game = pygame.image.load("images/exit_game.png").convert_alpha()
pause_button = pygame.image.load("images/pause_button.png").convert_alpha()
exit_pause_triangle = pygame.image.load("images/l_pause.png").convert_alpha()
check = pygame.image.load("images/check.png").convert_alpha()
gray = pygame.image.load("images/gray.png").convert_alpha()
retry_img = pygame.image.load("images/restart.png").convert_alpha()
setting = pygame.image.load("images/setting.png").convert_alpha()
us_uk_flag = pygame.image.load("images/US_UK_flag.png").convert_alpha()
ru_flag = pygame.image.load("images/RU_flag.jpg").convert_alpha()
label_MM = pygame.image.load("images/label.png").convert_alpha()
plus = pygame.image.load("images/plus.jpg").convert_alpha()
trashcan = pygame.image.load("images/trashcan.jpg").convert_alpha()
copy_folder = pygame.image.load("images/folder.jpg").convert_alpha()
open_CL = pygame.image.load("images/open_CL.png").convert_alpha()

one = pygame.image.load("level signs/1.png").convert_alpha()
two = pygame.image.load("level signs/2.png").convert_alpha()
three = pygame.image.load("level signs/3.png").convert_alpha()
four = pygame.image.load("level signs/4.png").convert_alpha()

level_bg = pygame.image.load("images/level_menu1.jpg").convert()
gaming_bg = pygame.image.load("images/gamingbg.jpg").convert()
# Create the surface "white" (surface for a background when opening widgets)
white = pygame.Surface((320, 180))
white.fill((255, 255, 255))
white_hb = white.get_rect()
white_hb.center = (640 // 2, 360 // 2)
# Load textures
player_texture = pygame.image.load("images/player.png").convert_alpha()  # игрок
enemy = pygame.image.load("images/enemy.png").convert_alpha()  # враг
wall = pygame.image.load("images/brickwall.jpg").convert_alpha()  # стена
every_platform = pygame.image.load("images/platform.jpg").convert_alpha()
spikes = pygame.image.load("images/spikes.png").convert_alpha()
money = pygame.image.load("images/money.png")
door = pygame.image.load("images/door.png")
cp0 = pygame.image.load("images/checkpoint0.png").convert_alpha()
cp1 = pygame.image.load("images/checkpoint1.png").convert_alpha()
start_end = pygame.image.load("images/startend.png").convert_alpha()
chest = pygame.image.load("images/chest.png").convert_alpha()
FAK = pygame.image.load("images/FAK.png").convert_alpha()  # First aid kit
button = pygame.image.load("images/button0.png").convert_alpha()

# Load player textures
player_right = [
    pygame.image.load('pright/sprite_13.png').convert_alpha(),
    pygame.image.load('pright/sprite_14.png').convert_alpha(),
    pygame.image.load('pright/sprite_15.png').convert_alpha(),
    pygame.image.load('pright/sprite_16.png').convert_alpha()
]
player_left = [
    pygame.image.load('pleft/sprite_9.png').convert_alpha(),
    pygame.image.load('pleft/sprite_10.png').convert_alpha(),
    pygame.image.load('pleft/sprite_11.png').convert_alpha(),
    pygame.image.load('pleft/sprite_12.png').convert_alpha()
]
# Create simple figures
Start_button = pygame.rect.Rect((270, 130, 100, 50))  # Start button
setting_rect = pygame.rect.Rect((580, 300, 60, 60))

# Create select markers (in settings)
g_F1 = gray
g_debug = gray

if os.path.exists("Custom Levels"):
    custom_levels = os.listdir("Custom Levels")
else:
    os.mkdir("Custom Levels")
    custom_levels = []



running = True
while running:

    if FT_flag:
        check_file()
        load_data()
        load_custom_levels_json()
        check_level()
        FT_flag = False

    mouse = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    if not gameplay:
        # Draw the main menu
        screen.fill((37, 150, 190))

        # Create a start button
        screen.blit(label_MM, (270, 130))
        screen.blit(start_button, (290, 140))

        # Create a Creator menu button
        screen.blit(label_MM, (270, 180))
        if not en_flag:
            screen.blit(my_levels_label[0], (290, 180))
            screen.blit(my_levels_label[1], (290, 200))
        else:
            screen.blit(my_levels_label, (290, 192))

        # Create a settings button
        pygame.draw.rect(screen, (255, 255, 255), setting_rect)
        screen.blit(setting, (587, 307))
        # Create an exit game button
        screen.blit(exit_game, (0, 0))

        # Update the surface
        if not is_open_setting and not exit_game_flag and not my_levels:
            white.fill((255, 255, 255))

        # Initialize settings menu
        if is_open_setting and not exit_game_flag and not my_levels:
            screen.blit(white, white_hb)
            draw_settings_menu()

        # Initialize exit game menu
        if exit_game_flag and not is_open_setting and not my_levels:
            screen.blit(white, white_hb)  # Create a settings surface
            # Create a game exit confirmation
            white.blit(exit_button, (290, 5))
            white.blit(confirm_exit_label, (20, 20))
            white.blit(yes, (120, 130))
            white.blit(no, (180, 130))
        # Initialize select level menu
        if is_open_level_select_menu:
            screen.blit(level_bg, (0, 0))
            screen.blit(exit_button, (0, 0))
            screen.blit(levels_label, (280, 20))
            screen.blit(one, (50, 75))  # Create the first level label
            screen.blit(two, (125, 75))
            pygame.display.update()

        if not my_levels:
            scroll_flag = True

        # initialize Load Custom Level menu
        if my_levels and not exit_game_flag and not is_open_setting:
            draw_CL_menu()



    else:
        # Initialize game
        if player and camera and level_data:
            if not pause and not death and not complete:
                # Reset flags
                death_flag = 0
                pause_flag = 0
                complete_flag = 0

                if player:
                    player.move(keys, level_data)
                    camera.update(player)

                # Draw game
                screen.blit(gaming_bg, (0, 0))
                if camera:
                    draw_level(screen, level_data, camera)
                player.draw(screen, camera.x, camera.y)
                screen.blit(pause_button, (0, 0))

            elif pause:
                # Create exit pause button surface
                exit_pause = pygame.Surface((25, 25))
                exit_pause.fill((255, 255, 255))
                # Render pause menu static UI elements once
                if pause_flag == 0:  # Render elements that need to be drawn only once
                    screen.blit(pause_bg_alpha, (0, 0))
                    screen.blit(pause_label, (SCREEN_WIDTH // 2 - pause_label.get_width() // 2, 10))  # Center the label
                    screen.blit(exit_pause_triangle,
                                (SCREEN_WIDTH // 2 - pause_label.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - pause_label.get_height()))
                    # Render alternative exit UI buttons
                    screen.blit(exit_pause, (0, 0))
                    screen.blit(exit_button, (0, 0))
                    # Render resume game icon
                    screen.blit(pygame.transform.flip(back, True, False), (610, 5))
                    pause_flag = 1

            elif death:
                pause = False
                pause_flag = 0
                # Render Game Over UI elements once
                if death_flag == 0:  # Render elements that need to be drawn only once
                    screen.blit(pause_bg_alpha, (0, 0))
                    # Center and render the UI elements
                    screen.blit(lose_label, (SCREEN_WIDTH // 2 - 60, 25))
                    screen.blit(retry_img, (SCREEN_WIDTH // 2 + 30, 250))
                    # Center and render the exit button
                    screen.blit(pygame.transform.scale(exit_button, (45, 45)), (SCREEN_WIDTH // 2 - 30, 250))
                    death_flag = 1
            # Render Victory Screen UI elements once
            elif complete:
                pause = False
                pause_flag = 0
                if complete_flag == 0:  # Render elements that need to be drawn only once
                    screen.blit(pause_bg_alpha, (0, 0))
                    screen.blit(win, (SCREEN_WIDTH // 2 - 60, 25))
                    screen.blit(pygame.transform.scale(exit_button, (45, 45)), (SCREEN_WIDTH // 2 - 60, 250))

                    # Render and draw collected coins counter
                    coin_c = font.render(f"{CC}: {coin}/{coins_level}", True, "black")
                    screen.blit(coin_c, (SCREEN_WIDTH // 2 - 60, 100))

                    complete_flag = 1

    clock.tick(FPS)
    pygame.display.update()
    # Main event loop
    for event in pygame.event.get():
        # Exit the game
        if event.type == pygame.QUIT:
            if root is not None:
                root.destroy()
            pygame.quit()
            sys.exit(0)

        # Handle keyboard input events
        if event.type == pygame.KEYDOWN:
            # Handle "ESCAPE" input events
            if event.key == pygame.K_ESCAPE:
                if gameplay:  # Toggle pause mode
                    pause = not pause
                elif not gameplay and not is_open_setting and not exit_game_flag and not is_open_level_select_menu and not my_levels:
                    # Trigger exit confirmation dialog from the game
                    exit_game_flag = True
                elif not gameplay and is_open_level_select_menu:
                    # Close level selection menu and return to main menu
                    is_open_level_select_menu = False
                elif exit_game_flag and not is_open_setting and not my_levels:
                    # Quit the game entirely from exit confirmation screen
                    running = False
                elif my_levels:
                    my_levels = False
                elif is_open_setting:
                    is_open_setting = False
                # Toggle fullscreen mode
            if event.key == pygame.K_F1 and not gameplay:
                pygame.display.toggle_fullscreen()
            # Do jump
            if player and gameplay and not pause:
                player.jump(event)

        # Handle mouse input events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos  # Get current mouse cursor coordinates on click

                # Main Menu navigation
                if not gameplay and not is_open_level_select_menu:
                    # Handle "Play" button click to open level selection
                    if Start_button.collidepoint(
                            mouse_pos) and not is_open_setting and not exit_game_flag and not my_levels:
                        is_open_level_select_menu = True

                    # Handle "Settings" button click to open settings
                    elif setting_rect.collidepoint(mouse_pos) and not exit_game_flag and not my_levels:
                        is_open_setting = True
                    # Settings menu navigation
                    elif is_open_setting:
                        # Toggle fullscreen mode in settings
                        if g_F1.get_rect(topleft=(white_screen(45, 70))).collidepoint(mouse_pos):
                            toggle_F1()
                        # Toggle debug mode
                        elif g_debug.get_rect(topleft=(white_screen(45, 83))).collidepoint(mouse_pos):
                            toggle_Debug()
                        # Handle "Close Settings" button click
                        elif is_open_setting and exit_button.get_rect(topleft=(white_screen(290, 5))).collidepoint(
                                mouse_pos):
                            is_open_setting = False
                        # Change language
                        elif us_uk_flag.get_rect(topleft=(white_screen(45, 50))).collidepoint(
                                mouse_pos) and is_open_setting:
                            en_flag = not en_flag
                            draw_settings_menu()

                    # Handle "Exit Game" button click
                    elif exit_game.get_rect(topleft=(0, 0)).collidepoint(
                            mouse_pos) and not is_open_setting and not my_levels:
                        exit_game_flag = True

                    # Handle "Change Language (flag)" button click
                    # Handle exit confirmation input
                    elif exit_game_flag and not my_levels:
                        if yes.get_rect(topleft=(white_screen(120, 130))).collidepoint(mouse_pos):
                            running = False
                        elif no.get_rect(topleft=(white_screen(180, 130))).collidepoint(mouse_pos) or \
                                exit_button.get_rect(topleft=(white_screen(290, 5))).collidepoint(mouse_pos):
                            exit_game_flag = False

                    # Handle 'Custom Levels' menu clicks
                    elif label_MM.get_rect(topleft=(270, 180)).collidepoint(mouse_pos):
                        my_levels = True

                    elif my_levels and not is_open_setting and not exit_game_flag and not is_open_level_select_menu:  # Level Creator navigation
                        if exit_button.get_rect(topleft=(white_screen(290, 5))).collidepoint(mouse_pos):
                            my_levels = False
                        elif plus.get_rect(topleft=(white_screen(20, 40))).collidepoint(mouse_pos):
                            save_custom_lvl()
                        for i in range(len(custom_levels)):
                            # Get trashcan coordinates on the cached_text_surface
                            trashcan_cached_x = 190
                            trashcan_cached_y = i * line_height

                            # Convert coordinates into the screen ones
                            screen_x, screen_y = CTS_screen(trashcan_cached_x, trashcan_cached_y)

                            trashcan_rect = trashcan.get_rect(topleft=(screen_x, screen_y))

                            if trashcan_rect.collidepoint(mouse_pos):
                                delete_level("Custom Levels/" + custom_levels[i])
                                draw_CL_menu()

                                break
                            # Get play button coordinates on the cached_text_surface
                            play_custom_level_cached_x = 220
                            play_custom_level_cached_y = i * line_height
                            # Convert coordinates into the screen ones
                            screen_x, screen_y = CTS_screen(play_custom_level_cached_x, play_custom_level_cached_y)

                            play_custom_level_rect = open_CL.get_rect(topleft=(screen_x, screen_y))

                            if play_custom_level_rect.collidepoint(mouse_pos):
                                success = reset_level("Custom Levels/" + custom_levels[i])
                                if success:
                                    gameplay = True
                                else:

                                    gameplay = False

                                    level_data = None
                                    player = None
                                    camera = None
                                break



                # Level Selection menu navigation
                elif is_open_level_select_menu and not my_levels:
                    # Handle "Back to Main Menu" button click
                    if exit_button.get_rect(topleft=(0, 0)).collidepoint(mouse_pos):
                        is_open_level_select_menu = False
                    # Launch Levels using the universal reset function
                    elif one.get_rect(topleft=(50, 75)).collidepoint(mouse_pos):
                        reset_level("levels/level 1.json")

                    elif two.get_rect(topleft=(125, 75)).collidepoint(mouse_pos):
                        reset_level("levels/level 2.json")

                # Gameplay UI navigation
                elif gameplay:
                    if not pause and not death and not complete:
                        # Handle pause button click in the corner
                        if pause_button.get_rect(topleft=(0, 0)).collidepoint(mouse_pos):
                            pause = True

                    elif pause:
                        # Pause menu navigation
                        # Handle "Resume" button click
                        if exit_pause_triangle.get_rect(topleft=(SCREEN_WIDTH // 2 - pause_label.get_width() // 2,
                                                                 SCREEN_HEIGHT // 2 - pause_label.get_height())).collidepoint(
                            mouse_pos):
                            pause = False
                        # Handle "Return to Main Menu" button click
                        if back.get_rect(topleft=(610, 5)).collidepoint(mouse_pos):
                            # Reset game state flags
                            gameplay = False
                            pause = False
                            death = False
                            complete = False
                            death_flag = 0
                            complete_flag = 0
                            is_open_level_select_menu = False
                            timer = 0
                        # Handle "Close pause" button click
                        elif exit_button.get_rect(topleft=(0, 0)).collidepoint(mouse_pos):
                            pause = False
                if death:
                    # Death screen navigation
                    # Handle Exit to Main Menu button click
                    if pygame.transform.scale(exit_button, (45, 45)).get_rect(
                            topleft=(SCREEN_WIDTH // 2 - 30, 250)).collidepoint(mouse_pos):
                        # Reset game state flags
                        gameplay = False
                        death = False
                        death_flag = 0
                        complete = False
                        complete_flag = 0
                        coin = 0
                    # Handle retry button click
                    elif retry_img.get_rect(topleft=(SCREEN_WIDTH // 2 + 30, 250)).collidepoint(mouse_pos):
                        reset_level(Level_path)
                elif complete:
                    # Victory screen navigation
                    if pygame.transform.scale(exit_button, (45, 45)).get_rect(
                            topleft=(SCREEN_WIDTH // 2 - 60, 250)).collidepoint(mouse_pos):
                        # Reset game state flags
                        complete = False
                        gameplay = False
                        is_open_level_select_menu = False
                        complete_flag = 0
                        death_flag = 0
                        coin = 0
                        # timer = 0
            elif event.button == 4:  # Wheel up
                scroll_y = max(0, scroll_y - scroll_speed)
            elif event.button == 5:  # Wheel down
                scroll_y = min(scroll_y + scroll_speed, max_scroll)

    # Scroll with keyboard arrows
    if keys[pygame.K_UP]:
        scroll_y -= scroll_speed
    if keys[pygame.K_DOWN]:
        scroll_y += scroll_speed

        # Limit scroll to avoid falling into the void
        if scroll_y < 0:
            scroll_y = 0
        elif scroll_y > max_scroll:
            scroll_y = max_scroll
