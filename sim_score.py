import math
import re
from collections import Counter

WORD = re.compile(r"\w+") # This line compiles a regular expression pattern \w+ using the re.compile() function.
                          # This pattern will be used later to extract words from text strings

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection]) # This line calculates the numerator of the cosine 
                                                               # similarity formula by summing the product of corresponding values of vec1 
                                                               # and vec2 for keys in the intersection.

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())]) # calculates the sum of squares of all values in vec1
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())]) # calculates the sum of squares of all values in vec2
    denominator = math.sqrt(sum1) * math.sqrt(sum2) # calculates the sum of squares of all values in vec2.

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text) # This line uses the previously compiled regular expression pattern WORD to 
                               # find all words in the given text and stores them in the words variable.
    return Counter(words)


text1 = "dark red"
text2 = "blood red "

vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)

cosine = get_cosine(vector1, vector2)

print("Cosine:", cosine)


# wtf does this code do??
# Text Preprocessing: text in each document is preprocessed to extract words. This is done using a regular expression pattern that matches word characters (\w+).
#The text_to_vector function converts each text document into a vector representation, where the keys are the words and the values are the frequencies of those words in the document. 
# which is done using the Counter class from the collections module.

#Cosine Similarity : The get_cosine function takes two vectors representing the documents and calculates the cosine similarity between them. Cosine similarity is a measure of 
#similarity between two non-zero vectors of an inner product space. so the cosine of the angle between the two vectors. so here, it's calculated as the dot product of 
#the two vectors divided by the product of their magnitudes . the numerator of the cosine similarity equation represents the sum of the products of corresponding elements
#of the two vectors, while the denominator represents the product of the magnitudes of the two vectors.

#basically code compares the similarity between two text documents based on the frequency of words they contain. The cosine similarity value ranges from -1 to 1
# where 0 indicates no similarity and 1 indicates identical documents.
