import json
import random

# read waiting_time.json to get the waiting time for each move
with open("waiting_time.json", "r") as f:
    waiting_times = json.load(f)

class Move:
    SIDES = ["F", "B"]  # forehand or backhand
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
        return f"Move(side={self.side}, zone={self.zone}, move_type={self.move_type}, direction={self.direction}, wait_time={self.wait_time})"

    @classmethod
    def random_move(cls):
        """Create a Move with random attributes."""
        return cls(
            side=random.choice(cls.SIDES),
            zone=random.choice(cls.ZONES),
            move_type=random.choice(cls.MOVE_TYPES),
            direction=random.choice(cls.DIRECTIONS)
        )

