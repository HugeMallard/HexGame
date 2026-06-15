# HexGame

A hex-based game built with PyGame and OpenGL.

## Setup

1. Install uv: https://github.com/uv/uv or install with pip:

   ```sh
   python -m pip install --user uv
   ```

2. From the repository root, install dependencies:

   ```sh
   uv sync --all-groups
   ```

3. Install the git hooks:

   ```sh
   uv run pre-commit install
   ```

4. Run pre-commit manually across all files:

   ```sh
   uv run pre-commit run --all-files
   ```

5. Run the test suite:

   ```sh
   uv run pytest
   ```

6. Run the game with:

   ```sh
   uv run python main.py
   ```

   or

   ```sh
   uv run hexgame
   ```
