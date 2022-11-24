import time
from itertools import product
from xml.dom import minidom

###############################################################
#########                   PETRI NET                  ########
###############################################################


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
        self.m, self.r, self.c, self.p = 0, 0, 0, 1

    def reset_petri_net(self):
        self.m, self.r, self.c, self.p = 0, 0, 0, 1
        # Remove all tokens
        for place in self.places.values():
            place.mark = 0

        # Give token to source
        self.places[1].do_mark()

    def get_remaining_tokens(self):
        for place in self.places.values():
            self.r += place.mark
        return self.r

    def add_place(self, id):
        self.places[id] = Place(id, 0)

    def add_transition(self, name, id):
        self.transitions[id] = Transition(id, name)

    def add_edge(self, source, target):
        if source not in self.edges:
            self.edges[source] = {"before": [], "after": []}
        if target not in self.edges:
            self.edges[target] = {"before": [], "after": []}

        if source < 0:
            self.edges[source]["after"].append(self.places[target])
            self.edges[source]["after"] = list(set(self.edges[source]["after"]))

            self.edges[target]["before"].append(self.transitions[source])
            self.edges[target]["before"] = list(set(self.edges[target]["before"]))
        else:
            self.edges[source]["after"].append(self.transitions[target])
            self.edges[source]["after"] = list(set(self.edges[source]["after"]))

            self.edges[target]["before"].append(self.places[source])
            self.edges[target]["before"] = list(set(self.edges[target]["before"]))

        return self

    def get_tokens(self, place):
        return self.places[place].mark

    def is_enabled(self, transition, fire_if_not_enabled=False):
        has_to_return_false = False
        for place in self.edges[transition]["before"]:
            if place.mark <= 0:
                has_to_return_false = True

                if fire_if_not_enabled:
                    # Still fire, then we mark it, and add it to missing token.
                    place.do_mark()
                    self.m += 1
                    has_to_return_false = False

        if has_to_return_false:
            return False
        else:
            return True

    def fire_transition(self, transition, fire_if_not_enabled=False):
        if self.is_enabled(transition, fire_if_not_enabled):
            for place in self.edges[transition]["before"]:
                place.unmark()
                self.c += 1

            for place in self.edges[transition]["after"]:
                place.do_mark()
                self.p += 1

    def transition_name_to_id(self, name):
        for transition_obj in self.transitions.values():
            if transition_obj.name == name:
                return transition_obj.id


def dependency_graph(log):
    for key, value in log.items():
        log[key] = [v["concept:name"] for v in value]

    TEMP = {}
    for tasks in log.values():
        for i in range(len(tasks) - 1):
            if tasks[i] not in TEMP:
                TEMP[tasks[i]] = {tasks[i + 1]: 1}
            elif tasks[i + 1] not in TEMP[tasks[i]]:
                TEMP[tasks[i]][tasks[i + 1]] = 1
            else:
                TEMP[tasks[i]][tasks[i + 1]] += 1
    return TEMP


###############################################################
#########                 READ_FROM_FILE               ########
###############################################################


def read_from_file(filename):
    CASES = {}
    file = minidom.parse(f"{filename}")

    for model in file.getElementsByTagName("trace"):
        case = model.getElementsByTagName("string")[0].attributes["value"].value
        if case not in CASES:
            CASES[case] = []

        for event in model.getElementsByTagName("event"):
            for ev in event.getElementsByTagName("string"):
                if ev.attributes["key"].value == "concept:name":
                    CASES[case].append({"concept:name": ev.attributes["value"].value})

    return CASES


###############################################################
#########                     ALPHA                    ########
###############################################################


def alpha(cases):
    FIRST_TRANSITION = list(cases.values())[0][0]
    FINAL_TRANSITION = list(cases.values())[-1][-1]

    d_g = dependency_graph(cases)

    ############################ Look for causal and parallels ############################

    causal, parallel = {}, {}

    for k in sorted(d_g.keys()):
        causal[k] = set()
        for vk in sorted(d_g[k].keys()):
            if vk in d_g and k in d_g[vk].keys():
                parallel[(k, vk)] = "2022"
            else:
                causal[k].add(vk)

    ##### Now create all the possible pairs of activites, by first taking the causal ####

    pairs = []
    for k, v in causal.items():
        for kv in v:
            pairs.append(({k}, {kv}))

    for i in range(0, len(pairs)):
        pair1 = pairs[i]
        for j in range(i, len(pairs)):
            pair2 = pairs[j]

            #### Check if the first pair is not a subset of the second one.
            if not (pair1[0].issubset(pair2[0]) or pair1[1].issubset(pair2[1])):
                continue

            ##### Create all possible combination, and check if it alreay exists in the causal
            # or the parallels activites. If it does, that means that its valid.
            relation = False
            for pair in product(pair1[0], pair2[0]):
                if pair in parallel or pair in causal:
                    relation = True

            for pair in product(pair1[1], pair2[1]):
                if pair in parallel or pair in causal:
                    relation = True

            if relation:
                continue

            ## Get the union of each member of pair to have a maximum set
            new_pair = (pair1[0] | pair2[0], pair1[1] | pair2[1])

            ### Don't take it if already exists
            if new_pair not in pairs:
                pairs.append(new_pair)

    # Getting all tasks name for the transitions
    all_tasks = list(d_g.keys())

    for v in d_g.values():
        all_tasks += list(v.keys())

    all_tasks = list(set(all_tasks))

    #### Instance petri net ####
    pn = PetriNet()

    #### Adding source and giving it a token ####
    pn.add_place(1)
    pn.places[1].do_mark()

    # Creating all transitions, starts from 1

    for idx in range(1, len(all_tasks) + 1):
        pn.add_transition(all_tasks[idx - 1], -idx)

    ####### Drop non maximum sets ######

    def drop_non_maximum_sets(pairs, p):
        for elem in pairs:
            # Compare the current pair to all of the possible pairs, and if it is a subset, remove it
            # For example, ({'accept'}, {'send decision e-mail'}) compared to ({'reject', 'accept'}, {'send decision e-mail'})
            # has to be removed because it is not a maximum set, it would have doubles.
            if p != elem and p[0].issubset(elem[0]) and p[1].issubset(elem[1]):
                return False
        return True

    # Filter the pairs to get only the on that correspond to a place
    PLACES = filter(
        lambda current_pair: drop_non_maximum_sets(pairs, current_pair), pairs
    )

    ######## Creating places ########

    for pair in PLACES:
        place_id = len(pn.places) + 1
        pn.add_place(place_id)

        for before in pair[0]:
            pn.add_edge(pn.transition_name_to_id(before), place_id)
        for after in pair[1]:
            pn.add_edge(place_id, pn.transition_name_to_id(after))

    # Add edge from first place to first transition
    pn.add_edge(1, pn.transition_name_to_id(FIRST_TRANSITION["concept:name"]))

    # Add sink and last transition leading to this place
    pn.add_place(len(pn.places) + 1)
    pn.add_edge(
        pn.transition_name_to_id(FINAL_TRANSITION["concept:name"]),
        pn.places[place_id + 1].id,
    )

    return pn


def fitness_token_replay(_log, _mined_model):
    _log_values = _log.values()

    m, c, p, r = [], [], [], []

    for trace in _log_values:
        id_trace = ""
        for t in trace:
            if "concept:name" in t:
                t = t["concept:name"]
            id_trace += t

            _mined_model.fire_transition(
                _mined_model.transition_name_to_id(t), fire_if_not_enabled=True
            )

        sink = _mined_model.places[len(_mined_model.places)]

        # Pull end token:
        if sink.mark == 0:
            # If not there, add a missing token and consume it
            _mined_model.m += 1
            _mined_model.c += 1
        elif sink.mark >= 1:
            # Consume one and the rest will be remaining tokens
            sink.unmark()
            _mined_model.c += 1

        m.append(_mined_model.m)
        r.append(_mined_model.get_remaining_tokens())
        c.append(_mined_model.c)
        p.append(_mined_model.p)

        _mined_model.reset_petri_net()

    f = 0.5 * (1 - (sum(m) / sum(c))) + 0.5 * (1 - (sum(r) / sum(p)))

    return f


###############################################################
#########                    TESTING                   ########
###############################################################

log = read_from_file("extension-log.xes")
log_noisy = read_from_file("extension-log-noisy.xes")

mined_model = alpha(log)

print(round(fitness_token_replay(log, mined_model), 5))
print(round(fitness_token_replay(log_noisy, mined_model), 5))
