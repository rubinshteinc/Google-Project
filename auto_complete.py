from collections import defaultdict
from copy import deepcopy
import time
import os

data = defaultdict(set)
list_data_sentences = []
class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def get_score(self):
        return self.score
    
    def get_completed_sentence(self):
        return self.completed_sentence

    def set_score(self, score):
        self.score = score

    def get_source_text(self):
        return self.source_text

    def get_offset(self):
        return self.offset


class AutoComplete:
    def __init__(self, prefix):
        self.found_completions = {}
        self.prefix = prefix
        self.len_prefix = len(prefix)

    def get_found_completion(self):
        return self.found_completions

    def update_founded_completions(self, obj):
        search_obj = self.found_completions.get(obj.get_completed_sentence())
        if search_obj:
            if obj.get_score() > search_obj.get_score():
                search_obj.set_score(obj.get_score())
        else:
            self.found_completions[obj.get_completed_sentence()] = obj

    def sort(self):
        self.found_completions = {k: v for k, v in sorted(self.found_completions.items(), key=lambda item: item[1].get_score(), reverse=True)}


    def change_prefix(self):
        for i in range(self.len_prefix):
            for ch in range(ord('a'), ord('z')+1):
                if chr(ch) not in self.prefix:
                    strings_to_search = data.get(self.prefix.replace(self.prefix[i], chr(ch), 1))

                    if strings_to_search:
                        for str in strings_to_search:
                            changed = deepcopy(list_data_sentences[str])
                            changed.set_score(2*(self.len_prefix -1) - (1 if i > 3 else 5 - i))
                            self.update_founded_completions(changed)

    def add_prefix(self):
        for i in range(self.len_prefix):
            strings_to_search = data.get(self.prefix.replace(self.prefix[i], "", 1))
            
            if strings_to_search:
                for str in strings_to_search:
                    added = deepcopy(list_data_sentences[str])
                    added.set_score(2*(self.len_prefix -1) - (2 if i > 3 else 10 - 2*i))
                    self.update_founded_completions(added)



    def erase_prefix(self):
        for i in range(self.len_prefix):
            for ch in range(ord('a'), ord('z')+1):
                if chr(ch) not in self.prefix:
                    strings_to_search = data.get(self.prefix[:i] + chr(ch) + self.prefix[i:])
                    
                    if strings_to_search:
                        for str in strings_to_search:
                            erased = deepcopy(list_data_sentences[str])
                            erased.set_score(2*(self.len_prefix) - (2 if i > 3 else 10 - 2*i))
                            self.update_founded_completions(erased)


    def complete_prefix(self):
        self.change_prefix()
        self.erase_prefix()
        self.add_prefix()
        self.sort()



def prefix_ignore_casing(prefix):
    prefix = " ".join(prefix.split())
    return "".join(filter(lambda x: x.isalnum() or x.isspace(), prefix)).lower()

def initilized_data():
    id_sentence = 0

    
    path = "python-3.8.4-docs-text/python-3.8.4-docs-text/library"
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            data_file = open(root + '/' + file, encoding="utf8")
            data_sentences = data_file.read().split("\n")
            offset = 1    
            for sentence in data_sentences:
                
                if sentence:
                    for i in range(len(sentence)):     
                        for j in range(i + 1, len(sentence) + 1):        
                            data[prefix_ignore_casing(sentence[i: j])].add(id_sentence) 
                    new_data = AutoCompleteData(sentence, file, offset, 0)
                    list_data_sentences.append(new_data)
                    id_sentence += 1
                offset += 1
    print(len(data))


def get_best_k_completions(prefix):

    k = 5
    completion = AutoComplete(prefix)
    if (data.get(prefix)):
        for item in data.get(prefix):
            complete = list_data_sentences[item]  
            complete.set_score(2 * len(prefix)) 
            completion.update_founded_completions(complete)

    if len(completion.get_found_completion()) < k:
        completion.complete_prefix()
    completion_list = [value for value in completion.get_found_completion().values()]

    return completion_list[:k]

def menu():

    print("Loading the file and prepraring the system...")
    initilized_data()
    print("The system is ready. Enter your text:")

    prefix = input()
    start_time = time.time()

    while(True):
        if("#" == prefix[-1]):
            prefix = input()
        i = 0
        suggestions = get_best_k_completions(prefix_ignore_casing(prefix))
        num = len(suggestions)
        if suggestions:
            print(f"Here are {num} suggestions:")
            for suggest in suggestions:
                i += 1
                print(f"{i}. {suggest.get_completed_sentence()} ({suggest.get_offset()} {suggest.get_source_text()} {suggest.get_score()})")
            print(prefix, end="")
            print("--- %s seconds ---" % (time.time() - start_time))

        else:
            print("There are no suggestions")
        prefix += input()
        start_time = time.time()



menu()








