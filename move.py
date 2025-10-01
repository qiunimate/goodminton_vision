# ====== MOVE DEFINITION ======
import random

# Example waiting times (can be loaded from JSON if you want)
waiting_times = {
    "net": {"straight": 1.0, "cross": 1.2},
    "lift": {"straight": 2.5, "cross": 2.7},
    "drop": {"straight": 2.0, "cross": 2.2},
    "smash": {"straight": 2.5, "cross": 2.7},
    "clear": {"straight": 2.5, "cross": 2.7}
}

class Move:
    SIDES = ["left", "right"]
    ZONES = ["front", "back"]
    MOVE_TYPES = ["net", "lift", "drop", "smash", "clear"]
    DIRECTIONS = ["straight", "cross"]

    # ====== INITIALIZATION ======
    def __init__(self, side: str, zone: str, move_type: str, direction: str):
        self.side = side
        self.zone = zone
        self.move_type = move_type
        self.direction = direction
        self.wait_time = waiting_times[self.move_type][self.direction]

    def __str__(self):
        return f"{self.side} | {self.zone} | {self.direction} {self.move_type}"

    # ====== RANDOM MOVE GENERATION ======
    @classmethod
    def random_move(cls):
        """Create a Move with constraints based on zone."""
        zone = random.choice(cls.ZONES)
        side = random.choice(cls.SIDES)
        direction = random.choice(cls.DIRECTIONS)

        # Constrain move_type based on zone
        if zone == "front":
            move_type = random.choice(["net", "lift"])
        else:
            move_type = random.choice(["drop", "smash", "clear"])

        return cls(side=side, zone=zone, move_type=move_type, direction=direction)
