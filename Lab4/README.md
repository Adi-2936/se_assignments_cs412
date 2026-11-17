# Flappy Bird - Lab 4 Vibe Coding

**Student:** Adithya Singh<br>
**SRN:** PES2UG24CS412

A completed Pygame implementation of the assigned Flappy Bird starter project.

## Completed tasks

- Accurate circle-to-pipe collision detection, including swept pipe movement.
- A game-over screen with the final score and collision reason.
- Replay choices for Easy, Medium, and Hard difficulty, plus exit controls.
- Generated sound feedback for flapping, scoring, and dying.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

## Controls

| Action | Control |
| --- | --- |
| Flap | `Space` or left mouse click |
| Easy replay | `1`, `E`, or click Easy |
| Medium replay | `2`, `M`, or click Medium |
| Hard replay | `3`, `H`, or click Hard |
| Exit after game over | `Q` or `Esc` |

## Test

```bash
python -m unittest discover -s tests -v
```

The five tests cover edge collision, high-speed swept collision, game-over state,
difficulty replay, scoring, and sound-event feedback.

## Lab deliverables

The `Lab-4` directory contains both 10-second gameplay videos, the exported chat
history PDF, submission notes, and the complete submission ZIP. Updated code is at
the repository root.
