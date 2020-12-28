import functools

class ErrorAutomata(Exception):
    pass


def eliminar_duplicados(lista):
    res = []
    for item in lista:
        if item not in res:
            res.append(item)
    lista.clear()
    for item_res in res:
        lista.append(item_res)


class Estado:
    def __init__(self, automata_padre, *id, **kwargs):
        '''
        Recibe como argumento el autómata padre al que pertenece,
        la lista con los id's (uno por defecto) y por último
        el diccionario de definición del estado
        '''
        self.automata_padre = automata_padre
        lista_ids = list(id)
        eliminar_duplicados(lista_ids)
        self.id = lista_ids
        self.inicial = kwargs.get("inicial".upper(), False)
        self.final = kwargs.get("final".upper(), False)
        # la funcion de transición será un diccionario de sets
        self.func_transicion = {}
        for inputs in kwargs.get("f_transicion".upper(), {}).items():
            self.func_transicion[inputs[0]] = []
            for estado_resultante in inputs[1]:
                self.func_transicion[inputs[0]].append(estado_resultante)
                # eliminamos duplicados que puedan surgir
                eliminar_duplicados(self.func_transicion[inputs[0]])

    def __eq__(self, o: object):
        if not isinstance(o, self.__class__):
            return False
        #ordenamos los ids previo a compararlos
        id_obj_ord = o.id
        id_obj_ord.sort()
        id_self_ord = self.id
        id_self_ord.sort()
        #comparamos ahora si
        return functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q,id_obj_ord,id_self_ord), True)
        #return isinstance(o, self.__class__) and o.id == self.id

    def __str__(self):
        out = ''
        out += 'ESTADO ' + str(self.id) + '\n'
        if self.inicial:
            out += '\t> estado inicial\n'
        if self.final:
            out += '\t> estado final\n'
        out += '\t Función de transicion: ' + str(self.func_transicion) + '\n'
        return out

    def __repr__(self):
        return '<estado ' + str(self.id) + '>'

    def __add__(self, other):
        '''
        Compone dos estados en uno solo
        '''
        if not isinstance(other, self.__class__):
            raise ErrorAutomata('No se puede sumar un estado con un ' + str(other.__class__))
        #creamos el automata padre del resultado
        if(other.automata_padre != self.automata_padre):
            raise ErrorAutomata('No se pueden sumar estados de dos autómatas distintos (' + str(self) + ' y ' + str(other) + ')')
        padre = self.automata_padre
        #creamos el id compuesto
        id = [*other.id, *self.id]
        eliminar_duplicados(id)
        #creamos si es final o inicial con un diccionario
        dict_definicion = {}
        dict_definicion["inicial".upper()] = self.inicial or other.inicial
        dict_definicion["final".upper()] = self.final or other.final
        #creamos la funcion de transicion compuesta
        dict_definicion['f_transicion'.upper()] = {}
        #la lista de inputs posibles será el alfabeto + la cadena vacía
        for letra_alfabeto in self.automata_padre.alfabeto:
            dict_definicion['f_transicion'.upper()][str(letra_alfabeto)] = [*self.func_transicion[str(letra_alfabeto)], *other.func_transicion[str(letra_alfabeto)]]
            eliminar_duplicados(dict_definicion['f_transicion'.upper()][str(letra_alfabeto)])
        #para lambda añadimos aquellos estado que no estén en el id del estado
        dict_definicion['f_transicion'.upper()]['lambda'.upper()] = []
        for estado_lambda in [*self.func_transicion['lambda'.upper()], *other.func_transicion['lambda'.upper()]]:
            if estado_lambda not in id and estado_lambda not in dict_definicion['f_transicion'.upper()]['lambda'.upper()]:
                dict_definicion['f_transicion'.upper()]['lambda'.upper()].append(estado_lambda)
        #creamos un nuevo estado con los nuevos datos
        return Estado(padre, *id, **dict_definicion)


    def transicion(self, input):
        '''
        Devuelve una lista con el estado al que se llega por ese input (compuesto si hubiera más de uno)
        '''
        if input not in self.automata_padre.alfabeto:
            raise ErrorAutomata(str(input) + 'no es un input válido ' + str(self.automata_padre.alfabeto))
        lista_estados = []
        #obtenemos la lista de estados finales para ese input
        for id_estado in self.func_transicion[str(input)]:
            estado = self.automata_padre.get_estado([id_estado])
            if estado not in lista_estados:
                lista_estados.append(estado)
            #añadimos la clausura de cada estado final al que lleguemos
            for estado_clausura in estado.clausura():
                if estado_clausura not in lista_estados:
                    lista_estados.append(estado_clausura)
        #de la lista de estados que obtengamos la combinamos en un único estado
        return functools.reduce(lambda x, y: x + y, lista_estados)


    def clausura(self):
        '''
        Devuelve una lista de estados que será la clausura del estado
        es decir las transiciones recursivas por la cadena vacía
        '''
        pilaAuxiliar = [self.id]
        # meto la primera generación de estados por la cadena vacia en pilaAuxiliar
        for estado_lambda in self.func_transicion['lambda'.upper()]:
            pilaAuxiliar.append([estado_lambda])
        # lista donde guardaremos los estados que obtengamos
        resultado = []
        # mientras la pila tenga algo
        while len(pilaAuxiliar) > 0:
            # quito el tope de la pila
            estado = self.automata_padre.get_estado(pilaAuxiliar.pop())
            # lo añado a los elemntos procesados
            resultado.append(estado)
            #obtengo la descendencia
            ids_clausura = estado.func_transicion['lambda'.upper()]
            #por cada elemento de la descendencia
            for id_estado_clausura in ids_clausura:
                #lo transformo de id a estado
                estado_clausura = self.automata_padre.get_estado([id_estado_clausura])
                #si no lo he procesado lo añado a la pila
                if estado_clausura not in resultado:
                    pilaAuxiliar.append(estado_clausura.id)
        eliminar_duplicados(resultado)
        return resultado


class Automata:
    def __init__(self, **dict_definicion):
        '''
        Iniciamos el autómata vacío o con el diccionario de definicion en json
        '''
        self.dict_definicion = dict_definicion
        self.alfabeto = dict_definicion.get('alfabeto'.upper(), [])
        self.estados = []
        # creamos cada uno de los estados
        for estado in dict_definicion.get('estados'.upper(), {}).items():
            self.estados.append(Estado(self, estado[0], **(estado[1])))
        # eliminamos estados duplicados
        eliminar_duplicados(self.estados)

    def __str__(self):
        out = ''
        out += '*) alfabeto: ' + str(self.alfabeto) + '\n'
        out += '*) estados actuales:' + '\n'
        out += '*) estados posibles:' + '\n'
        for estado in self.estados:
            out += str(estado)
        return out

    def get_estado(self, id):
        '''
        Recibe el id (lista de letras) que queramos buscar
        Normalmente será solo una ['A'], pero si quisiéramos estados compuestos
        será de tantos estados como queramos componer

        Devuelve un estado o estado compuesto
        '''
        if len(id) == 1:
            #solo queremos un estado
            for estado in self.estados:
                if id == estado.id:
                    return estado
            raise ErrorAutomata("No se ha encontrado ningún estado con id ->" + str(id))
        else:
            #queremos un estado compuesto
            lista_estados = []
            for estado_individual in id:
                for estado_automata in self.estados:
                    if [estado_individual] == estado_automata.id:
                        lista_estados.append(estado_automata)
            #una vez que hayamos pillado todos los estados los sumamos y los devolvemos
            return functools.reduce(lambda x, y: x + y, lista_estados)

    def es_determinista(self):
        for estado in self.estados:
            for inputs in estado.func_transicion.items():
                if len(inputs[1]) > 1:
                    return False
        return True

    def transformar_determinista(self):
        '''
        Devuelve un autómata determinista equivalente al actual
        '''
        if self.es_determinista():
            raise ErrorAutomata('El autómata ya es determinista')
        #estructuras de datos auxiliares
        pila_auxiliar = []
        estados_resultado = []
        #empezamos localizando el estado inicial
        estado_inicial = None
        for estado in self.estados:
            if estado.inicial:
                estado_inicial = estado
        #obtenemos su clausura
        estado_inicial = functools.reduce(lambda x, y: x+y, estado_inicial.clausura())
        #lo metemos en la pilaAuxiliar
        pila_auxiliar.append(estado_inicial)
        #mientras que haya elemntos en la pila que procesar
        while len(pila_auxiliar) > 0:
            #sacamos el tope de la pila
            estado_tope = pila_auxiliar.pop();
            #lo metemos en el resultado si no estuviera
            if estado_tope not in estados_resultado:
                estados_resultado.append(estado_tope)
            #vemos sus outputs para sus inputs del alfabeto (SIN LAMBDA)
            for input in self.alfabeto:
                estado_resultado = estado_tope.transicion(input)
                if estado_resultado not in estados_resultado:
                    pila_auxiliar.append(estado_resultado)
        #imprimimos el resultado
        print(estados_resultado)




    def minimizar(self):
        pass
