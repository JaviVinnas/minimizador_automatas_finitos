from automata import Automata
import json


def main():
    with open('automata.json') as json_file:
        # inicializamos variables de utilidad
        automatas = json.load(json_file)
        id_automata = {}
        letra = 'a'
        salir = False
        automata = None
        opcion = None
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
                opcion = input("Escoge tu autómata o 'S' para salir: ")
                if id_automata.get(opcion, None) != None:
                    automata = Automata(set(
                        id_automata[opcion]['alfabeto'.upper()]), id_automata[opcion]['estados'.upper()])
                    print('Autómata ' + opcion + ' cargado correctamente')
                elif opcion == 'S':
                    salir = True
                else:
                    print('> ERROR, no hay ningún autómata de nº ' + opcion)
            else:
                print('__MENÚ_DEL_AUTÓMATA_[' + opcion.upper() + ']__')
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
                    opcion = input('Escoge una opción: ')
                    if opcion in ['a', 'c', 'S'] if automata.es_determinista() else ['a', 'b', 'c', 'S']:
                        print('>>>>>>>>>>>>')
                        if opcion == 'a':
                            # imprimir por pantalla el autómata
                            print(automata)
                        if opcion == 'b':
                            # queremos determinizar el autómata
                            print("Transformaremos el AFN en un AFD")
                            automata_determinista = automata.transformar_determinista()
                            print("Autómata determinista equivalente:")
                            print(automata_determinista)
                        if opcion == 'c':
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
                            print("Minimizamos el autómata obtenido:")
                            #TODO: hacer esta opción y arreglar el tostring de los estados
                        if opcion == 'S':
                            # queremos salir
                            automata = None
                    else:
                        print(opcion + ' no es una opción válida')
                else:
                    # tiene errores
                    print('El autómata tiene los siguientes errores:')
                    for error in automata.es_valido():
                        print('\t> ' + error)
                    print('Corrígelos en el archivo de definición ' + marca_negrita + 'automata.json' + marca_fin_negrita)
                    automata = None
            print('--------------------------------------------------------------------')


if __name__ == '__main__':
    main()
