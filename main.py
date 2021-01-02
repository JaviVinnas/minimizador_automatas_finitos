#!/usr/bin/env python3

from automata import Automata
import json


def main():
    with open('automatas.json') as json_file:
        # inicializamos variables de utilidad
        automatas = json.load(json_file)
        id_automata = {}
        letra = 'a'
        salir = False
        automata = None
        opcion_menu_principal = None
        opcion_menu_automata = None
        marca_negrita = '\033[1m'
        marca_fin_negrita = '\033[0m'
        # fin de la inicialización
        while not salir:
            if automata == None:
                id_automata = {}
                letra = 'a'
                print('__MENU_PRINCIPAL__')
                print('Se han encontrado los siguientes autómatas en ' + marca_negrita + 'automatas.json' + marca_fin_negrita + ':')
                for automata_def in automatas.items():
                    id_automata[letra] = automata_def[1]
                    print(letra + ') ' + automata_def[0])
                    letra = chr(ord(letra) + 1)
                opcion_menu_principal = input("Escoge tu autómata o 'S' para salir: ")
                if id_automata.get(opcion_menu_principal, None) != None:
                    automata = Automata(set(
                        id_automata[opcion_menu_principal]['alfabeto'.upper()]), id_automata[opcion_menu_principal]['estados'.upper()])
                    print('Autómata ' + opcion_menu_principal + ' cargado correctamente')
                elif opcion_menu_principal == 'S':
                    salir = True
                else:
                    print('> ERROR, no hay ningún autómata de nº ' + opcion_menu_principal)
            else:
                print('__MENÚ_DEL_AUTÓMATA_[' + opcion_menu_principal.upper() + ']__')
                # automata sin errores
                if len(automata.es_valido()) == 0:
                    # dividimos si fuera o no determinista
                    print('a) Mostrar por pantalla')
                    if automata.es_determinista():
                        print(
                            '<<b) Transformar a determinista>> -> NO DISPONIBLE (ya es determinista)')
                    else:
                        print('b) Transformar a determinista')
                    print('c) Minimizar')
                    print('S) Salir')
                    opcion_menu_automata = input('Escoge una opción: ')
                    if opcion_menu_automata in ['a', 'c', 'S'] if automata.es_determinista() else ['a', 'b', 'c', 'S']:
                        print('>>>>>>>>>>>>')
                        if opcion_menu_automata == 'a':
                            # imprimir por pantalla el autómata
                            print(automata)
                        if opcion_menu_automata == 'b':
                            # queremos determinizar el autómata
                            print("Transformaremos el AFN en un AFD")
                            automata_determinista = automata.transformar_determinista()
                            print("Autómata determinista equivalente:")
                            print(automata_determinista)
                        if opcion_menu_automata == 'c':
                            # queremos minimizar el automata
                            #si no fuera determinista lo determinizaríamos primero
                            automata_determinista = None
                            if not automata.es_determinista():
                                print('Como el autómata no es determinista primero hay que minimizarlo')
                                automata_determinista = automata.transformar_determinista()
                                print("Autómata determinista equivalente:")
                                print(automata_determinista)
                            else:
                                automata_determinista = automata
                            print("Minimizamos el autómata:")
                            automata_minimizado = automata_determinista.minimizar()
                            print("Autómata determinista mínimo equivalente:")
                            print(automata_minimizado)
                        if opcion_menu_automata == 'S':
                            # queremos salir
                            automata = None
                    else:
                        print(opcion_menu_automata + ' no es una opción válida')
                else:
                    # tiene errores
                    print('El autómata tiene los siguientes errores:')
                    for error in automata.es_valido():
                        print('\t> ' + error)
                    print('Corrígelos en el archivo de definición ' + marca_negrita + 'automatas.json' + marca_fin_negrita)
                    automata = None
            print('--------------------------------------------------------------------')


if __name__ == '__main__':
    main()
