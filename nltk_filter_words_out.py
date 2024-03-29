from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sent = "his is a sentence with lots of random words. hiii. i love choclate milk. yah." 
stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(example_sent) # tokenizers divide strings into lists of substrings. 
# converts the words in word_tokens to lower case and then checks whether they are present in stop_words or not

filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

print(word_tokens)
print(filtered_sentence)
