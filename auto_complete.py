from collections import defaultdict
from copy import deepcopy

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

def prefix_ignore_casing(prefix):
    prefix = " ".join(prefix.split())
    return "".join(filter(lambda x: x.isalnum() or x.isspace(), prefix)).lower()

def initilized_data(filename):
    id_sentence = 0
    data_file = open(filename, encoding="utf8")
    data_sentences = data_file.read().split("\n")
    offset = 0
    for sentence in data_sentences:
    
        if sentence:
            for i in range(len(sentence)):     
                for j in range(i + 1, len(sentence) + 1):        
                    data[prefix_ignore_casing(sentence[i: j])].add(id_sentence) 
            new_data = AutoCompleteData(sentence, filename, offset, 0)
            list_data_sentences.append(new_data)
            id_sentence += 1
        offset += 1


def change_prefix(prefix):
    changed_prefix = set()

    for i in range(len(prefix)):
        for ch in range(ord('a'), ord('z')+1):
            if chr(ch) not in prefix:
                strings_to_search = data.get(prefix.replace(prefix[i], chr(ch), 1))

                if strings_to_search:
                    for str in strings_to_search:
                        changed = deepcopy(list_data_sentences[str])
                        changed.set_score(2*(len(prefix) -1) - (1 if i > 3 else 5 - i))
                        changed_prefix.add(changed)
    return changed_prefix


def add_prefix(prefix):
    added_prefix = set()

    for i in range(len(prefix)):
        strings_to_search = data.get(prefix.replace(prefix[i], "", 1))
        
        if strings_to_search:
            for str in strings_to_search:
                added = deepcopy(list_data_sentences[str])
                added.set_score(2*(len(prefix) -1) - (2 if i > 3 else 10 - 2*i))
                added_prefix.add(added)
    return added_prefix



def erase_prefix(prefix):
    erased_prefix = set()

    for i in range(len(prefix)):
        for ch in range(ord('a'), ord('z')+1):
            if chr(ch) not in prefix:
                strings_to_search = data.get(prefix[:i+1] + chr(ch) + prefix[i:])
                
                if strings_to_search:
                    for str in strings_to_search:
                        erased = deepcopy(list_data_sentences[str])
                        erased.set_score(2*(len(prefix)) - (2 if i > 3 else 10 - 2*i))
                        erased_prefix.add(erased)
    return erased_prefix


def complete_prefix(prefix, num_of_substring):
    completed_prefix = set()
    completed_prefix.update(change_prefix(prefix))
    completed_prefix.update(erase_prefix(prefix))
    completed_prefix.update(add_prefix(prefix))
    return completed_prefix




def get_best_k_completions(prefix):

    k = 5
    found_completions = set()
    if (data.get(prefix)):
        # found_completions.add(list_data_sentences[item].set_score(len(prefix)) for item in data.get(prefix))
        for item in data.get(prefix):
            complete = list_data_sentences[item]  
            complete.set_score(2 * len(prefix)) 
            found_completions.add(complete)

    if len(found_completions) < k:
        found_completions.update(complete_prefix(prefix, k - len(found_completions)))

    found_completions = sorted(found_completions, key=lambda x: (x.get_score(), x.get_completed_sentence()), reverse=True)
    return found_completions[:k]


def menu():

    print("Loading the file and prepraring the system...")
    initilized_data("about.txt")
    print("The system is ready. Enter your text:")
    
    prefix = input()
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
        else:
            print("There are no suggestions")
        prefix += input()


def process():
    menu()




process()




