def simplify_instruction(instruction: str, handedness: str) -> str:
    """
    Simplify the instruction string by replacing 
    - forehand front with '1', 
    - forehand back with '2',
    - backhand back with '3',
    - backhand front with '4'
    """
    forehand = "right" if handedness == "R" else "left"
    backhand = "left" if handedness == "R" else "right"

    mapping = {
        f"{forehand} front": "1",
        f"{forehand} back": "2",
        f"{backhand} back": "3",
        f"{backhand} front": "4"
    }

    for key, value in mapping.items():
        instruction = instruction.replace(key, value)

    return instruction