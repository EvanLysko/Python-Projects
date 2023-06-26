import os
import pandas as pd
import numpy as np
from collections import Counter

def count_words_fast(text):
    text = text.lower()
    skips = [".", ",", ";", ":", "'", '"', "\n", "!", "?", "(", ")"]
    for ch in skips:
        text = text.replace(ch, "")
    word_counts = Counter(text.split(" "))
    return word_counts

def word_stats(word_counts):
    num_unique = len(word_counts)
    counts = word_counts.values()
    return (num_unique, counts)

hamlets = pd.read_csv("/Users/evanlysko/Desktop/PythonforResearch/hamletanalysis/asset-v1%3AHarvardX+PH526x+2T2019+type@asset+block@hamlets.csv", index_col = 0)
print(type(hamlets))

def summarize_text(language, text):
    counted_text = count_words_fast(text)
    (num_unique, counts) = word_stats(counted_text)
    data = pd.DataFrame(columns = ("word", "count", "length", "frequency"))
    words = list(counted_text.keys())
    counts = list(counted_text.values())
    row = 1
    frequency = 'none'
    frequency_count = {"frequent" : 0, "infrequent" : 0, "unique": 0}
    sums_of_word_length = {"frequent" : 0, "infrequent" : 0, "unique": 0}

    for i in range(len(counted_text)):
        if counts[i] > 10:
            frequency = 'frequent'
            frequency_count["frequent"] += 1
            sums_of_word_length["frequent"] += len(words[i])
        elif 1 < counts[i] <= 10:
            frequency = 'infrequent'
            frequency_count["infrequent"] += 1
            sums_of_word_length["infrequent"] += len(words[i])
        elif counts[i] == 1:
            frequency = 'unique'
            frequency_count["unique"] += 1
            sums_of_word_length["unique"] += len(words[i])

    mean_word_length = {"frequent" : sums_of_word_length["frequent"]/frequency_count["frequent"],
                        "infrequent" : sums_of_word_length["infrequent"]/frequency_count["infrequent"],
                        "unique" : sums_of_word_length["unique"]/frequency_count["unique"]}

    sub_data = pd.DataFrame({
        "language": language,
        "frequency": ["frequent","infrequent","unique"],
        "mean_word_length": list(mean_word_length.values()),
        "num_words": list(frequency_count.values())})

    return(sub_data)

#language, text = hamlets.iloc[0]
#print(type())


grouped_data = pd.DataFrame(columns = ("language", "frequency", "mean_word_length", "num_words"))
for i in range(3):
    language, text = hamlets.iloc[i]
    grouped_data = grouped_data.append(summarize_text(language, text))

print(grouped_data)
grouped_data.to_csv(r'/Users/evanlysko/Desktop/PythonforResearch/hamletanalysis/output2.csv')

colors = {"Portuguese": "green", "English": "blue", "German": "red"}
markers = {"frequent": "o","infrequent": "s", "unique": "^"}
import matplotlib.pyplot as plt
for i in range(grouped_data.shape[0]):
    row = grouped_data.iloc[i]
    plt.plot(row.mean_word_length, row.num_words,
        marker=markers[row.frequency],
        color = colors[row.language],
        markersize = 10
    )

color_legend = []
marker_legend = []
for color in colors:
    color_legend.append(
        plt.plot([], [],
        color=colors[color],
        marker="o",
        label = color, markersize = 10, linestyle="None")
    )
for marker in markers:
    marker_legend.append(
        plt.plot([], [],
        color="k",
        marker=markers[marker],
        label = marker, markersize = 10, linestyle="None")
    )
plt.legend(numpoints=1, loc = "upper left")

plt.xlabel("Mean Word Length")
plt.ylabel("Number of Words")
# write your code to display the plot here!
plt.show()
plt.savefig("hamanalysis.pdf")
