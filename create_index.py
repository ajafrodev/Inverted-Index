import urllib.request
from bs4 import BeautifulSoup
from nltk import tokenize
from nltk.stem import PorterStemmer

urls = []
stop_words = []
ps = PorterStemmer()
inverted_index = {}
pages = 0
with open('sample_urls.txt') as file:
    for line in file:
        urls.append(line.strip())
with open('sample_stopwords.txt') as file:
    for line in file:
        stop_words.append(line.strip())
print(stop_words)
for url in urls:
    with urllib.request.urlopen(url) as response:
        words = BeautifulSoup(response.read(), "html.parser").get_text().lower()
        tokenized_words = tokenize.word_tokenize(words)
        for word in tokenized_words:
            if word not in stop_words:
                word_stemmed = ps.stem(word)
                print(word_stemmed)
                if word_stemmed in inverted_index:
                    if pages in inverted_index[word_stemmed]:
                        inverted_index[word_stemmed][pages] += 1
                    else:
                        inverted_index[word_stemmed][pages] = 1
                else:
                    inverted_index[word_stemmed] = {pages: 1}
    pages += 1

while True:
    word = input("Word to retrieve: ")
    if word != 'quit':
        if word in inverted_index:
            for k, v in inverted_index[word].items():
                print(f'({urls[k]}, {v})')
    else:
        break
