import argparse
from itertools import product

from cs_grammar_generator import parse_automaton


def generate_rules(sigma, gamma, delta, init_state, accept_state):
    rules = []
    rules += [('A1', '[,_]{q0}A2[,_][,_]'.format(q0=init_state))]
    rules += [('A2', '[{a},{a}]A2'.format(a=a)) for a in sigma]  # 2 из Мартыненко
    rules += [('A2', '')]

    gamma = gamma
    t_sigma = sigma + ['']
    for a in t_sigma:
        for left, rights in delta.items():
            q, c = left
            for right in rights:
                p, d, m = right
                if m == '>':  # 6
                    l_rule = '{q}[{a},{C}]'.format(q=q, a=a, C=c)
                    r_rule = '[{a},{D}]{p}'.format(a=a, D=d, p=p)
                    rules.append((l_rule, r_rule))
                else:  # 7
                    for b, e in product(t_sigma, gamma):
                        l_rule = '[{b},{E}]{q}[{a},{C}]'.format(b=b, E=e, q=q, a=a, C=c)
                        r_rule = '{p}[{b},{E}][{a},{D}]'.format(p=p, a=a, D=d, b=b, E=e)
                        rules.append((l_rule, r_rule))

    for a, c in product(sigma, gamma):  # 8
        rules.append(('[{a},{C}]{q}'.format(a=a, C=c, q=accept_state), '{q}{a}'.format(q=accept_state, a=a)))
        rules.append(('{q}[{a},{C}]'.format(q=accept_state, a=a, C=c), '{q}{a}{q}'.format(q=accept_state, a=a)))

    for c in gamma:
        rules.append(('[,{C}]{q}'.format(C=c, q=accept_state), accept_state))
        rules.append(('{q}[,{C}]'.format(C=c, q=accept_state), accept_state))

    rules.append(('{q}'.format(q=accept_state), ''))

    return rules


def save_grammar(dest_file, rules, sigma):
    with open(dest_file, 'w') as grammar:
        s = ''
        for a in sigma:
            s += a + ' '
        s += '\n'
        grammar.write(s)
        lines = ["{l} -> {r}\n".format(l=left, r=right) for left, right in rules]
        grammar.writelines(lines)


def optimize_grammar(rules):
    size = 60
    stg1 = 3
    active = set()
    tmp = set()
    q = ["A1"]
    stage2 = []
    while len(q):
        word = q.pop(0)
        if word not in tmp:
            tmp.add(word)
            if word not in ["A1", "A2"]:
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
    parser = argparse.ArgumentParser("free_grammar_generator")
    parser.add_argument("--automaton_path", help="Path to lba file", type=str)
    parser.add_argument("--grammar_path", help="Specifies where to save generated grammar",
                        type=str, nargs='?', default="resources/grammars/free-grammar.txt")
    args = parser.parse_args()

    sigma, gamma, delta, init_state, accept_state = parse_automaton(args.automaton_path)
    gamma += sigma

    rules = generate_rules(sigma, gamma, delta, init_state, accept_state)
    rules = optimize_grammar(rules)

    save_grammar(args.grammar_path, rules, sigma)


if __name__ == '__main__':
    main()
