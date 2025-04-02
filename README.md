# Wordle Solver Bot

This is a simple Python script that automates playing Wordle using Selenium. It selects words based on character frequency and feedback from previous guesses to efficiently solve the puzzle.

## Requirements
- Python 3
- Google Chrome
- ChromeDriver
- Required Python libraries:
  ```sh
  pip install selenium nltk
  ```

## How It Works
1. Loads a list of 5-letter words from the NLTK corpus.
2. Ranks words based on character frequency.
3. Uses Selenium to interact with the Wordle webpage, guessing words and reading feedback.
4. Eliminates words based on feedback and refines future guesses.
5. Continues until the correct word is found or all attempts are used.

## Usage
1. Ensure you have Chrome and ChromeDriver installed.
2. Run the script:
   ```sh
   python wordle_solver.py
   ```
3. The script will automatically play Wordle and display the correct word if found.

## Notes
- The script runs in incognito mode to avoid saved game data.
- Adjust `time.sleep()` if needed to accommodate loading times.

## Disclaimer
This script is for educational purposes only. Use it responsibly.

