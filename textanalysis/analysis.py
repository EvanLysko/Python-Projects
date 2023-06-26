from collections import Counter
import os
import pandas as pd
import matplotlib.pyplot as plt

text = "This is my test text. We're keeping this text short to keep things manageable."


def count_words(text):
    """
    Count the number of times each word occurs in text (str). Return dictionary
    where keys are unique words and values are word counts. Skips punctuation.
    """
    text = text.lower()
    skips = [".", ",", ";", ":", "''", '""']
    for ch in skips:
        text = text.replace(ch, "")

    word_counts = {}
    for word in text.split(" "):
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    return word_counts

print(count_words(text))

def count_words_fast(text):
    """
    Count the number of times each word occurs in text (str). Return dictionary
    where keys are unique words and values are word counts. Skips punctuation.
    """
    text = text.lower()
    skips = [".", ",", ";", ":", "'", '"', "?","!"]
    for ch in skips:
        text = text.replace(ch, "")

    word_counts = Counter(text.split(" "))

    return word_counts

print(count_words_fast(text))
print(len(count_words("This comprehension check is to check for comprehension.")))
print(count_words(text) is count_words_fast(text))


def read_book(title_path):
    """
    Read a book and return it as a string.
    """
    with open(title_path, "r", encoding="utf8") as current_file:
        text = current_file.read()
        text = text.replace("\n", "").replace("\r", "")

    return text


def word_stats(word_counts):
    """Returns number of unique words and frequencies."""
    num_unique = len(word_counts)
    counts = word_counts.values()

    return (num_unique, counts)

text = read_book("/Users/evanlysko/Desktop/PythonforResearch/textanalysis/books/English/shakespeare/Romeo and Juliet.txt")
word_counts = count_words(text)
print(word_counts)
(num_unique, counts) = word_stats(word_counts)
print(num_unique)
print(sum(counts))

stats = pd.DataFrame(columns = ("language", "author", "title", "length", "unique"))
title_num = 1
book_dir = "/Users/evanlysko/Desktop/PythonforResearch/textanalysis/books"
for language in os.listdir(book_dir):
    if not language.startswith('.'):
        for author in os.listdir(book_dir + "/" + language):
            if not author.startswith('.'):
                for title in os.listdir(book_dir + "/" + language + "/" + author):
                    if not title.startswith('.'):
                        inputfile = book_dir + "/" + language + "/" + author + "/" + title
                        print(inputfile)
                        text = read_book(inputfile)
                        (num_unique, counts) = word_stats(count_words(text))
                        stats.loc[title_num] = language, author.capitalize(), title.replace(".txt", ""), sum(counts), num_unique
                        title_num += 1
print(stats)

scatterplot = plt.plot(stats.length, stats.unique, "bo")
print(scatterplot)
scatterplot = plt.loglog(stats.length, stats.unique, "bo")
print(scatterplot)

print(stats[stats.language == "English"])

plt.figure(figsize = (10, 10))
subset = stats[stats.language == "English"]
plt.loglog(subset.length, subset.unique, "o", label = "English", color = "crimson")

subset = stats[stats.language == "French"]
plt.loglog(subset.length, subset.unique, "o", label = "French", color = "forestgreen")

subset = stats[stats.language == "German"]
plt.loglog(subset.length, subset.unique, "o", label = "German", color = "orange")

subset = stats[stats.language == "Portuguese"]
plt.loglog(subset.length, subset.unique, "o", label = "Portuguese", color = "blueviolet")
plt.legend()
plt.xlabel("Book Length")
plt.ylabel("Number of unique words")
plt.savefig("lang_plot.pdf")
