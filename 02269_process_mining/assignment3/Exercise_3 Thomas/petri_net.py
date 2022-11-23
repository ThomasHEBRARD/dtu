class Token():

    def __init__(self, id):
        self.id = id
        self.place = None
        self.transition = None

    def set_place(self, place):
        self.place = place

    def set_transition(self, transition):
        self.transition = transition

class Place():

    def __init__(self, id):
        self.id = id
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def remove_token(self, token):
        self.tokens.pop()

class Edge():

    def __init__(self, source, target):
        self.source = source
        self.target = target

class Transition():

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.enabled = False
        self.enabled_by = []
        self.disabled_by = []

    def set_enabled(self, enabled):
        self.enabled = enabled

    def set_enabled_by(self, enabled_by):
        self.enabled_by = enabled_by

    def set_disabled_by(self, disabled_by):
        self.disabled_by = disabled_by


class PetriNet():

    def __init__(self):
        self.places = {}
        self.transitions = {}
        self.edges = []

    def add_place(self, name):
        self.places[name] = Place(name)

    def add_transition(self, name, id):
        self.transitions[id] = Transition(name, id)

    def add_edge(self, source, target):
        self.edges.append(Edge(source, target))
        if target in self.transitions:
            disabled_by = self.transitions[target].disabled_by
            disabled_by.append(source)
            self.transitions[target].set_disabled_by(disabled_by)
        return self

    def get_tokens(self, place):
        # return the number of tokens on the place
        return len(self.places[place].tokens)

    def is_enabled(self, transition):
        return self.transitions[transition].enabled

    def add_marking(self, place):
        self.places[place].add_token(Token(place))
        for edge in self.edges:
            if edge.source == place:
                self.transitions[edge.target].set_enabled(True)

    def set_enabled(self, place):
        for edge in self.edges:
            if edge.source == place:
                self.transitions[edge.target].disabled_by.remove(place)
                self.transitions[edge.target].enabled_by.append(place)
                if len(self.transitions[edge.target].disabled_by) == 0:
                    self.transitions[edge.target].set_enabled(True)
                    self.transitions[edge.target].set_disabled_by(self.transitions[edge.target].enabled_by)
                    self.transitions[edge.target].set_enabled_by([])
                    
    
    def set_disabled(self, place):
        for edge in self.edges:
            if edge.source == place:
                self.transitions[edge.target].set_enabled(False)

    def fire_transition(self, transition):
        for edge in self.edges:
            if edge.source == transition:
                self.places[edge.target].add_token(Token(edge.target))
                self.set_enabled(self.places[edge.target].id)
            if edge.target == transition:
                self.places[edge.source].remove_token(Token(edge.source))
                self.set_disabled(self.places[edge.source].id)

    

