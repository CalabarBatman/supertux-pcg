"""
generate_level.py — Integration script
Runs all three PCG generators and assembles a .stl level file.

Usage:
    python generate_level.py              # random seed
    python generate_level.py --seed 42   # reproducible
    python generate_level.py --out output/generated_levels/my_level.stl
"""
import argparse
import os
import random
import time

from obstacle_gen import generate_obstacles
from background_gen import generate_background
from music_gen import generate_music


def build_stl(obstacles, background, music, level_name="PCG Level") -> str:
    """Assemble the three components into a valid SuperTux .stl string."""
    tilemap_data = " ".join(str(t) for t in obstacles["tiles"])
    enemies_block = "\n    ".join(obstacles["enemies"])

    stl = f"""(supertux-level
  (version 3)
  (name ("{level_name}"))
  (author "PCG Generator")
  (license "CC-BY-SA 4.0 International")
  (sector
    (name "main")
    (ambient-light
      (color {background["ambient_r"]} {background["ambient_g"]} {background["ambient_b"]})
    )
    (background
      (image "{background["image"]}")
      (speed {background["scroll_speed"]})
    )
    (music "{music["track"]}")
    (tilemap
      (layer "foreground")
      (solid #t)
      (speed-x 1)
      (speed-y 1)
      (width {obstacles["width"]})
      (height {obstacles["height"]})
      (tiles {tilemap_data})
    )
    {enemies_block}
    (spawnpoint
      (name "main")
      (x 64)
      (y {obstacles["spawn_y"]})
    )
    (end-sequence
      (x {obstacles["end_x"]})
      (y 192)
    )
  )
)
"""
    return stl


def main():
    parser = argparse.ArgumentParser(description="SuperTux PCG Level Generator")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--out", type=str, default=None, help="Output .stl file path")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else int(time.time())
    random.seed(seed)
    print(f"Generating level with seed: {seed}")

    # Run each generator
    print("  [1/3] Generating obstacles (Moses)...")
    obstacles = generate_obstacles(seed=seed)

    print("  [2/3] Generating background (Daniel)...")
    background = generate_background(difficulty=obstacles["difficulty"])

    print("  [3/3] Generating music (Magdala)...")
    music = generate_music(intensity=obstacles["difficulty"])

    # Assemble .stl
    level_name = f"PCG Level (seed {seed})"
    stl_content = build_stl(obstacles, background, music, level_name)

    # Write output
    out_path = args.out or f"output/generated_levels/pcg_seed_{seed}.stl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(stl_content)

    print(f"\nLevel written to: {out_path}")
    print(f"To play it, run:")
    print(f"  supertux2.exe --level {out_path}")


if __name__ == "__main__":
    main()
