"""
background_gen.py — Background & scenery generation (Daniel)
Rule-based approach: selects background assets that match the level's difficulty.
"""

# Available SuperTux backgrounds (paths relative to data/)
# Add more from data/images/background/ as needed
BACKGROUNDS = {
    "easy": [
        "/images/background/arctis/arctis2.png",
        "/images/background/misc/airship.png",
    ],
    "medium": [
        "/images/background/forest/forest2.png",
        "/images/background/misc/ghostforest.png",
    ],
    "hard": [
        "/images/background/misc/nightsky.png",
        "/images/background/misc/darkforest.png",
    ],
}

# Ambient light colors per difficulty (R G B, range 0.0–1.0)
AMBIENT_LIGHT = {
    "easy":   (0.9, 0.9, 1.0),   # bright, cool
    "medium": (0.7, 0.7, 0.8),   # slightly dim
    "hard":   (0.4, 0.4, 0.6),   # dark, moody
}

SCROLL_SPEED = {
    "easy":   0.5,
    "medium": 0.4,
    "hard":   0.3,
}


def _difficulty_tier(difficulty: float) -> str:
    """Map 0.0–1.0 difficulty score to a named tier."""
    if difficulty < 0.4:
        return "easy"
    elif difficulty < 0.7:
        return "medium"
    else:
        return "hard"


def generate_background(difficulty: float = 0.5) -> dict:
    """
    Rule-based background selection.
    
    Args:
        difficulty: 0.0 (easy) to 1.0 (hard), from obstacle_gen
    Returns:
        dict with image path, ambient light values, and scroll speed
    """
    import random
    tier = _difficulty_tier(difficulty)

    image = random.choice(BACKGROUNDS[tier])
    r, g, b = AMBIENT_LIGHT[tier]
    speed  = SCROLL_SPEED[tier]

    return {
        "image":        image,
        "ambient_r":    r,
        "ambient_g":    g,
        "ambient_b":    b,
        "scroll_speed": speed,
        "tier":         tier,
    }
