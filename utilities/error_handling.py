import logging
import os
import traceback
from datetime import datetime
from shutil import copyfile
from typing import Any

import pygame

from constants import SAVE_FILE


LOGGER = logging.getLogger(__file__)
error_dir = "error_saves"


def catch_error() -> str:
    if not os.path.isdir(error_dir):
        os.makedirs(error_dir)
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    out_file_name = os.path.join(error_dir, f"{dt_string}_error_save.sav")
    in_file_name = os.path.join("saves", SAVE_FILE)
    copyfile(in_file_name, out_file_name)
    return dt_string


def save_error(dt_string: str, screen: Any) -> None:
    out_file_name = os.path.join(error_dir, f"{dt_string}_error_trace.txt")
    with open(out_file_name, "w") as out_file:
        traceback.print_exc(file=out_file)
    LOGGER.warning(f"ERROR LOG SAVED TO {out_file_name}")
    out_file_name = os.path.join(error_dir, f"{dt_string}_error_screencap.jpeg")
    pygame.image.save(screen, out_file_name)
