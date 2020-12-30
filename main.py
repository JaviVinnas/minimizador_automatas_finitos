from automata import Automata
import json
#from automata_v1 import AutomataV1


def main():
    with open('automata.json') as json_file:

        dict_definicion = json.load(json_file)
        '''
        automata = AutomataV1(**dict_definicion)
        print(automata)
        print(automata.es_determinista())
        automata.transformar_determinista()
        '''
        automata = Automata(set(dict_definicion['alfabeto'.upper()]), dict_definicion['estados'.upper()])
        print(automata)


if __name__ == '__main__':
    main()
