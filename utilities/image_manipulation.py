from typing import Optional
from typing import Tuple

import pygame
from PIL import Image


def resize_image_by_scale(img: Image, scale_ratio: float = 1.5) -> Image:
    image_string = pygame.image.tostring(img, "RGBA", False)
    image = Image.frombytes("RGBA", img.get_size(), image_string)
    x = int(image.width * scale_ratio)
    y = int(image.height * scale_ratio)
    if img.get_width() == x and img.get_height() == y:
        return img
    image = image.resize((x, y), Image.ANTIALIAS)
    return pygame.image.fromstring(
        image.tobytes("raw", "RGBA"), image.size, "RGBA"
    ).convert_alpha()


def resize_image(img: Image, size: Tuple[int, int]) -> Image:
    if img.get_width() == size[0] and img.get_height() == size[1]:
        return img
    image_string = pygame.image.tostring(img, "RGBA", False)
    image = Image.frombytes("RGBA", img.get_size(), image_string)
    image = image.resize(size, Image.ANTIALIAS)
    return pygame.image.fromstring(
        image.tobytes("raw", "RGBA"), image.size, "RGBA"
    ).convert_alpha()


def scale_and_rotate_image(
    img: Image,
    ratio: float,
    size: Optional[Tuple[int, int]] = None,
    rotation: int = 0,
    force_size: bool = False,
) -> Image:
    if size:
        scale = size if force_size else [int(size[0] * ratio), int(size[1] * ratio)]
        img = resize_image(img, scale)  # type: ignore
    else:
        img = img.convert_alpha()

    if rotation:
        img = pygame.transform.rotate(img, rotation)
    return img
