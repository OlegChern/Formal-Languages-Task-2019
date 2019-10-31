import argparse
from itertools import product

from cs_grammar_generator import parse_automaton


def generate_rules(sigma, gamma, delta, init_state, accept_state):
    init_symbol_1 = 'A1'
    init_symbol_2 = 'A2'

    rules = []
    rules += [(f'{init_symbol_1}', f'[,_]{init_state}{init_symbol_2}[,_][,_]')]
    rules += [(f'{init_symbol_2}', f'[{a},{a}]{init_symbol_2}') for a in sigma]  # 2 из Мартыненко
    rules += [(f'{init_symbol_2}', '')]

    gamma = gamma
    t_sigma = sigma + ['']
    for a in t_sigma:
        for left, rights in delta.items():
            q, c = left
            for right in rights:
                p, d, m = right
                if m == '>':  # 6
                    l_rule = f'{q}[{a},{c}]'
                    r_rule = f'[{a},{d}]{p}'
                    rules.append((l_rule, r_rule))
                else:  # 7
                    for b, e in product(t_sigma, gamma):
                        l_rule = f'[{b},{e}]{q}[{a},{c}]'
                        r_rule = f'{p}[{b},{e}][{a},{d}]'
                        rules.append((l_rule, r_rule))

    for a, c in product(sigma, gamma):  # 8
        rules.append((f'[{a},{c}]{accept_state}', f'{accept_state}{a}'))
        rules.append((f'{accept_state}[{a},{c}]', f'{accept_state}{a}{accept_state}'))

    for c in gamma:
        rules.append((f'[,{c}]{accept_state}', accept_state))
        rules.append((f'{accept_state}[,{c}]', accept_state))

    rules.append((accept_state, ''))

    return rules, init_symbol_1, init_symbol_2


def save_grammar(dest_file, rules, sigma):
    with open(dest_file, 'w') as grammar:
        s = ''
        for a in sigma:
            s += a + ' '
        s += '\n'
        grammar.write(s)
        lines = [f"{left} -> {right}\n" for left, right in rules]
        grammar.writelines(lines)


def optimize_grammar(rules, init_symbol_1, init_symbol_2):
    size, stg1 = 60, 3
    active, tmp = set(), set()
    q, stage2 = [init_symbol_1], []

    while q:
        word = q.pop(0)
        if word not in tmp:
            tmp.add(word)
            if word not in [init_symbol_1, init_symbol_2]:
                stage2.append(word)
            for left, right in rules[:stg1]:
                if left in word:
                    active.add((left, right))
                    new_word = word.replace(left, right)
                    if len(new_word) <= size:
                        q.append(new_word)

    st = set()
    while len(stage2):
        word = stage2.pop(0)
        if word not in st:
            st.add(word)
            for left, right in rules[stg1:]:
                if left in word:
                    active.add((left, right))
                    new_word = word.replace(left, right)
                    stage2.append(new_word)

    return list(active)


def main():
    parser = argparse.ArgumentParser("Free grammar Generator")
    parser.add_argument("--automaton_path", help="Path to lba file", type=str)
    parser.add_argument("--grammar_path", help="Specifies where to save generated grammar",
                        type=str, nargs='?', default="resources/grammars/free-grammar.txt")
    args = parser.parse_args()

    sigma, gamma, delta, init_state, accept_state = parse_automaton(args.automaton_path)
    gamma += sigma

    rules, init_symbol_1, init_symbol_2 = generate_rules(sigma, gamma, delta, init_state, accept_state)
    rules = optimize_grammar(rules, init_symbol_1, init_symbol_2)

    save_grammar(args.grammar_path, rules, sigma)


if __name__ == '__main__':
    main()
