import json
from automata import Automata

def main():
    with open('automata.json') as json_file:
        dict_definicion = json.load(json_file)
        automata = Automata(**dict_definicion)
        print(automata)
        print(automata.es_determinista())
        automata.transformar_determinista()

if __name__ == '__main__':
    main()