from functools import reduce
import json


class ErrorAutomata(Exception):
    '''
    Excepción general para errores dentro del autómata
    '''
    pass


class Estado:
    # declaramos variables para el autocompletado
    def __init__(self):
        self.id = set()
        self.automata = None
        self.inicial = False
        self.final = False
        self.f_transicion = {}

    def clausura(self) -> set:
        pass


class Automata:
    # declaramos variables para el autocompletado
    def __init__(self):
        self.alfabeto = set()
        self.estados_activos = set()
        self.estados = set()

    def get_estado(self, id: set) -> Estado:
        pass

    def es_determinista(self) -> bool:
        pass


class Estado:
    '''Clase que representará cada estado del autómata'''

    def __init__(self, id: set, automata: Automata, inicial: bool = False, final: bool = False, f_transicion: dict = {}):
        '''Cada estado tendrá un ID único que será un set, un autómata padre, su funcion de transición y si es final o inicial'''
        self.id = id
        self.automata = automata
        self.inicial = inicial
        self.final = final
        # construimos la funcion de transicion en base al alfabeto + lambda (cadena vacía)
        self.f_transicion = {}
        inputs_and_lambda = automata.alfabeto.copy()
        inputs_and_lambda.add('lambda'.upper())
        for input_or_lambda in inputs_and_lambda:
            self.f_transicion[input_or_lambda] = set(
                f_transicion.get(input_or_lambda, []))

    def __str__(self):
        out = ''
        out += 'Estado ' + str(sorted(list(self.id))) + '\n'
        if self.inicial:
            out += '\t> estado inicial\n'
        if self.final:
            out += '\t> estado final\n'
        out += '\t> funcion de transicion: '
        for key, value in sorted(self.f_transicion.items(), key=lambda x: x[0]):
            out += "[{} -> {}] ".format(key, value if len(value) > 0 else '{}')
        return out +'\n'

    def __repr__(self):
        return '<Estado' + str(sorted(list(self.id))) + '>'

    def __eq__(self, o: object):
        '''Nos dice si dos estados son iguales'''
        # si no son de la misma clase
        if not isinstance(o, self.__class__):
            return False
        return o.id == self.id

    def __lt__(self, o: object):
        '''
        Nos dice si el objeto self es menor que el objeto o

        En una lista se ordenan menor -> mayor
        '''
        if not isinstance(o, self.__class__):
            return False
        # primero siempre irá el inicial
        if self.inicial != o.inicial:
            return self.inicial
        # ordenaremos por tamaño del set id
        if len(self.id) != len(o.id):
            return len(self.id) < len(o.id)
        else:
            # y si son iguales por el orden de la letra en el abecedario
            self_menor_o = {True: 0, False: 0}
            for letra_id in self.id:
                for letra_id_o in o.id:
                    self_menor_o[letra_id < letra_id_o] += 1
            return self_menor_o[True] > self_menor_o[False]

    def __add__(self, o: object):
        '''Compone dos estados como uno solo'''
        if not isinstance(o, self.__class__):
            raise ErrorAutomata(
                'No se puede sumar un estado con un ' + str(o.__class__))
        # el automata padre debe ser el mismo
        if(o.automata != self.automata):
            raise ErrorAutomata(
                'No se pueden sumar estados de dos autómatas distintos (' + str(self) + ' y ' + str(o) + ')')
        # creamos el id
        id_result = self.id.union(o.id)
        # creamos su automata padre
        automata_result = self.automata
        # creamos si es inicial y/o final
        inicial_result = self.inicial or o.inicial
        final_result = self.final or o.final
        # creamos su función de transición iterativamente
        f_transicion_result = {}
        for letra_alfabeto in self.automata.alfabeto:
            f_transicion_result[str(letra_alfabeto)] = self.f_transicion[str(
                letra_alfabeto)].union(o.f_transicion[str(letra_alfabeto)])
        # para lambda añadimos aquellos estados que no estén en la nueva id del estado compuesto
        f_transicion_result['lambda'.upper()] = set()
        for estado_lambda in self.f_transicion['lambda'.upper()].union(o.f_transicion['lambda'.upper()]):
            if estado_lambda not in id_result:
                f_transicion_result['lambda'.upper()].add(estado_lambda)
        # devolvemos el nuevo estado
        return Estado(id_result, automata_result, inicial_result, final_result, f_transicion_result)

    def __hash__(self):
        '''identificador unico del estado'''
        return hash(str(sorted(list(self.id))))

    def clausura(self):
        '''
        Devuelve un set con él mismo y los estados recursivos por la cadena vacía
        '''
        pila_auxiliar = [self.id]
        # meto la primera generación de estados por la cadena vacia en pilaAuxiliar
        for estado_lambda in self.f_transicion['lambda'.upper()]:
            if estado_lambda not in pila_auxiliar:
                pila_auxiliar.append([estado_lambda])
        # donde guardaremos los estados que obtengamos
        resultado = set()
        # mientra haya cosas en la pila
        while len(pila_auxiliar) > 0:
            # quito el tope de la pila
            estado = self.automata.get_estado(set(pila_auxiliar.pop()))
            # lo añado a los elemntos procesados
            resultado.add(estado)
            # lo añado a la funcion de transición
            ids_clausura = estado.f_transicion['lambda'.upper()]
            # por cada estado de la descendencia
            for id_estado_clausura in ids_clausura:
                # paso de id a estado
                estado_clausura = self.automata.get_estado(
                    set(id_estado_clausura))
                # si no lo procesé lo añado a la pila
                if estado_clausura not in resultado:
                    pila_auxiliar.append(estado_clausura.id)
        # devolvemos el set resultado
        return resultado

    def clausura_compuesta(self):
        '''
        igual que la clausura pero devuelve un estado compuesto
        en lugar de un set con los diversos estados
        '''
        # no es necesario lanzar una excepción ya que como poco la clausura
        # tendrá el mismo estado como mucho
        return reduce(lambda x, y: x + y, self.clausura())

    def transicion(self, input: str):
        '''
        Devuelve una set con los estados a los que se llega para un input determinado
        El input será un
        '''
        if input not in self.automata.alfabeto:
            raise ErrorAutomata(
                str(input) + 'no es un input válido ' + str(self.automata.alfabeto))
        # variable que guradará los estados resultantes
        estados_resultantes = set()
        # recorremos la función de transición para cada input (si hubiera más de uno)
        for id_estado in self.f_transicion[input]:
            estado = self.automata.get_estado(set(id_estado))
            # añadimos el estado y su clausura
            estados_resultantes.update(list(estado.clausura()))
        # devolvemos una lista con todos los resultados
        return estados_resultantes

    def transicion_compuesta(self, input: str):
        '''
        Igual que transición pero devuelve un unico estado compuesto
        con los estados que resulten de ese input en concreto

        Devuelve None si no hubiera ningún estado como resultado del input
        '''
        # si la transición no diera nada lanzamos una excepción para evitar errores
        # en el reduce
        if len(self.transicion(input)) == 0:
            return None
        return reduce(lambda x, y: x+y, self.transicion(input))

def indexar(estados: set, clave: str = "A", verbose:bool = True):
    '''
    Devuelve un diccionario con los items del set indexados de forma item1 -> 'A', item2 -> 'B'...
    '''
    estados_indexados = {}
    for item in sorted(list(estados)):
        estados_indexados[item] = clave
        # aumentamos el valor de la clave
        clave = chr(ord(clave) + 1)
    # imprimimos el diccionario indexado
    if verbose:
        print('Nuevos estados -> ' + str(estados_indexados))
    return estados_indexados

def automata_from_dict_estados(estados_indexados: dict, **kwargs: dict):
    '''
    Para una Diccionario de estados indexados se devolverá un autómata con dicho indexados en un funcionamiento equivalente
    '''
    #comprobamos que los argumentos son correctos
    determinizar = None
    minimizar = None
    if kwargs.get('determinizar', False) and not kwargs.get('minimizar', False):
        #queremos determinizar
        determinizar = True
        minimizar = False
    elif not kwargs.get('determinizar', False) and  kwargs.get('minimizar', False):
        determinizar = False
        minimizar = True
    else:
        raise ErrorAutomata("Parámetros incorrectos -> " + kwargs)

    estados_finales = {}
    alfabeto = None
    # recorremos los pares estado antiguo -> nuevo id
    for item_1 in estados_indexados.items():
        # evaluamos cada input del alfabeto (sin lambda)
        # creamos una entrada para el nuevo estado en el diccionario y metemos sus parámetros inicial y final en él
        estados_finales[item_1[1]] = {}
        estados_finales[item_1[1]]['inicial'.upper()] = item_1[0].inicial
        estados_finales[item_1[1]]['final'.upper()] = item_1[0].final
        estados_finales[item_1[1]]['f_transicion'.upper()] = {}
        alfabeto = item_1[0].automata.alfabeto
        # evaluamos para cada input del alfabeto el estado compuesto en el que desemboca
        for input in alfabeto:
            # evaluamos el estado que conseguimos
            estado_result = item_1[0].transicion_compuesta(input)
            #obtener el estado asociado será diferente para determinizar que minimizar
            ids_result = None
            if determinizar:
                #el estado obtenido siempre será tal cual uno de los indexados
                #nos limitamos a buscar en los indexados si hay alguno que coincida
                if estados_indexados.get(estado_result, None) == None:
                    ids_result = []
                else:
                    ids_result = [estados_indexados[estado_result]]
            if minimizar:
                #sin embargo aquí el estado será tipo <A> siendo un elemento indexado <A,B> por ejemplo
                #<A,B> (o su nuevo id asociado mejor dicho) sería el estado que querríamos obtener
                #1º -> recorremos los estados indexados
                encontrado = False
                #comprobamos que realmente haya surgindo un estado de esa transición
                if estado_result != None:
                    for item_2 in estados_indexados.items():
                        if estado_result.id.issubset(item_2[0].id) or estado_result.id == item_2[0].id:
                            encontrado = True
                            ids_result = [estados_indexados[item_2[0]]]
                            break
                    if not encontrado:
                        ids_result = []
                else:
                    ids_result = []
            estados_finales[item_1[1]]['f_transicion'.upper()][input] = ids_result
    # devolvemos un nuevo autómata
    return Automata(alfabeto, estados_finales)


class Automata:
    '''Clase que representará a un autómata determinista'''

    def __init__(self, alfabeto: set = set(), estados: dict = {}):
        '''Un autómata se define por el alfabeto que admite y sus estados'''
        self.alfabeto = alfabeto
        self.estados_activos = set()
        self.estados = set()
        self.estados_definicion = estados
        # construimos el set de estados
        for estado_def in estados.items():
            id_estado = set(estado_def[0])
            inicial = estado_def[1].get('inicial'.upper(), False)
            final = estado_def[1].get('final'.upper(), False)
            f_transicion = estado_def[1].get('f_transicion'.upper(), {})
            self.estados.add(
                Estado(id_estado, self, inicial, final, f_transicion))

    def __str__(self):
        out = ''
        out += 'alfabeto: ' + str(list(self.alfabeto)) + '\n'
        out += 'estados activos: ' + str(list(self.estados_activos)) + '\n'
        out += 'estados: ' + '\n'
        for estado in sorted(list(self.estados)):
            out += str(estado) + '\n'
        return out

    def get_estado(self, id: set):
        '''
        Recibe el id (set de letras) que queramos buscar
        Normalmente será solo una {'A'}, pero si quisiéramos estados compuestos
        será de tantos estados como queramos componer

        Devuelve un estado o estado compuesto
        '''
        if len(id) == 1:
            # solo queremos un estado
            for estado in self.estados:
                if id == estado.id:
                    return estado
        else:
            lista_estados = set()
            for estado_id in id:
                for estado in self.estados:
                    if set(estado_id) == estado.id:
                        lista_estados.add(estado)
            return reduce(lambda x, y: x + y, lista_estados)

    def es_valido(self):
        '''
        Nos dice si es válido o no. Devuelve una lista con los errores encontrados
        '''
        errores = []

        if len(self.alfabeto) == 0:
            errores.append('El alfabeto debe ser tener al menos un input')
        elif set([item for item in self.alfabeto if len(item) == 1 and isinstance(item,str)]) != self.alfabeto:
            errores.append('Los elementos del alfabeto deben ser letras')
        num_estados_iniciales = 0
        num_estados_finales = 0
        for estado in self.estados:
            if estado.inicial:
                num_estados_iniciales +=1
            if estado.final:
                num_estados_finales +=1
            #vemos si las transiciones se corresponden con un estado
            for f_trans_individual in estado.f_transicion.items():
                if f_trans_individual[0] != 'lambda'.upper():
                    input = set(f_trans_individual[0])
                    if not input.issubset(self.alfabeto) and input != self:
                        errores.append('El input' + str(input) + ' del estado ' + repr(estado) + ' no está en el alfabeto del autómata ' + str(self.alfabeto))
                for output in f_trans_individual[1]:
                    if output not in self.estados_definicion.keys():
                        errores.append('El output <' + output + '> no se corresponde con ningún estado')
        if num_estados_iniciales != 1:
            errores.append('El autómata solo debe tener un estado inicial (tiene ' + str(num_estados_iniciales) + ')')
        if num_estados_finales == 0:
            errores.append('El autómata debe tener mínimo un estado final')
        return errores

    def es_determinista(self):
        '''Nos dice si el automata es determinista'''
        for estado in self.estados:
            for inputs in estado.f_transicion.items():
                if inputs[0] == 'lambda'.upper():
                    if len(inputs[1]) > 0:
                        return False
                else:
                    if len(inputs[1]) > 1:
                        return False
        return True
    
    def clausura_compuesta_inicial(self):
        '''Devuelve la clausura de partida que tendrá el autómata como estado compuesto'''
        for estado in self.estados:
            if estado.inicial:
                return estado.clausura_compuesta()
        return None

    def transformar_determinista(self):
        '''
        Devuelve un autómata determinista equivalente al actual
        '''
        if self.es_determinista():
            return self
        # metemos la clausura del estado inicial en la pila
        pila_auxiliar = [self.clausura_compuesta_inicial()]
        estados_resultado = set()
        if len(pila_auxiliar) == 0:
            raise ErrorAutomata('El autómata debe tener un estado inicial')
        # mientras que la pila no esté vacía
        while len(pila_auxiliar) > 0:
            # sacamos el tope de la pila y lo metemos en el resultado
            estado = pila_auxiliar.pop()
            estado.inicial = (estado == self.clausura_compuesta_inicial())
            estados_resultado.add(estado)
            # vemos sus estados para inputs del alfabeto (sin lambda)
            for input in self.alfabeto:
                estado_resultado = estado.transicion_compuesta(input)
                if estado_resultado not in estados_resultado and estado_resultado is not None:
                    pila_auxiliar.append(estado_resultado)
        # indexamos los estados resultantes para construir un nuevo automata
        return automata_from_dict_estados(indexar(estados_resultado, 'A'), determinizar = True)

    def minimizar(self) -> Automata:
        '''
        Devuelve el autómata determinista mínimo equivalente al actual

        El autómata debe ser determinista
        '''
        #nos aseguramos de que sea determinista
        if not self.es_determinista():
            raise ErrorAutomata("el autómata debe ser determinista para poder minimizarse")
        #construimos los dos conjuntos, generación anterior y la actual
        #serán listas de sets
        last_gen = []
        actual_gen = []
        #la generación actual tendrá dos conjuntos: los estados finales y los no finales
        #serán frozensets para evitar líos de hashabilidad al ser estos no mutables
        estados_finales = set([estado for estado in self.estados if estado.final])
        actual_gen.append(estados_finales)
        actual_gen.append(set(self.estados - estados_finales))
        #mientras haya cambios entre generaciones
        while last_gen != actual_gen:
            #guardamos la generación anterior en la anterior y vaciamos la generación actual
            last_gen = actual_gen.copy()
            actual_gen.clear()
            #iteramos en los grupos de estados de la generación pasada
            for grupo_estados_1 in last_gen:
                #creamos un diccionario para los resultados
                transiciones_grupo = {}
                #creamos una lista donde estarán los sets de nuevos grupos de estados que generemos
                #puede ser una lista porque last_gen es un set de frozensets
                nuevos_grupos_estados = []
                #para cada estado de un grupo de estados
                for estado in grupo_estados_1:
                    #creamos su entrada en el diccionario
                    transiciones_grupo[estado] = {}
                    #evaluamos sus posibles inputs
                    for input in self.alfabeto:
                        #vemos el estado al que vamos con ese input
                        #vale transición y transición compuesta pero usamos esta última porque nos da un estado y no un array
                        estado_resultado = estado.transicion_compuesta(input)
                        #vemos en que grupo de estados de la generación anterior se encuentra el estado
                        for grupo_estados_2 in last_gen:
                            if estado_resultado in grupo_estados_2:
                                transiciones_grupo[estado][input] = grupo_estados_2
                                break
                    #en este momento tenemos las transiciones del estado cargadas
                    #comprobaremos si hubiera un estado con transiciones hechas con la misma función de transicion
                    #que no sea a él mismo -> estados equivalentes
                    encontrado = False
                    for transicion_estado in transiciones_grupo.items():
                        if transicion_estado[0] != estado and transicion_estado[1] == transiciones_grupo[estado]:
                            encontrado = True
                            #iteraríamos sobre el contenido de la lista nuevos_grupos_estados para encontrar el set que
                            #contiene dicho estado y meterlo ahí
                            for nuevo_grupo_estados in nuevos_grupos_estados:
                                if transicion_estado[0] in nuevo_grupo_estados:
                                    nuevo_grupo_estados.add(estado)
                                    break
                            break
                    if not encontrado:
                        #si no fuera el caso creamos un nuevo set en nuevos_grupos_estados con solamente él
                        nuevos_grupos_estados.append(set([estado]))
                #una vez hemos recorrido todos los estados del grupo meteríamos los sets de estados en la generación actual
                actual_gen.extend(nuevos_grupos_estados)
        #llegados a este punto podemos asumir que last_gen y actual_gen son iguales y tienen sets de estados
        #los cuales se podrían combinar para minimizar el autómata borramos el past gen pa no confundir
        del last_gen
        #reducimos cada uno de ellos
        set_estados_minimos = set()
        for set_estados in actual_gen:
            #añadimos los estados del set compuestos al set de estados mínimos
            set_estados_minimos.add(reduce(lambda x,y: x + y, set_estados))
        #devolvemos el autómata que sale de esos estados
        return automata_from_dict_estados(indexar(set_estados_minimos, 'Q'), minimizar = True)



