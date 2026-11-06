"""
obstacle_gen.py — Obstacle & platform generation (Moses)
Uses a Genetic Algorithm (DEAP) to evolve playable level layouts.

A chromosome is a list of SEGMENTS. Each segment is:
  [platform_width, gap_width, enemy_type, platform_height_offset]
  - platform_width:        2–8 tiles wide
  - gap_width:             0–4 tiles (0 = no gap)
  - enemy_type:            0=none, 1=snowball, 2=jumpy
  - platform_height_offset: -2 to +2 tiles relative to previous
"""
import random
from deap import base, creator, tools, algorithms

# ── Tile IDs (SuperTux world1 tileset) ──────────────────────────
TILE_AIR   = 0
TILE_SOLID = 1    # basic ground tile — replace with correct IDs from data/tiles.strf
TILE_BRICK = 2

LEVEL_WIDTH  = 60   # tiles across
LEVEL_HEIGHT = 15   # tiles tall
BASE_Y       = 11   # row index of the ground (0 = top)

# ── DEAP setup ──────────────────────────────────────────────────
NUM_SEGMENTS = 12   # number of platform segments per level

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def random_segment():
    return [
        random.randint(2, 8),    # platform_width
        random.randint(0, 4),    # gap_width
        random.randint(0, 2),    # enemy_type
        random.randint(-2, 2),   # height_offset
    ]

toolbox.register("individual", tools.initRepeat, creator.Individual,
                 random_segment, n=NUM_SEGMENTS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
    """
    Fitness function — higher is better.
    Rewards: playability, variety, appropriate difficulty.
    Penalizes: impossible gaps, monotonous layouts, out-of-bounds platforms.
    """
    score = 0.0
    prev_height = BASE_Y
    gap_sizes = []
    platform_widths = []

    for seg in individual:
        p_width, gap, enemy, h_offset = seg
        new_height = prev_height + h_offset

        # Penalize platforms out of vertical bounds
        if new_height < 4 or new_height > LEVEL_HEIGHT - 2:
            score -= 10

        # Penalize gaps the player can't jump (> 4 tiles is too wide for Tux)
        if gap > 4:
            score -= 5 * (gap - 4)

        # Reward having some gaps (variety)
        if 1 <= gap <= 3:
            score += 2

        # Reward varied platform widths
        platform_widths.append(p_width)

        # Reward enemies (adds challenge) but not too many
        if enemy > 0:
            score += 1

        gap_sizes.append(gap)
        prev_height = new_height

    # Reward variety in platform widths (std dev > 1)
    if len(set(platform_widths)) > 3:
        score += 5

    return (score,)


toolbox.register("evaluate", evaluate)
toolbox.register("mate",    tools.cxTwoPoint)
toolbox.register("mutate",  tools.mutUniformInt,
                 low=[-2, 0, 0, -2], up=[8, 4, 2, 2], indpb=0.2)
toolbox.register("select",  tools.selTournament, tournsize=3)


def chromosome_to_tilemap(individual):
    """Convert a chromosome into a 2D tile grid."""
    grid = [[TILE_AIR] * LEVEL_WIDTH for _ in range(LEVEL_HEIGHT)]
    enemies = []
    x = 2
    cur_y = BASE_Y

    for seg in individual:
        p_width, gap, enemy_type, h_offset = seg
        cur_y = max(4, min(LEVEL_HEIGHT - 2, cur_y + h_offset))

        # Draw platform tiles
        for px in range(x, min(x + p_width, LEVEL_WIDTH)):
            for py in range(cur_y, LEVEL_HEIGHT):
                grid[py][px] = TILE_SOLID

        # Place enemy on platform
        if enemy_type == 1 and p_width >= 3:
            ex = (x + x + p_width) // 2
            ey = (cur_y - 1) * 32
            enemies.append(f'(snowball (x {ex * 32}) (y {ey}))')
        elif enemy_type == 2 and p_width >= 4:
            ex = (x + x + p_width) // 2
            ey = (cur_y - 1) * 32
            enemies.append(f'(jumpy (x {ex * 32}) (y {ey}))')

        x += p_width + gap
        if x >= LEVEL_WIDTH - 4:
            break

    flat_tiles = [tile for row in grid for tile in row]
    return flat_tiles, enemies, x


def generate_obstacles(seed=None, generations=20, pop_size=50):
    """
    Run the GA and return the best level layout.
    Returns a dict with tiles, enemies, dimensions, and difficulty score.
    """
    if seed is not None:
        random.seed(seed)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)

    algorithms.eaSimple(pop, toolbox,
                        cxpb=0.5, mutpb=0.3,
                        ngen=generations,
                        halloffame=hof,
                        verbose=False)

    best = hof[0]
    tiles, enemies, end_x = chromosome_to_tilemap(best)
    fitness_score = best.fitness.values[0]

    # Normalise difficulty to 0.0–1.0 for other generators
    difficulty = min(1.0, max(0.0, (fitness_score + 20) / 60))

    return {
        "tiles":      tiles,
        "enemies":    enemies,
        "width":      LEVEL_WIDTH,
        "height":     LEVEL_HEIGHT,
        "spawn_y":    (BASE_Y - 1) * 32,
        "end_x":      end_x * 32,
        "difficulty": difficulty,
    }
