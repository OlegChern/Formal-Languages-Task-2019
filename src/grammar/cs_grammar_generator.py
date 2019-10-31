from itertools import product
from collections import deque
from sys import path
import re


def parse_automaton(file):
    with open(file) as automaton:
        init_state = automaton.readline().replace("init: ", "").strip()
        accept_state = automaton.readline().replace("accept: ", "").strip()

        sigma = automaton.readline().replace("sigma: {", "").replace("}", "").strip().split(", ")
        gamma = automaton.readline().replace("gamma: {", "").replace("}", "").strip().split(", ")

        lines = list(filter(lambda s: s != '\n', automaton.readlines()))
        lines = list(map(lambda s: s.strip().split(","), lines))

        delta = {}
        left = map(tuple, lines[::2])
        right = map(tuple, lines[1::2])
        for l, r in zip(left, right):
            if l in delta.keys():
                delta[l] += [r]
            else:
                delta.update({l: [r]})

        return sigma, gamma, delta, init_state, accept_state


# 1 из Мартыненко
def init_config_single(sigma, init_state, init_symbol):
    return [(init_symbol, f'[{init_state},$,{a},{a},#]') for a in sigma]


# 2.1 - 2.4 из Мартыненко
def movement_config_single(sigma, gamma, delta, accept_state):
    rules = []
    for a in sigma:
        for left, rights in delta.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if y == '$' and x == '$' and d == '>':
                        for g in gamma:
                            l_rule = f'[{q},$,{x},{a},#]'
                            r_rule = f'[$,{p},{x},{a},#]'
                            rules.append((l_rule, r_rule))
                    elif y == '#' and x == '#' and d == '<':
                        for g in gamma:
                            l_rule = f'[$,{g},{a},{q},#]'
                            r_rule = f'[$,{p},{g},{a},#]'
                            rules.append((l_rule, r_rule))
                    elif d == '<':
                        l_rule = f'[$,{q},{x},{a},#]'
                        r_rule = f'[{p},$,{y},{a},#]'
                        rules.append((l_rule, r_rule))
                    elif d == '>':
                        l_rule = f'[$,{q},{x},{a},#]'
                        r_rule = f'[$,{y},{a},{p},#]'
                        rules.append((l_rule, r_rule))

    return rules


# 3.1 - 3.3 из Мартыненко
def restore_word_accept(sigma, gamma, accept_state):
    rules = []
    for a in sigma:
        for g in gamma:
            rules.append((f'[{accept_state},$,{g},{a},#]', a))
            rules.append((f'[$,{accept_state},{g},{a},#]', a))
            rules.append((f'[$,{g},{a},{accept_state},#]', a))
    return rules


# 4.1 - 4.3 из Мартыненко
def init_config_general(sigma, init_state, init_symbol_1, init_symbol_2):
    rules = []
    for a in sigma:
        rules.append((init_symbol_1, f'[{init_state},$,{a},{a}]{init_symbol_2}'))
        rules.append((init_symbol_2, f'[{a},{a}]{init_symbol_2}'))
        rules.append((init_symbol_2, f'[{a},{a},#]'))
    return rules


# 5.1 - 5.3 из Мартыненко, 5.4 из презентации Башкирова Александра
def movement_config_left(sigma, gamma, delta, accept_state):
    rules = []
    for a in sigma:
        for left, rights in delta.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if y == '$' and x == '$' and d == '>':
                        for g in gamma:
                            rules.append(
                                ('[{q},$,{X},{a}]'.format(q=q, X=g, a=a), '[$,{p},{X},{a}]'.format(p=p, X=g, a=a)))
                    elif d == '<':
                        rules.append(('[$,{q},{X},{a}]'.format(q=q, X=x, a=a), '[{p},$,{Y},{a}]'.format(p=p, Y=y, a=a)))
                    elif d == '>':
                        for z, b in product(gamma, sigma):
                            l_rule = '[$,{q},{X},{a}][{Z},{b}]'.format(q=q, X=x, a=a, Z=z, b=b)
                            r_rule = '[$,{Y},{a}][{p},{Z},{b}]'.format(p=p, Y=y, a=a, Z=z, b=b)
                            rules.append((l_rule, r_rule))

                            l_rule = '[$,{q},{X},{a}][{Z},{b},#]'.format(q=q, X=x, a=a, Z=z, b=b)
                            r_rule = '[$,{Y},{a}][{p},{Z},{b},#]'.format(p=p, Y=y, a=a, Z=z, b=b)
                            rules.append((l_rule, r_rule))
    return rules


# 6.1 - 6.4 из Мартыненко
def movement_config_center(sigma, gamma, delta, accept_state):
    rules = []
    for a in sigma:
        for left, rights in delta.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if x in gamma and y in gamma:
                        for z, b in product(gamma, sigma):
                            if d == '>':
                                l_rule = f'[{q},{x},{a}][{z},{b}]'
                                r_rule = f'[{y},{a}][{p},{z},{b}]'
                                rules.append((l_rule, r_rule))

                                l_rule = f'[{q},{x},{a}][{z},{b},#]'
                                r_rule = f'[{y},{a}][{p},{z},{b},#]'
                                rules.append((l_rule, r_rule))
                            else:
                                l_rule = f'[{z},{b}][{q},{x},{a}]'
                                r_rule = f'[{p},{z},{b}][{y},{a}]'
                                rules.append((l_rule, r_rule))

                                l_rule = f'[$,{z},{b}][{q},{x},{a}]'
                                r_rule = f'[$,{p},{z},{b}][{y},{a}]'
                                rules.append((l_rule, r_rule))

    return rules


# 7.1 - 7.3, 7.4 из презентации Башкирова Александра
def movement_config_right(sigma, gamma, delta, accept_state):
    rules = []
    for a in sigma:
        for left, rights in delta.items():
            q, x = left
            if q != accept_state:
                for right in rights:
                    p, y, d = right
                    if y == '#' and x == '#' and d == '<':
                        for g in gamma:
                            rules.append(
                                (f'[{g},{a},{q},#]', f'[{p},{g},{a},#]'))
                    elif d == '>':
                        rules.append(
                            (f'[{q},{x},{a},#]', f'[{y},{a},{p},#]'))
                    elif d == '<':
                        for z, b in product(gamma, sigma):
                            l_rule = f'[{z},{b}][{q},{x},{a},#]'
                            r_rule = f'[{p},{z},{b}][{y},{a},#]'
                            rules.append((l_rule, r_rule))

                            l_rule = f'[$,{z},{b}][{q},{x},{a},#]'
                            r_rule = f'[$,{p},{z},{b}][{y},{a},#]'
                            rules.append((l_rule, r_rule))
    return rules


# 8.1 - 8.5
def restore_word_accepted(sigma, gamma, accept_state):
    rules = []
    for x, a in product(gamma, sigma):
        rules.append((f'[{accept_state},$,{x},{a}]', a))
        rules.append((f'[$,{accept_state},{x},{a}]', a))
        rules.append((f'[{accept_state},{x},{a}]', a))
        rules.append((f'[{accept_state},{x},{a},#]', a))
        rules.append((f'[{x},{a},{accept_state},#]', a))
    return rules


# 9.1 - 9.4
def restore_word_general(sigma, gamma):
    rules = []
    for x, a, b in product(gamma, sigma, sigma):
        rules.append((f'{a}[{x},{b}]', f'{a}{b}'))
        rules.append((f'{a}[{x},{b},#]', f'{a}{b}'))
        rules.append((f'[{x},{a}]{b}', f'{a}{b}'))
        rules.append((f'[$,{x},{a}]{b}', f'{a}{b}'))
    return rules


def build_cs_grammar(sigma, gamma, delta, init_state, accept_state):
    gamma += sigma
    init_symbol_1 = 'A1'
    init_symbol_2 = 'A2'

    rules = init_config_single(sigma, init_state, init_symbol_1)
    rules += movement_config_single(sigma, gamma, delta, accept_state)
    rules += restore_word_accept(sigma, gamma, accept_state)
    rules += init_config_general(sigma, init_state, init_symbol_1, init_symbol_2)
    rules += movement_config_left(sigma, gamma, delta, accept_state)
    rules += movement_config_center(sigma, gamma, delta, accept_state)
    rules += movement_config_right(sigma, gamma, delta, accept_state)
    rules += restore_word_accepted(sigma, gamma, accept_state)
    rules += restore_word_general(sigma, gamma)

    return rules, init_symbol_1


def weak_optimize_grammar(rules):
    new_rules = rules.copy()
    pattern = re.compile('(\[[\w,#$]*\])')
    for left, right in rules:
        brackets = re.findall(pattern, right)
        for entry in brackets:
            if all(entry not in left for left, _ in rules):
                new_rules = list(filter(lambda x: x[1] != right, new_rules))
        brackets = re.findall(pattern, left)
        for entry in brackets:
            if all(entry not in right for _, right in rules):
                new_rules = list(filter(lambda x: x[0] != left, new_rules))
    return weak_optimize_grammar(new_rules) if new_rules != rules else new_rules


def deep_optimize_grammar(rules, initial_symbol, sigma, steps):
    counter = 0
    st = set()
    used = set()
    queue = deque()
    queue.append(initial_symbol)

    while len(queue):
        word = queue.popleft()
        for left, right in rules:
            if left in word:
                used.add((left, right))
                tmp = word.replace(left, right)
                if tmp not in st:
                    queue.append(tmp)
                    st.add(tmp)

        if all(c in sigma for c in word):
            if counter < steps:
                counter += 1
                continue
            else:
                return list(used)


def optimize_grammar(rules, init_symbol, sigma):
    steps_for_optimization = 3

    rules = weak_optimize_grammar(rules)
    rules = deep_optimize_grammar(rules, init_symbol, sigma, steps_for_optimization)

    return rules


def save_grammar(dest_file, rules, sigma):
    with open(dest_file, 'w') as grammar:
        grammar.write(str(*sigma) + ' $ #\n')
        grammar.writelines(sorted(left + " -> " + right + '\n' for left, right in rules))


def main():
    automata_folder = '../../resources/automata/'
    resource_folder = '../../resources/grammars/'

    sigma, gamma, delta, init_state, accept_state = parse_automaton(automata_folder + 'lba.txt')
    rules, init_symbol = build_cs_grammar(sigma, gamma, delta, init_state, accept_state)

    rules = optimize_grammar(rules, init_symbol, sigma)
    save_grammar(resource_folder + 'cs-grammar.txt', rules, sigma)


if __name__ == '__main__':
    main()
