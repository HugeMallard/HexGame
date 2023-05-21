import os
import pygame
from utilities import scale_and_rotate_image
from utilities import resize_image_by_scale
from typing import List
from typing import Any
import pickle
import io
import copy

root_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.join(root_dir, "assets")


images_to_load = dict(
    grid_hex="grid_hex.png"
)

sounds_to_load = dict(
)

music_to_load = dict(
)


class AssetPreloader(object):
    def save_sound_dict(self, file_name="raw_audio.dat"):
        save_dict = {}
        for key, value in self._sound_dict.items():
            if isinstance(value, pygame.mixer.Sound):
                save_dict[key] = (value.get_raw(), "sound")
                continue
            save_dict[key] = (value, "music")
        with open(os.path.join(root_dir, file_name), "wb") as out_file:
            pickle.dump(save_dict, out_file)

    def load_sound_dict(self, file_name="raw_audio.dat"):
        with open(os.path.join(root_dir, file_name), "rb") as in_file:
            load_input = pickle.load(in_file)

        for key, value in load_input.items():
            sound = value[0]
            sound_type = value[1]
            if sound_type == "sound":
                self._sound_dict[key] = pygame.mixer.Sound(sound)
                continue
            self._sound_dict[key] = sound

    def save_image_dict(self, file_name="raw_assets.dat"):
        save_dict = {}
        for key, value in self._image_dict.items():
            if isinstance(value, pygame.Surface):
                save_dict[key] = (
                    pygame.image.tostring(value, "RGBA"),
                    value.get_size(),
                )
            if isinstance(value, (list, tuple)):
                temp = [(pygame.image.tostring(v, "RGBA"), v.get_size()) for v in value]
                save_dict[key] = temp

        with open(os.path.join(root_dir, file_name), "wb") as out_file:
            pickle.dump(save_dict, out_file)

    def process_image(self, img):
        if self.old_isr != self.game.isr or self.game.isr != 1:
            return resize_image_by_scale(img, self.game.isr)
        return img.convert_alpha()

    def load_image_dict(self, file_name="raw_assets.dat"):
        with open(os.path.join(root_dir, file_name), "rb") as in_file:
            load_input = pickle.load(in_file)

        self._image_dict = dict()
        for key, value in load_input.items():
            if isinstance(value, tuple):
                image = value[0]
                size = value[1]
                self._image_dict[key] = self.process_image(
                    pygame.image.fromstring(image, size, "RGBA")
                )
                continue
            temp = [
                self.process_image(pygame.image.frombuffer(i[0], i[1], "RGBA"))
                for i in value
            ]
            self._image_dict[key] = temp
        self.old_isr = self.game.isr

    def image(self, key_name: str, *, rotation: int=0, size: List[int]=None, force_size: bool=False) -> Any:
        scale_ratio = self.game.isr
        images = self._image_dict[key_name]
        if isinstance(images, list):
            transformed = []
            for image in images:
                img = scale_and_rotate_image(
                    image, scale_ratio, size, rotation, force_size
                )
                transformed.append(img)
            return transformed
        image = scale_and_rotate_image(images, scale_ratio, size, rotation, force_size)
        return image

    def sound(self, key_name):
        sound = pygame.mixer.Sound(self._sound_dict[key_name].get_raw())
        sound.set_volume(self.game.sound_volume)
        return sound

    def music(self, key_name):
        music = copy.deepcopy(self._sound_dict[key_name])
        music.seek(0)
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(self.game.music_volume)

    def __init__(self, game):
        self.game = game
        self.old_isr = None
        self._image_dict = dict()
        self._sound_dict = dict()

    def load(self):
        for key_name, sound_name in sounds_to_load.items():
            self.load_sound(key_name, sound_name)
        for key_name, image_name in images_to_load.items():
            self.load_image(key_name, image_name)
        for key_name, music_name in music_to_load.items():
            self.load_music(key_name, music_name)
        self.save_image_dict()
        self.save_sound_dict()

    def load_image(self, key_name, image_name):
        assert key_name not in self._image_dict.keys()
        if "." not in image_name:
            images = load_images(image_name)
        else:
            images = load_image(image_name)
        self._image_dict[key_name] = images

    def load_sound(self, key_name, sound_name):
        assert key_name not in self._sound_dict.keys()
        sound = load_sound(sound_name)
        assert sound not in self._sound_dict.values()
        self._sound_dict[key_name] = sound

    def load_music(self, key_name, sound_name):
        """
        Loads a sound into the system as music
        """
        assert key_name not in self._sound_dict.keys()
        music = load_music(sound_name)
        assert music not in self._sound_dict.values()
        self._sound_dict[key_name] = music


def load_images(folder, allow_fail=False, in_dir=main_dir):
    folder = os.path.join(in_dir, folder)
    if allow_fail and not os.path.exists(folder):
        return []
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    images = []
    for image in files:
        if os.path.splitext(image)[1] == ".png":
            try:
                surface = pygame.image.load(os.path.join(in_dir, folder, image))
                images.append(surface.convert_alpha())
            except pygame.error:
                raise SystemExit(
                    'Could not load image "%s" %s' % (image, pygame.get_error())
                )
    return images


def load_image(file_name, allow_fail=False, in_dir=main_dir):
    """loads an image, prepares it for play"""
    image = os.path.join(in_dir, "img", file_name)
    if allow_fail and not os.path.isfile(image):
        return
    try:
        surface = pygame.image.load(image)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (image, pygame.get_error()))
    return surface.convert_alpha()


def load_sound(file_name):
    """because pygame can be be compiled without mixer."""
    if not pygame.mixer:
        return None
    sound_file = os.path.join(main_dir, file_name)
    try:
        sound = pygame.mixer.Sound(file=sound_file)
        return sound
    except Exception:
        print("Warning, unable to load, %s" % file_name)
        raise
    return None


def load_music(file_name):
    sound_file = os.path.join(main_dir, file_name)
    try:
        with open(sound_file, "rb") as in_file:
            buffer = io.BytesIO(in_file.read())
        return buffer
    except Exception:
        print("Warning, unable to load, %s" % file_name)
        raise
    return None
