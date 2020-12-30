

class ErrorAutomata(Exception):
    pass

class Automata:
    #declaramos variables para el autocompletado
    def __init__(self):
        self.alfabeto = set()
        self.estados_activos = set()
        self.estados = set()

class Estado:
    '''Clase que representará cada estado del autómata'''
    def __init__(self, id: set, automata: Automata, inicial: bool = False, final: bool = False, f_transicion: dict = {}):
        '''Cada estado tendrá un ID único que será un set, un autómata padre, su funcion de transición y si es final o inicial'''
        self.id = id
        self.automata = automata
        self.inicial = inicial
        self.final = final
        #construimos la funcion de transicion en base al alfabeto + lambda (cadena vacía)
        self.f_transicion = {}
        inputs_and_lambda = automata.alfabeto.copy()
        inputs_and_lambda.add('lambda'.upper())
        for input_or_lambda in inputs_and_lambda:
            self.f_transicion[input_or_lambda] = set(f_transicion.get(input_or_lambda,[]))

    def __str__(self):
        out = ''
        out += 'Estado ' + str(list(self.id)) + '\n'
        if self.inicial:
            out += '\t> estado inicial\n'
        if self.final:
            out += '\t> estado final\n'
        out += '\t> funcion de transicion' + str(self.f_transicion)
        return out

    def __repr__(self):
        return '<Estado' + str(list(self.id)) + '>'


class Automata:
    '''Clase que representará a un autómata determinista'''
    def __init__(self, alfabeto: set = set(), estados: dict = {}):
        '''Un autómata se define por el alfabeto que admite y sus estados'''
        self.alfabeto = alfabeto
        self.estados_activos = set()
        self.estados = set()
        #construimos el set de estados
        for estado_def in estados.items():
            id_estado = set(estado_def[0])
            inicial = estado_def[1].get('inicial'.upper(), False)
            final = estado_def[1].get('final'.upper(), False)
            f_transicion = estado_def[1].get('f_transicion'.upper(), {})
            self.estados.add(Estado(id_estado, self, inicial, final, f_transicion))
        #TODO: añadimos al set de estados activos los estados activos correspondientes


    def __str__(self):
        out = ''
        out += 'alfabeto: ' + str(list(self.alfabeto)) + '\n'
        out += 'estados activos: ' + str(list(self.estados_activos)) + '\n'
        out += 'estados: ' + '\n'
        for estado in self.estados:
            out += str(estado) + '\n'
        return out




