# Outplay RPG

A basic CLI RPG framework built with Python.

## Features
- **Cross-platform**: Clear screen logic works on Windows and Linux/macOS.
- **Robust Input**: Safe input handler to catch `Ctrl+C` or empty inputs.
- **State-based Engine**: Simple flow management (Menu -> Game -> Exit).

## How to Run
Make sure you have Python 3.x installed.

```bash
python main.py
```

## Project Structure
- `main.py`: Entry point.
- `src/`:
    - `engine.py`: Core game engine and logic.
    - `utils.py`: Terminal and input utilities.