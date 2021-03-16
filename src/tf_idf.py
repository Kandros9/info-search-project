import math
from src.crawler import get_doc_text, read_doc, get_doc_num
from src.preprocessing import tokenize, get_num_files

inverted_terms = {}
tf = {}
idf = {}
tf_idf = {}
doc_terms_count = {}

num_files = 0


def read_inverted_terms():
    print("Reading inverted terms...")
    with open('../data/inverted_terms.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            ws = line.split(':')
            term = ws[0]
            inverted_terms[term] = ws[1].split(',')


def get_doc_term_count():
    print("Writing to doc_term_count.txt...")
    with open('../data/doc_term_count.txt', 'w', encoding='utf-8') as file:
        for i in range(1, num_files + 1):
            doc_text = get_doc_text(read_doc(int(i)))
            tokens = tokenize(doc_text)
            doc_terms_count[get_doc_num(i)] = len(tokens)
            file.write(str(i) + ':' + str(len(tokens)) + '\n')


def read_doc_term_count():
    print("Reading doc_term_count...")
    with open('../data/doc_term_count.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            ws = line.split(':')
            doc_terms_count[ws[0]] = int(ws[1])


def get_term_index(term):
    docs = inverted_terms[term]
    mapped_docs = []
    for str_doc in docs:
        doc = str_doc.split('/')
        if doc[0] != '\n':
            term_doc_count = int(doc[1].split('\n')[0])
        else:
            continue
        mapped_docs.append((doc[0], term_doc_count))

    return mapped_docs


def get_tf_index(term):
    mapped_docs = []
    if term in tf:
        docs = tf[term]
        for str_doc in docs:
            doc = str_doc.split('/')
            if doc[0] != '\n':
                tf_value = float(doc[1].split('\n')[0])
            else:
                continue
            mapped_docs.append((doc[0], tf_value))

    return mapped_docs


def calc_tf(term, doc):
    doc_count = doc_terms_count[doc[0].strip("0")]
    if term not in tf:
        tf[term] = []
    tf[term].append(doc[0] + '/' + '{0:.10f}'.format(doc[1] / doc_count))


def calc_tf_term_doc_all(term):
    term_index = get_term_index(term)
    for doc in term_index:
        calc_tf(term, doc)


def calc_tf_terms_all():
    for term in inverted_terms:
        calc_tf_term_doc_all(term)


def write_tf():
    print("Writing to tf.txt...")
    with open('../data/tf.txt', 'w', encoding='utf-8') as file:
        for key in tf:
            file.write(key + ':' + ','.join(tf[key]) + '\n')


def calc_idf():
    for term in inverted_terms:
        index = get_term_index(term)
        if len(index) > 0:
            idf[term] = math.log(num_files / len(get_term_index(term)), 10)


def write_idf():
    print("Writing to idf.txt...")
    with open('../data/idf.txt', 'w', encoding='utf-8') as file:
        for key in idf:
            file.write(key + ':' + str(idf[key]) + '\n')


def calc_tf_idf():
    for term in inverted_terms:
        term_index = get_tf_index(term)
        for doc in term_index:
            if term not in tf_idf:
                tf_idf[term] = []
            tf_idf[term].append(doc[0] + '/' + '{0:.10f}'.format(float(doc[1]) * float(idf[term])))


def write_tf_idf():
    print("Writing to tf_idf.txt...")
    with open('../data/tf_idf.txt', 'w', encoding='utf-8') as file:
        for key in tf_idf:
            file.write(key + ':' + ','.join(tf_idf[key]) + '\n')


if __name__ == "__main__":
    num_files = get_num_files('../pages')
    read_doc_term_count()
    read_inverted_terms()
    calc_tf_terms_all()
    write_tf()
    calc_idf()
    write_idf()
    calc_tf_idf()
    write_tf_idf()
