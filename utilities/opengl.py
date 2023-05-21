from typing import Any
from typing import Optional

from OpenGL import GL


# basic openGL.gl configuration
def setup_gl(width: int, height: int) -> None:
    GL.glViewport(0, 0, width, height)
    GL.glDepthRange(0, 1)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    GL.glClearDepth(1.0)
    GL.glDisable(GL.GL_DEPTH_TEST)
    GL.glDisable(GL.GL_LIGHTING)
    GL.glDepthFunc(GL.GL_LEQUAL)
    GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST)
    GL.glEnable(GL.GL_BLEND)


def init_open_gl(generate_tex_id: bool = False) -> Optional[Any]:
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glDisable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_TEXTURE_2D)
    if generate_tex_id:
        texID = GL.glGenTextures(1)
        return texID
    return None


def surface_to_texture(pygame_surface: Any, texID: Any) -> None:
    w, h = pygame_surface.get_size()
    GL.glBindTexture(GL.GL_TEXTURE_2D, texID)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        GL.GL_RGB,
        w,
        h,
        0,
        GL.GL_BGRA,
        GL.GL_UNSIGNED_BYTE,
        # pygame_surface.get_buffer().raw,
        pygame_surface.get_view("0").raw,
    )
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


def draw_open_gl(texID: Any) -> None:
    GL.glBindTexture(GL.GL_TEXTURE_2D, texID)
    GL.glBegin(GL.GL_QUADS)
    GL.glTexCoord2f(0, 0)
    GL.glVertex2f(-1, 1)
    GL.glTexCoord2f(0, 1)
    GL.glVertex2f(-1, -1)
    GL.glTexCoord2f(1, 1)
    GL.glVertex2f(1, -1)
    GL.glTexCoord2f(1, 0)
    GL.glVertex2f(1, 1)
    GL.glEnd()
