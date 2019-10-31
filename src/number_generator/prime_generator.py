import argparse
from collections import deque


def generator_for_free_grammar(rules, init_symbol_1, init_symbol_2, sigma):
    q = deque([init_symbol_1])
    st = set()
    while len(q):
        word = q.popleft()
        if word not in st:
            st.add(word)
            if all(c in sigma for c in word):
                yield word
            else:
                for left, right in rules:
                    if left in word:
                        new_word = word.replace(left, right)
                        if any(S in new_word for S in [init_symbol_1, init_symbol_2]):
                            q.append(new_word)
                        else:
                            q.appendleft(new_word)


def generator_for_cs_grammar(rules_list, initial_symbol, sigma):
    st = set()
    queue = deque()
    queue.append(initial_symbol)

    while len(queue):
        word = queue.popleft()
        for left, right in rules_list:
            if left in word:
                tmp = word.replace(left, right)
                if tmp not in st:
                    queue.append(tmp)
                    st.add(tmp)

        if all(c in sigma for c in word):
            yield word


def read_cs_grammar(file):
    with open(file) as grammar:
        str_rules = list(map(str.strip, grammar.readlines()))
        sigma = str_rules[0].split()
        rules = [tuple(line.split(" -> ")) for line in str_rules[1:]]
    return rules, sigma


def read_free_grammar(file):
    with open(file) as grammar:
        str_rules = [line.strip('\n') for line in grammar.readlines()]
        sigma = str_rules[0].strip().split()
        rules = []
        for line in str_rules[1:]:
            line = line.split(' -> ')
            rules += [tuple(line)] if len(line) > 1 else [(line[0], '')]
    return rules, sigma


def main():
    parser = argparse.ArgumentParser("Prime Numbers Generator")
    parser.add_argument("-p", "--grammar_path", help="Specifies where to save generated grammar",
                        type=str)
    parser.add_argument("-t", "--grammar_type", help="Type of a given grammar (cs/f)", type=str)
    parser.add_argument("-n", help="Amount of required numbers", nargs="?", default=10, type=int)
    args = parser.parse_args()

    if args.grammar_type == "f":
        rules, sigma = read_free_grammar(args.grammar_path)
        gen = generator_for_free_grammar(rules, 'A1', 'A2', sigma)
    elif args.grammar_type == "cs":
        rules, sigma = read_free_grammar(args.grammar_path)
        gen = generator_for_cs_grammar(rules, 'A1', sigma)

    for i in range(args.n):
        print(len(gen.__next__()))


if __name__ == '__main__':
    main()
