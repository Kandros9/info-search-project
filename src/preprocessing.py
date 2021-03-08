import os
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from src.crawler import read_doc, get_doc_text
import re

stop_words = set(stopwords.words("english"))


def get_num_files(path):
    return sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def get_texts():
    texts = ''
    for i in range(1, num_files + 1):
        texts += get_doc_text(read_doc(i))
        print("Read doc " + str(i))
    return texts


def tokenize(texts):
    # print("Tokenization...")
    # words = nltk.word_tokenize(texts)
    # print("Removing stop words...")
    # without_stop_words = [word for word in words if not word.lower() in stop_words
    #                       and word not in string.punctuation
    #                       and not has_numbers(word)]
    # return without_stop_words
    print("Tokenization...")
    words = re.findall(r'\w+', texts)
    print("Removing stop words...")
    without_stop_words = [word.lower() for word in words if not word.lower() in stop_words
                          and not has_numbers(word)
                          and is_english(word)
                          and len(word) > 1]
    return without_stop_words


def write_tokens(token_list):
    print("Writing to tokens.txt...")
    with open('data/tokens.txt', 'w', encoding='utf-8') as file:
        file.writelines('\n'.join(token_list))


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def lemmatize(words):
    print("Lemmatization...")
    lemmatizer = nltk.WordNetLemmatizer()
    lemmas = dict()
    for word in words:
        lemma = lemmatizer.lemmatize(word, get_wordnet_pos(word))
        if lemma in lemmas:
            if word not in lemmas[lemma] and word != lemma:
                lemmas[lemma].append(word)
        else:
            lemmas[lemma] = [word] if word != lemma else []
    return lemmas


def write_lemmas(lemma_list):
    print("Writing to lemmas.txt...")
    with open('data/lemmas.txt', 'w', encoding='utf-8') as file:
        for key in lemma_list:
            file.write(key + ' ' + ' '.join(lemma_list[key]) + '\n')


num_files = get_num_files('./pages')
tokens = tokenize(get_texts())
write_tokens(tokens)
lemmas = lemmatize(tokens)
write_lemmas(lemmas)
