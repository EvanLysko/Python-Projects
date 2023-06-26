# DO NOT EDIT THIS CODE!
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
print(hamlets)

language, text = hamlets.iloc[0]
counted_text = count_words_fast(text)
(num_unique, counts) = word_stats(counted_text)
data = pd.DataFrame(columns = ("word", "count", "length", "frequency"))
type(counted_text.keys())
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
    data.loc[row] = words[i], counts[i], len(words[i]), frequency
    row +=1
print(data)

sub_data = pd.DataFrame(columns = ("language", "frequency", "mean_word_length", "num_words"))
mean_word_length = {"frequent" : sums_of_word_length["frequent"]/frequency_count["frequent"],
                    "infrequent" : sums_of_word_length["infrequent"]/frequency_count["infrequent"],
                    "unique" : sums_of_word_length["unique"]/frequency_count["unique"]}
frequency = ["frequent", "infrequent", "unique"]
row = 1
sub_data.loc[row] = language, frequency, list(mean_word_length.values()), list(frequency_count.values())

print(sub_data)
sub_data.to_csv(r'/Users/evanlysko/Desktop/PythonforResearch/hamletanalysis/output.csv')

def summarize_text(language, text):
    counted_text = count_words_fast(text)
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

grouped_data = pd.DataFrame()
language, text = hamlets.iloc[0]
language, text = hamlets.iloc[0]
language, text = hamlets.iloc[0]
