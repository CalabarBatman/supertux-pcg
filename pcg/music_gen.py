"""
music_gen.py — Music generation (Magdala)
Phase 1: selects existing SuperTux tracks based on level intensity.
Phase 2 (TODO): use DEAP GA to generate original musical sequences.
"""
import random

# Existing SuperTux music tracks (paths relative to data/)
# See data/music/ for the full list
TRACKS = {
    "calm": [
        "music/chipdisko.ogg",
        "music/clarabell.ogg",
    ],
    "moderate": [
        "music/fortress.ogg",
        "music/voc-mango.ogg",
    ],
    "intense": [
        "music/theme.ogg",
        "music/antarctica.ogg",
    ],
}


def _intensity_tier(intensity: float) -> str:
    if intensity < 0.35:
        return "calm"
    elif intensity < 0.70:
        return "moderate"
    else:
        return "intense"


def generate_music(intensity: float = 0.5) -> dict:
    """
    Select a music track that matches the level intensity.

    Args:
        intensity: 0.0–1.0 from obstacle_gen difficulty score
    Returns:
        dict with track path
    
    TODO (Phase 2 — GA approach):
        - Represent a musical phrase as a chromosome of (note, duration, velocity) genes
        - Use DEAP to evolve phrases that score well on:
            * key consistency (all notes in scale)
            * rhythmic regularity
            * intensity match (note density, velocity)
        - Export the best individual as a .ogg file using a MIDI → audio pipeline
    """
    tier = _intensity_tier(intensity)
    track = random.choice(TRACKS[tier])
    return {
        "track":     track,
        "tier":      tier,
        "intensity": intensity,
    }
