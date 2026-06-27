# 2D platformer written on Python, PyGame
[License: MIT](LICENSE)

Read this in other languages: [Russian/Русский](README.ru.md)

Read full documentation: [Documentation](Documentation.md)

This is the active development branch. Check the educational one: [Repository](https://github.com/SIBDuck/JumpOverlord/)


- **Two playable levels** (more coming soon)
- **Dual language** - English and Russian

## Mechanics
- **Coyote time** - jump forgiveness after leaving a ledge
- **Jump buffer** - jump input buffering before landing
- **Pause menu**
- **Death menu**
- **Victory menu**
- **Debug mode** - show hitboxes (enable in settings)

- 🆕 **Custom Levels** — you can add and play custom levels using `.txt` and `.json` files
- 🆕 Settings auto-save — your language, fullscreen mode, and debug mode preferences are saved and loaded automatically when you restart the game.
- 🆕 FPS counter — shows framerate (enable in Debug mode)

### How to Add Your Own Level?

Adding a custom level is super easy! Here's how:

- Check the [GitHub page](https://github.com/SIBDuck/JumpOverlord-play/blob/main/objects/supported%20objects.md) for the full list of symbols you can use.

#### **Option 1: Using a `.txt` file**
- Just write your level map in a text file using the symbols supported by the game. 

#### **Option 2: Using a `.json` file**
- Create a JSON file with a `"map"` key. The value should be a list of strings, where each string represents one row of your level.

Once your file is ready, just load it in the game and you're good to go!

## Controls
- A/D - movement
- SPACE - jump
- ESC - pause
- F1 - toggle fullscreen mode

## Gameplay - screenshots and GIFs

![Screenshot 1](images/screenshot1.png)
![Screenshot 2](images/screenshot2.png)
![Screenshot 3](images/screenshot3.png)
![Screenshot 4](images/screenshot4.png)
![Screenshot 5](images/screenshot5.png)
![Screenshot 6](images/screenshot6.png)
![Gameplay GIF](images/game.gif)

## Installation
1. Download `JumpOverlord.zip` 
2. Unzip the file
3. Open `JumpOverlord/`
4. Run `Main.exe` (no Python installation required)

## System Requirements

### Minimum:
- **OS:** Windows 10 / 11 (64-bit)
- **Processor:** 1.5 GHz
- **RAM:** 256 MB
- **Graphics:** DirectX 9 or OpenGL 2.0 compatible
- **Storage:** 200 MB available space
- **Display:** 640x360 (scales to any resolution)

### Recommended:
- **OS:** Windows 10 / 11 (64-bit)
- **Processor:** 2.0 GHz (dual-core)
- **RAM:** 512 MB+
- **Graphics:** OpenGL 3.0 compatible
- **Storage:** 200 MB+ available space
- **Display:** 1920x1080 (fullscreen supported)

## 📁 Project Structure
### JumpOverlord
```
JumpOverlord/                     # Project root folder
│
├── Main.py                       # Main game file (entry point)
├── Main.spec                     # PyInstaller config (.exe build)
├── Main.exe                      # Main game executable
│
├── objects/                      # Game objects (supported ones, .json)
│   ├── supported objects.md
│   └── objects.json
│
├── player data/                  # Player data
│   └── data.json
│
├── images/                       # Images (textures, buttons, flags, background)
├── level signs/                  # Level signs
├── levels/                       # Level files (.txt, .json)
├── fonts/                        # Fonts (OpenSans)
├── pleft/                        # Player sprites (left movement)
├── pright/                       # Player sprites (right movement)
│
├── Documentation_screens/        # Code screenshots (5 appendices)
│   ├── Appendix_1/
│   ├── Appendix_2/
│   ├── Appendix_3/
│   ├── Appendix_4/
│   └── Appendix_5/
│
├── Custom Levels/                # Custom levels
│
├── screenshots_gifs/             # Screenshots and GIFs for README
│
├── .gitignore                    # Ignored files (build/, dist/, .idea/, etc.)
│
├── README.md                     # Project description (English)
├── README.ru.md                  # Project description (Russian)
│
├── DOCUMENTATION.md              # Full documentation (English)
├── DOCUMENTATION.ru.md           # Full documentation (Russian)
│
├── LICENSE                       # MIT License
```
## 🙏 Thanks
- Python, Pygame
- Google Fonts (Open Sans)
- Flaticon, Iconfinder
- Various free sources (Pinterest, etc.)

## License
**MIT** — free to use, modify, and share.  
Designed as educational material for beginners.
