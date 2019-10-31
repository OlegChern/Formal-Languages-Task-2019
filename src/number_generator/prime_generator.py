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
    resource_folder = '../../resources/grammars/'

    rules, sigma = read_cs_grammar(resource_folder + "cs-grammar.txt")
    # rules, sigma = read_free_grammar(resource_folder + "free-grammar.txt")
    gen = generator_for_free_grammar(rules, 'A1','A2', sigma)

    for i in range(20):
        print(len(gen.__next__()))


if __name__ == '__main__':
    main()
