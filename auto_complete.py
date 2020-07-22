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
        self.score -= sub_score

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
            first_word = sentence.split()[0]         
            first_word = sentence.split()[0]         

            for i in range(len(first_word)):     
                for j in range(i + 1, len(first_word) + 1):        
                    new_ = AutoCompleteData(sentence, filename, offset, 2*len(first_word[i: j]))
                    data[first_word[i: j]].add(offset) 
        list_data_sentences.append(new_)
        offset += 1
      

#   changed_prefix = []

#     for i in range(len(prefix)):
#         for ch in range(ord('a'), ord('z')+1):
#             string_to_search = data.get(prefix.replace(prefix[i], ch, 1))
#             if str:
#                 strdef change_prefix(prefix):
#   ing_to_search.set_score(2+(1 if i > 3 else 5 - i))
#                 changed_prefix.append(string_to_search)
#     return changed_prefix

# def erase_prefix(prefix):
#     erased_prefix = []

#     for i in range(len(prefix)):
#         strings_to_search = [list_data_sentences[str] for str in data.get(prefix.replace(prefix[i], "", 1))]
#         if string_to_search:
#             for str in strings_to_search:
#                 string_to_search.set_score(2+(2 if i > 3 else 10 - 2*i)),
#                 erased_prefix.append(string_to_search)
#     return erased_prefix

# def add_prefix(prefix):
#     added_prefix = []

#     for i in range(len(prefix)):
#         for ch in range(ord('a'), ord('z')+1):
#             string_to_search = data.get(prefix[:i+1] + ch + prefix[i+1:])
#             if str:
#                 string_to_search.set_score(2+(1 if i > 3 else 5 - i))
#                 added_prefix.append(string_to_search)
#     return add_prefix


# def complete_prefix(prefix):
#     completed_prefix = []
#     # completed_prefix = change_prefix(prefix)
#     completed_prefix += erase_prefix(prefix)
#     # completed_prefix += add_prefix(prefix)
#     return completed_prefix




def get_best_k_completions(prefix):

    k = 5
    found_completions = []
    found_completions = [list_data_sentences[item] for item in data.get(prefix)]

    if(len(found_completions) < k):
        found_completions += complete_prefix(prefix)

    found_completions = sorted(found_completions, key=lambda x: (x.get_score(), x.get_completed_sentence()))
    return found_completions[:k]


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


b = get_best_k_completions("ou")
for complete in b:
    print(f"sentence: {complete.get_completed_sentence()} offset: {complete.get_offset()} score:  {complete.get_score()}")