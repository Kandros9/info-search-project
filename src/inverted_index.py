from src.crawler import get_doc_text, read_doc, get_doc_num
from src.preprocessing import get_num_files, tokenize, lemmatize, lemmatize_with_frequency
from collections import OrderedDict

terms = {}
terms_full = {}


def read_terms():
    print("Reading terms...")
    with open('../data/lemmas.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            ws = line.split(' ')
            term = ws[0]
            terms[term] = []
            terms_full[term] = ws[:-1]


def sort_terms():
    sorted_terms = OrderedDict(sorted(terms.items()))
    return sorted_terms


def get_all_inverted_index():
    num_files = get_num_files('../pages')

    for i in range(1, num_files + 1):
        text = get_doc_text(read_doc(i))
        print("Creating inverted index for " + str(i))
        create_inverted_index_for_doc(text, get_doc_num(i))


def create_inverted_index_for_doc(text, doc_num):
    tokens = tokenize(text)
    lemmas, lemmas_frequency = lemmatize_with_frequency(tokens)
    for lemma in lemmas:
        terms[lemma].append(doc_num + '/' + str(lemmas_frequency[lemma]))


def write_inverted_index():
    print("Writing to inverted_terms.txt...")
    with open('../data/inverted_terms.txt', 'w', encoding='utf-8') as file:
        for key in terms:
            file.write(key + ':' + ','.join(terms[key]) + '\n')


if __name__ == "__main__":
    read_terms()
    terms = sort_terms()
    get_all_inverted_index()
    write_inverted_index()
