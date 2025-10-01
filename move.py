import json
import random

# read waiting_time.json to get the waiting time for each move
with open("waiting_time.json", "r") as f:
    waiting_times = json.load(f)

class Move:
    SIDES = ["forehand", "backhand"]
    ZONES = ["front", "back"]
    MOVE_TYPES = ["net", "lift", "drop", "smash", "clear"]
    DIRECTIONS = ["straight", "cross"]

    def __init__(self, side: str, zone: str, move_type: str, direction: str, wait_time: float = None):
        self.side = side  # "F" or "B"
        self.zone = zone  # "front" or "back"
        self.move_type = move_type  # "net", "lift", "drop", "smash", "clear"
        self.direction = direction  # "straight" or "cross"
        self.wait_time = waiting_times[self.move_type][self.direction]

    def __str__(self):
        return f"{self.side} \n{self.zone} \n{self.direction} {self.move_type}"


    @classmethod
    def random_move(cls):
        """Create a Move with random attributes obeying zone constraints."""
        zone = random.choice(cls.ZONES)
        side = random.choice(cls.SIDES)
        direction = random.choice(cls.DIRECTIONS)

        # Constrain move_type based on zone
        if zone == "front":
            move_type = random.choice(["net", "lift"])
        else:  # back zone
            move_type = random.choice(["drop", "smash", "clear"])

        return cls(side=side, zone=zone, move_type=move_type, direction=direction)

