import pandas as pd
from nltk import ngrams
import argparse
from macros import *
import csv
from TableManager import TableManager
import time

no_dup_anchor_table = TableManager("no_dup_anchors")


def to_utf8(input_string):
    local_string = input_string.encode()
    local_string = local_string.decode("utf-8")
    return local_string


def open_abbreviation(word):
    if word in ABBREVIATIONS.keys():
        return ABBREVIATIONS[word]
    return word


def get_all_spots(file_descriptor):
    text = open(file_descriptor, 'r', encoding='utf-8')
    data = text.read()
    spots = []
    for gram_size in range(1,5):
        grams_list = []
        grams = ngrams(data.split(), gram_size)
        skip_flag = False
        for gram in grams:
            gram = list(gram)
            for j in range(2,gram_size+1):
                if gram[j-1] in ABBREVIATIONS.keys() or gram[j-1] in ABBREVIATIONS.items():
                    skip_flag = True
            gram[0] = open_abbreviation(gram[0])
            for j in range(gram_size-1, -1, -1):
                if j == gram_size-1:
                    continue
                if gram[j].endswith(".") or gram[j].endswith(","):
                    skip_flag = True
            if skip_flag:
                continue
            mention = ''.join(w + ' ' for w in gram).strip()
            mention = ''.join(ch for ch in mention if ch not in PUNCTUATION)
            if "''" in mention:
                splitted_list = mention.split("''")
                mention = ''.join(w + '"' for w in splitted_list)
                mention = mention[:-1]
            if "'" in mention:
                splitted_list = mention.split("'")
                mention = ''.join(w + "''" for w in splitted_list)
                mention = mention[:-2]
            mention = to_utf8(mention)
            # entries = relevant_anchor_table.select_from_table(Alias=mention)
            # for entry in entries:
            #     spots.append((entry[0], entry[1], entry[2], entry[3]))
            grams_list.append(mention)
        entries = no_dup_anchor_table.select_batch_from_table(grams_list)
        for entry in entries:
            spots.append((entry[0], entry[1], entry[2]))
    all_spots = pd.DataFrame(spots, columns=["Link", "Title", "Alias"])
    text.close()
    no_dup_anchor_table.close_connection()
    return all_spots


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser(description="Provide path of input data and name of your desired csv file")
    parser.add_argument("input_file", help="your input file")
    parser.add_argument("output_csv_file",help="your output csv file")
    args = parser.parse_args()
    input_file = args.input_file
    output_csv_file = args.output_csv_file
    df = get_all_spots(input_file)
    csv_file = open(output_csv_file,'w',encoding='utf-8')
    df.to_csv(csv_file, encoding='utf-8')
    csv_file.close()
    print("finished in {} minutes".format(str((time.time()-start)/60)))




