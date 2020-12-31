

class ErrorAutomata(Exception):
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
        out += '\t> funcion de transicion' + str(self.f_transicion)
        return out

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
        #primero siempre irá el inicial
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

    def __hash__(self):
        '''identificador unico del estado'''
        return hash(str(sorted(list(self.id))))

    def clausura(self):
        '''
        Devuelve un set con él mismo y los estados recursivos por la cadena vacía
        '''
        pass


class Automata:
    '''Clase que representará a un autómata determinista'''

    def __init__(self, alfabeto: set = set(), estados: dict = {}):
        '''Un autómata se define por el alfabeto que admite y sus estados'''
        self.alfabeto = alfabeto
        self.estados_activos = set()
        self.estados = set()
        # construimos el set de estados
        for estado_def in estados.items():
            id_estado = set(estado_def[0])
            inicial = estado_def[1].get('inicial'.upper(), False)
            final = estado_def[1].get('final'.upper(), False)
            f_transicion = estado_def[1].get('f_transicion'.upper(), {})
            self.estados.add(
                Estado(id_estado, self, inicial, final, f_transicion))
        # TODO: añadimos al set de estados activos los estados activos correspondientes

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
            # todo:queremos un estado compuesto
            pass

    def es_determinista(self):
        '''Nos dice si el automata es determinista'''
        for estado in self.estados:
            for inputs in estado.f_transicion.items():
                if len(inputs['lambda'.upper()]) > 1:
                    return False
        return True
