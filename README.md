# Formal-Languages-Task-2019
Генератор контекстно-зависимой грамматики по линейно-ограниченному автомату: src/grammar/cs_grammar_generator.py

Использование: CS Grammar Generator [-h] [-a AUTOMATON_PATH] [-g [GRAMMAR_PATH]]

optional arguments:
  -h, --help            вывод помощи

  -a AUTOMATON_PATH, --automaton_path AUTOMATON_PATH
                        путь к файлу с LBA

  -g [GRAMMAR_PATH], --grammar_path [GRAMMAR_PATH]
                        путь для сохранения грамматики

Файл с LBA: resources/grammars/lba.txt



Генератор свободной грамматики по машине Тьюринга: src/grammar/free_grammar_generator.py

Использование: Free grammar Generator [-h] [-a AUTOMATON_PATH] [-g [GRAMMAR_PATH]]

optional arguments:
  -h, --help            вывод помощи

  -a AUTOMATON_PATH, --automaton_path AUTOMATON_PATH
                        путь к машине Тьюринга

  -g [GRAMMAR_PATH], --grammar_path [GRAMMAR_PATH]
                        путь для сохранения грамматики

Файл с МТ: resources/grammars/mt.txt



Генератор простых чисел по грамматике: src/number_generator/prime_generator.py

Использование: Prime Numbers Generator [-h] [-p GRAMMAR_PATH] [-t GRAMMAR_TYPE]
                               [-n [N]]
optional arguments:
  -h, --help            вывод помощи

  -p GRAMMAR_PATH, --grammar_path GRAMMAR_PATH
                        путь к грамматике

  -t GRAMMAR_TYPE, --grammar_type GRAMMAR_TYPE
                        тип грамматики (cs либо f)

  -n [N]                количество выводимых чисел




