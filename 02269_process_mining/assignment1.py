class Transition:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Place:
    def __init__(self, id, mark):
        self.id = id
        self.mark = mark

    def do_mark(self):
        self.mark += 1

    def unmark(self):
        self.mark -= 1


class PetriNet:
    def __init__(self):
        self.places = {}
        self.transitions = {}
        self.edges = {}

    def add_place(self, id):
        self.places[id] = Place(id, 0)
        pass

    def add_transition(self, name, id):
        self.transitions[id] = Transition(id, name)

    def add_edge(self, source, target):
        if source not in self.edges:
            self.edges[source] = {"before": [], "after": []}
        if target not in self.edges:
            self.edges[target] = {"before": [], "after": []}

        self.edges[source]["after"].append(
            self.places[target] if source < 0 else self.transitions[target]
        )
        self.edges[target]["before"].append(
            self.places[source] if source > 0 else self.transitions[source]
        )

        return self

    def get_tokens(self, place):
        return self.places[place].mark

    def is_enabled(self, transition):
        for place in self.edges[transition]["before"]:
            if place.mark == 0:
                return False
        return True

    def add_marking(self, place):
        self.places[place].do_mark()

    def fire_transition(self, transition):
        for place in self.edges[transition]["before"]:
            place.unmark()

        for place in self.edges[transition]["after"]:
            place.do_mark()
