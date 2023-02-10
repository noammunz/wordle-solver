import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import nltk
nltk.download("words")

words = list(set(nltk.corpus.words.words()))
words = [word.lower() for word in words if len(word) == 5]

occurances = [0] * 26

# character occurrences
for word in words:
    for char in word:
        occurances[ord(char) - 97] += 1

# normalizing the counts between 0-10
occurances = [(10 * count / max(occurances)) for count in occurances]

def score_word(word):
    score = 0
    word_set = set(word)
    score += 2 * len(word_set)
    for char in word_set:
        score += occurances[ord(char) - 97]
    return score

colors = {'rgba(0, 0, 0, 0)': 'black', 'rgba(58, 58, 60, 1)': 'gray', 'rgba(181, 159, 59, 1)': 'yellow', 'rgba(83, 141, 78, 1)': 'green', 'rgba(18, 18, 19, 1)': 'black'}


# generate a list of words
word_scores = sorted([(word, score_word(word)) for word in words], key=lambda x: x[1], reverse=True)

# setting up driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.nytimes.com/games/wordle/index.html")

# closing pop-up on arrival
element = driver.find_element(By.CLASS_NAME, 'game-icon')
element.click()

# clicking on page (to input text)
element = driver.find_element(By.CLASS_NAME, 'App-module_game__yruqo')
element.click()

word = None
row = 1

while not word:
    # guessing a word
    guess = word_scores.pop(0)[0]
    actions = ActionChains(driver)
    actions.send_keys(guess + Keys.ENTER)
    actions.perform()
    actions.send_keys(Keys.BACKSPACE * 5)
    actions.perform()
    time.sleep(2)

    # checking colors
    elements = driver.find_elements(By.CLASS_NAME, 'Tile-module_tile__UWEHN')
    curr_elements = elements[(row-1)*5:row*5]
    curr_colors = [colors[element.value_of_css_property('background-color')] for element in curr_elements]

    # word doesn't exist
    if curr_colors.count('black') == 5:
        continue

    # correct word
    if curr_colors.count('green') == 5:
        word = guess
        print('The word is: ' +  word)
        break

    # filtering word list
    for i, color in enumerate(curr_colors):
        char = guess[i]
        if color == 'gray':
            word_scores = [(word, score) for word, score in word_scores if char not in word]
        elif color == 'yellow':
            word_scores = [(word, score) for word, score in word_scores if char in word and word[i] != char]
        elif color == 'green':
            word_scores = [(word, score) for word, score in word_scores if word[i] == char]

    print(f'Remaining words: {len(word_scores)}\nRemaining tries: {6-row}\n************************************')

    # moving to next row
    if row == 6:
        print('Failed to find word')
        break
    else: row += 1

time.sleep(5)
driver.quit()