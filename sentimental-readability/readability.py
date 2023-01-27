# TODO
from cs50 import get_string

text = get_string("Text: ")
letterCount = 0
wordCount = 1
sentenceCount = 0

for char in text:
    if char.isalpha():
        letterCount += 1
    elif char == " ":
        wordCount += 1
    elif char in ["!", "?", "."]:
        sentenceCount += 1

#0.0588 * L - 0.296 * S - 15.8
grade = round((0.0588 * 100 *(letterCount/wordCount)) - (0.296 * 100 * (sentenceCount/wordCount)) - 15.8)
if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")



