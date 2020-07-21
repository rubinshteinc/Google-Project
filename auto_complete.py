from collections import defaultdict

data = defaultdict()

class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def get_score(self):
        return self.score
    
    def get_completed_sentence(self):
        return self.score

    def set_score(self, sub_score):
        self.score -= sub_score

    def get_source_text(self):
        return self.source_text

    def get_offset(self):
        return self.offset



def read_data(filename):
   
   data_file = open(filename)
   data_sentences = data_file.read().split("\n")

   for sentence in data_sentences:
   
      if sentence:
         first_word = sentence.split()[0]         

         for i in range(len(first_word)):
            for j in range(i + 1, len(first_word) + 1):        
                new_ = AutoCompleteData(sentence, filename, 0, 2*len(first_word[i: j]))
                data[first_word[i: j]].add(new_)
      

def change_prefix(prefix):
    changed_prefix = []

    for i in range(len(prefix)):
        for ch in range(ord('a'), ord('z')+1):
            string_to_search = data.get(prefix.replace(prefix[i], ch, 1))
            if str:
                string_to_search.set_score(2+(1 if i > 3 else 5 - i))
                changed_prefix.append(string_to_search)
    return changed_prefix

def erase_prefix(prefix):
    erased_prefix = []

    for i in range(len(prefix)):
        string_to_search = data.get(prefix.replace(prefix[i], "", 1))
        if string_to_search:
            string_to_search.set_score(2+(2 if i > 3 else 10 - 2*i)),
            erased_prefix.append(string_to_search)
    return erased_prefix

def add_prefix(prefix):
    added_prefix = []

    for i in range(len(prefix)):
        for ch in range(ord('a'), ord('z')+1):
            string_to_search = data.get(prefix[:i+1] + ch + prefix[i+1:])
            if str:
                string_to_search.set_score(2+(1 if i > 3 else 5 - i))
                added_prefix.append(string_to_search)
    return add_prefix


def complete_prefix(prefix):
    
    completed_prefix = change_prefix(prefix)
    completed_prefix += erase_prefix(prefix)
    completed_prefix += add_prefix(prefix)
    return completed_prefix




def get_best_k_completions(prefix):

    k = 5
    found_completions = []
    found_completions = list(data.get(prefix))
    

    if(len(found_completions) < k):
        found_completions += complete_prefix(prefix)

    found_completions = sorted(found_completions,  key=lambda x: x.get_score())
    return found_completions[:k]



def menu():
    print("Loading the file and prepraring the system...")
    print("The system is ready. Enter your text:")
    
    while(1):
        substring = input()
        suggestions = get_best_k_completions(substring)
        if suggestions:
            print("Here are 5 suggestions:")
            for suggest in suggestions:
                i = 0
                print(f"{i}. {suggest.get_completed_sentence()} ({suggest.get_offset()} {suggest.get_completed_sentence()})")

        else:
            print("There are no suggestions")




read_data("about.txt")
menu()

