from automata import Automata
import json
#from automata_v1 import AutomataV1


def main():
    with open('automata.json') as json_file:

        dict_definicion = json.load(json_file)
        automata = Automata(set(dict_definicion['alfabeto'.upper()]), dict_definicion['estados'.upper()])
        print(automata.transformar_determinista())


if __name__ == '__main__':
    main()
