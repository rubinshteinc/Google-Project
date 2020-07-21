from collections import defaultdict


def initialized_data():

   data = defaultdict(set)
   
   data_file = open("about.txt")
   data_sentences = data_file.read().split("\n")

   for sentence in data_sentences:
      
      if sentence:
         first_word = sentence.split()[0]
         substrings = [first_word[i: j] for i in range(len(first_word)) for j in range(i + 1, len(first_word) + 1)]
         
         for string in substrings:
            data[string].add(sentence)
         

initialized_data()



