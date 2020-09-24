import os
import json
import pickle
from my_data_structure import AutoCompleteData, list_data_sentences, data
from utils.encoder import SetEncoder
from utils.ignore_casing import ignore_casing


def get_ID():
    get_ID.id_sentence += 1
    return get_ID.id_sentence


get_ID.id_sentence = -1

def preparing_system():
    path = "../python-3.8.4-docs-text/python-3.8.4-docs-text/installing"
    for root, dirs, files in os.walk(path, topdown=True):

        for file in files:
            data_file = open(root + '/' + file, encoding="utf8")
            data_sentences = data_file.read().split("\n")
            offset = 1

            for sentence in data_sentences:

                if sentence:
                    initialized_data(file, sentence, offset)

                offset += 1

    with open("sub_sentences.json", "w") as f:
        json.dump(data, f, cls=SetEncoder)

    with open('sentences.pkl', 'wb') as sentences:
        pickle.dump(list_data_sentences, sentences)


def initialized_data(file_name, completed_sentence, offset):
    sentence_length = len(completed_sentence)
    id_sentence = get_ID()
    # sub_sentence = ""

    for i in range(sentence_length):

        for j in range(i + 1, sentence_length + 1):
            sub_sentence = data[ignore_casing(completed_sentence[i: j])]

            if (len(sub_sentence)) < 5:
                sub_sentence.add(id_sentence)

    new_data = AutoCompleteData(completed_sentence, file_name, offset, 0)
    list_data_sentences.append(new_data)


if __name__ == "__main__":
    preparing_system()
