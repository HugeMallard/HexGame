from typing import List
from typing import Optional
from typing import Tuple

from PIL.Image import Image as Img


class MockAssetPreloader(object):
    def __init__(self) -> None:
        pass

    def image(
        self,
        key_name: str,
        *,
        rotation: int = 0,
        size: Optional[Tuple[int, int]] = None,
        force_size: bool = False
    ) -> List[str]:
        return ["test_image"]


class MockGame(object):
    def __init__(self, version: str, debug: bool):
        self.version = version
        self.debug = debug
        self.asset_preloader = MockAssetPreloader()
