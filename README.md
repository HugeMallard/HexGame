# HexGame

A hex-based game built with PyGame and OpenGL.

## Setup

1. Install Poetry: https://python-poetry.org/docs/
2. From the repository root, run:

   ```sh
   poetry install
   ```

3. Run the game with:

   ```sh
   poetry run python main.py
   ```

   or

   ```sh
   poetry run hexgame
   ```

## Notes

- Dependency management has moved to Poetry via `pyproject.toml`.
- `pip install -r requirements.txt` is deprecated for this repository.
- To export a pip-compatible requirements file from Poetry if needed:

  ```sh
  poetry export -f requirements.txt --output requirements.txt --without-hashes
  ```
