from automata import Automata
import json


def main():
    with open('automata.json') as json_file:

        automatas = json.load(json_file)
        print('Se han encontrado los siguientes autómatas:')
        for nombre_automata in automatas.keys():
            print(nombre_automata)


        #automata = Automata(set(automata_dict['alfabeto'.upper()]), automata_dict['estados'.upper()])
        #print(automata.transformar_determinista())
        #print(automata.transformar_determinista().minimizar())


if __name__ == '__main__':
    main()
