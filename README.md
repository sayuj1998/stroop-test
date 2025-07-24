<p align="center">
  <img src="https://github.com/user-attachments/assets/c46fb7d1-80e3-4f68-a6ac-84ab6194f346" alt="Stroop Test Screenshot" width="600">
</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/aab865ab-e982-494a-b7de-b54b3486c5d5" alt="Stroop Test Screenshot 2" width="600">
</p>



# Stroop Test Game

A cognitive psychology experiment built in Python using Pygame, designed to measure reaction time and cognitive interference (based on the classic Stroop effect).

---

## How It Works

Participants are shown color names (like "RED" or "GREEN") rendered in a font color that may not match the word itself. The task is to **click the button that matches the **font color**, not the word**.

Reaction times are recorded for each trial, and incorrect answers are tracked. Results are saved to a local text file.

---

## Requirements

- Python
- [Pygame](https://www.pygame.org/)

Install with:

```
pip install pygame
```

## How To Run

1. Clone the repository:
```
git clone https://github.com/sayuj1998/stroop-test.git
cd stroop-test
```

2. Run the game:
```
python stroop_test.py
```

## Features
- Clean GUI using Pygame
- Text input for user's name
- Color-word interference test with clickable color buttons
- Tracks:
  - Reaction time per trial
  - Average reaction time
  - Incorrect responses
  - Saves results to reaction_times.txt

## Change Number of Trials
To adjust the number of trials in the game, change this line inside the **main** block:
```
stroop_test.run_test(trials=4)
```

## What is the Stroop Effect?
The Stroop effect is a psychological phenomenon where your brain takes longer to name the color of the word when the word itself spells a different color. This task demonstrates cognitive interference and is often used in cognitive science and psychology research.

## License
This project is licensed under the **MIT License**.
Feel free to use, modify, and share it.
