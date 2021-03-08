import re

inverted_index = {}


def read_inverted_index():
    print("Reading inverted index...")
    with open('../data/inverted_terms.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            ws = line.split(':')
            term = ws[0]
            inverted_index[term] = []
            term_value = ws[1].split(',')
            for doc in term_value:
                inverted_index[term].append(doc.split('/')[0])


def boolean_search(query):
    print("Querying...")

    words = re.split(" +(AND|OR) +", query)
    result_set = set(inverted_index[words[0]])
    operation = None

    for word in words:

        inverted = False  # for "NOT word" operations

        if word in ['AND', 'OR']:
            operation = word
            continue

        if word.find('NOT ') == 0:
            if operation == 'OR':
                continue

            inverted = True
            realword = word[4:]
        else:
            realword = word

        if operation is not None:
            current_set = set(inverted_index[realword])

            if operation == 'AND':
                if inverted is True:
                    result_set -= current_set
                else:
                    result_set &= current_set
            elif operation == 'OR':
                result_set |= current_set

        operation = None

    return result_set


if __name__ == "__main__":
    read_inverted_index()
    print(boolean_search("fortune OR fortify AND NOT forteana"))
