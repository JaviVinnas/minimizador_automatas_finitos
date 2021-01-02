from automata import Automata
import json

def init_variables():
    '''Se inicializan variables de utilidad para el menú'''
    automatas = json.load(json_file)
    id_automata = {}
    letra = 'a'
    salir = False
    automata = None

def main():
    with open('automata.json') as json_file:
        #inicializamos variables de utilidad
        automatas = json.load(json_file)
        id_automata = {}
        letra = 'a'
        salir = False
        automata = None
        #fin de la inicialización
        while not salir:
            if automata == None:
                id_automata = {}
                letra = 'a'
                print('Se han encontrado los siguientes autómatas:')
                for automata_def in automatas.items():
                    id_automata[letra] = automata_def[1]
                    print(letra + ') ' + automata_def[0])
                    letra = chr(ord(letra) + 1)
                opcion = input("Escoge tu autómata: ")
                if id_automata.get(opcion, None) != None:
                    automata = Automata(set(id_automata[opcion]['alfabeto'.upper()]), id_automata[opcion]['estados'.upper()])
                    print('Autómata ' + opcion + ' cargado correctamente')
                else:
                    print('> ERROR, no hay ningún autómata de nº ' + opcion)


if __name__ == '__main__':
    main()
