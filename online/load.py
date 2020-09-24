import pickle
import json

def load_text_sources():
    print("Loading the file and preparing the system...")

    with open("../offline/sub_sentences.json", "r") as sub_sentences_file:
        sub_sentences = json.load(sub_sentences_file)

    with open("../offline/sentences.pkl", "rb") as sentences_file:
        sentences = pickle.load(sentences_file)

    return sub_sentences, sentences


data, list_data_sentences = load_text_sources()


