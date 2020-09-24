from copy import deepcopy
from .load import data, list_data_sentences
from ..utils.ignore_casing import ignore_casing


class AutoComplete:
    def __init__(self, prefix):
        self.found_completions = {}
        self.prefix = ignore_casing(prefix)
        self.len_prefix = len(self.prefix)

    def get_found_completion(self):
        return self.found_completions

    def get_prefix(self):
        return self.prefix

    def update_founded_completions(self, obj):
        search_obj = self.found_completions.get(obj.get_completed_sentence())

        if search_obj:
            if obj.get_score() > search_obj.get_score():
                search_obj.set_score(obj.get_score())
        else:
            self.found_completions[obj.get_completed_sentence()] = obj

    def sort(self):
        self.found_completions = {k: v for k, v in
                                  sorted(self.found_completions.items(), key=lambda item: item[1].get_score(),
                                         reverse=True)}

    def change_prefix(self):
        for i in range(self.len_prefix):
            for ch in range(ord('a'), ord('z') + 1):
                if chr(ch) not in self.prefix:
                    strings_to_search = data.get(self.prefix.replace(self.prefix[i], chr(ch), 1))

                    if strings_to_search:
                        for str in strings_to_search:
                            changed = deepcopy(list_data_sentences[str])
                            changed.set_score(2 * (self.len_prefix - 1) - (1 if i > 3 else 5 - i))
                            self.update_founded_completions(changed)

    def add_prefix(self):
        for i in range(self.len_prefix):
            strings_to_search = data.get(self.prefix.replace(self.prefix[i], "", 1))

            if strings_to_search:
                for str in strings_to_search:
                    added = deepcopy(list_data_sentences[str])
                    added.set_score(2 * (self.len_prefix - 1) - (2 if i > 3 else 10 - 2 * i))
                    self.update_founded_completions(added)

    def erase_prefix(self):
        for i in range(self.len_prefix):
            for ch in range(ord('a'), ord('z') + 1):
                if chr(ch) not in self.prefix:
                    strings_to_search = data.get(self.prefix[:i] + chr(ch) + self.prefix[i:])

                    if strings_to_search:
                        for str in strings_to_search:
                            erased = deepcopy(list_data_sentences[str])
                            erased.set_score(2 * (self.len_prefix) - (2 if i > 3 else 10 - 2 * i))
                            self.update_founded_completions(erased)

    def complete_prefix(self):
        self.change_prefix()
        self.erase_prefix()
        self.add_prefix()
        self.sort()


def get_best_k_completions(prefix):
    k = 5
    completion = AutoComplete(prefix)

    if data.get(prefix):
        for item in data.get(prefix):
            complete = list_data_sentences[item]
            complete.set_score(2 * len(prefix))
            completion.update_founded_completions(complete)

    if len(completion.get_found_completion()) < k:
        completion.complete_prefix()
    completion_list = [value for value in completion.get_found_completion().values()]

    return completion_list[:k]
