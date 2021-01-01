from automata import Automata
import json


def main():
    with open('automata.json') as json_file:

        dict_definicion = json.load(json_file)
        automata = Automata(set(dict_definicion['alfabeto'.upper()]), dict_definicion['estados'.upper()])
        print(automata.transformar_determinista())
        print(automata.transformar_determinista().minimizar())


if __name__ == '__main__':
    main()
