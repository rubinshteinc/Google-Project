from collections import defaultdict
import json
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

    def set_score(self, sub_score):
        self.score = sub_score

    def get_source_text(self):
        return self.source_text

    def get_offset(self):
        return self.offset



def read_data(filename):
   
    data_file = open(filename)
    data_sentences = data_file.read().split("\n")
    offset = 0
    for sentence in data_sentences:
    
        if sentence:
            first_word = sentence.split()[0]             

            for i in range(len(first_word)):     
                for j in range(i + 1, len(first_word) + 1):        
                    new_ = AutoCompleteData(sentence, filename, offset, 2*len(first_word[i: j]))
                    data[first_word[i: j]].add(offset) 
        list_data_sentences.append(new_)
        offset += 1
      

def change_prefix(prefix):

    changed_prefix = set()

    for i in range(len(prefix)):
        for ch in range(ord('a'), ord('z')+1):
            strings_to_search = data.get(prefix.replace(prefix[i], chr(ch), 1))

            if strings_to_search:
                for str in strings_to_search:
                    changed = list_data_sentences[str]
                    changed.set_score(2*(len(prefix) -1) - (1 if i > 3 else 5 - i))
                    changed_prefix.add(changed)
    return changed_prefix


def erase_prefix(prefix):
    erased_prefix = set()

    for i in range(len(prefix)):
        strings_to_search = data.get(prefix.replace(prefix[i], "", 1))
        if strings_to_search:
            for str in strings_to_search:
                erased = list_data_sentences[str]
                erased.set_score(2*(len(prefix) -1) - (2 if i > 3 else 10 - 2*i))
                erased_prefix.add(erased)
    return erased_prefix



def add_prefix(prefix):
    added_prefix = set()

    for i in range(len(prefix)):
        for ch in range(ord('a'), ord('z')+1):
            strings_to_search = data.get(prefix[:i+1] + chr(ch) + prefix[i+1:])
            if strings_to_search:
                for str in strings_to_search:
                    added = list_data_sentences[str]
                    added.set_score(2*(len(prefix) -1) - (2 if i > 3 else 10 - 2*i))
                    added_prefix.add(added)
    return add_prefix

def complete_prefix(prefix):
    completed_prefix = set()
    # completed_prefix = change_prefix(prefix)
    completed_prefix.update(erase_prefix(prefix))
    # completed_prefix += add_prefix(prefix)
    return completed_prefix




def get_best_k_completions(prefix):

    k = 5
    found_completions = []
    found_completions = {list_data_sentences[item] for item in data.get(prefix)}

    if len(found_completions) < k:
        # found_completions.update(complete_prefix(prefix))
        complete_prefix(prefix)

    found_completions = sorted(found_completions, key=lambda x: (x.get_score()), reverse=True)
    return found_completions[:k]
# x.get_completed_sentence()

# def menu():
#     print("Loading the file and prepraring the system...")
#     print("The system is ready. Enter your text:")
    
#     while(1):
#         substring = input()
#         suggestions = get_best_k_completions(substring)
#         if suggestions:
#             print("Here are 5 suggestions:")
#             for suggest in suggestions:
#                 i = 0
#                 print(f"{i}. {suggest.get_completed_sentence()} ({suggest.get_offset()} {suggest.get_completed_sentence()})")

#         else:
#             print("There are no suggestions")




read_data("about.txt")
# # menu()

# # for item in data:
# #     print(data[item])

# for item in sentences:
#     print(item.get_completed_sentence())


b = get_best_k_completions("on")
for complete in b:
    print(f"sentence: {complete.get_completed_sentence()} offset: {complete.get_offset()} score:  {complete.get_score()}")