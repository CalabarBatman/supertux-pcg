# SuperTux PCG — COMP 4980 | Thompson Rivers University

**Team:** Daniel Anyogo · Moses Kpughur-Tule · Magdala Nwuke

Procedural content generation for [SuperTux](https://github.com/SuperTux/supertux).
Generates playable levels using genetic algorithms (obstacles, music) and a rule-based approach (backgrounds).

---

## Project structure

```
supertux/
├── pcg/
│   ├── generate_level.py   # integration script — run this to make a level
│   ├── obstacle_gen.py     # GA: platforms, gaps, enemies        (Moses)
│   ├── background_gen.py   # rule-based: backgrounds, lighting   (Daniel)
│   ├── music_gen.py        # GA: music selection / generation    (Magdala)
│   └── requirements.txt
└── output/
    └── generated_levels/   # generated .stl files land here
```

---

## Team setup (do this once)

### 1. Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Visual Studio 2022 Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) with **Desktop development with C++**
- [CMake](https://cmake.org/download/) (add to PATH during install)

### 2. Clone the repo

```cmd
git clone https://github.com/YOUR_USERNAME/supertux-pcg.git
cd supertux-pcg
git submodule update --init --recursive
```

### 3. Install Python dependencies

```cmd
cd pcg
pip install -r requirements.txt
```

### 4. Build SuperTux (one-time, ~20–40 min first run)

```cmd
cd ..
winget install Microsoft.VisualStudio.2022.BuildTools
winget install Kitware.CMake

git clone https://github.com/microsoft/vcpkg.git C:\vcpkg
C:\vcpkg\bootstrap-vcpkg.bat

mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake
cmake --build . --config Release
```

The game executable will be at `build/Release/supertux2.exe`.

---

## Generating and playing a level

```cmd
cd pcg

# Generate a level (random seed)
python generate_level.py

# Generate with a fixed seed (reproducible — good for testing)
python generate_level.py --seed 42

# Specify an output path
python generate_level.py --out ../output/generated_levels/my_level.stl
```

Then play it:

```cmd
cd ..
build\Release\supertux2.exe --level output/generated_levels/pcg_seed_42.stl
```

---

## Daily workflow

```cmd
git pull                        # get teammates' latest changes
# ... work on your file in pcg/ ...
git add pcg/your_file.py
git commit -m "describe what you changed"
git push
```

After pulling changes, re-run `git submodule update --init --recursive` only if
someone updated the submodules (rare).

---

## Who does what

| Component | File | Method | Owner |
|-----------|------|--------|-------|
| Obstacle generation | `pcg/obstacle_gen.py` | Genetic Algorithm (DEAP) | Moses |
| Background generation | `pcg/background_gen.py` | Rule-based | Daniel |
| Music generation | `pcg/music_gen.py` | Genetic Algorithm (DEAP) | Magdala |
| Integration | `pcg/generate_level.py` | Calls all three | All |

---

## References

1. Broadbent & Corradini (2024) — GA terrain generation, IEEE EAIS
2. Yap et al. (2021) — GA music composition, IEEE SCOReD
3. Togelius et al. (2011) — Search-based PCG taxonomy
4. Schaa & Barriga (2024) — Platform level generator evaluation
