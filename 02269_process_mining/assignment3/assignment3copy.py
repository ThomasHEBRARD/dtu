import pprint
import datetime

from xml.dom import minidom
from itertools import combinations

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
        self.m, self.c, self.p = 0, 0, 0

    def reset_petri_net(self):
        self.m, self.c, self.p = 0, 0, 0
        for place in self.places.values():
            place.mark = 0

        self.places[1].mark = len(self.edges[-1]["before"])

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

    def is_enabled(self, transition):
        for place in self.edges[transition]["before"]:
            if place.mark <= 0:
                return False
        return True

    def fire_transition(self, transition):
        if self.is_enabled(transition):
            for place in self.edges[transition]["before"]:
                place.unmark()

            for place in self.edges[transition]["after"]:
                place.do_mark()

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
            event_data = {
                "org:resource": None,
                "concept:name": None,
                "cost": None,
                "time:timestamp": None,
            }
            # strings:
            for ev in event.getElementsByTagName("string"):
                if ev.attributes["key"].value in event_data:
                    event_data[ev.attributes["key"].value] = ev.attributes[
                        "value"
                    ].value
            # ints
            for ev in event.getElementsByTagName("int"):
                if ev.attributes["key"].value in event_data:
                    event_data[ev.attributes["key"].value] = int(
                        ev.attributes["value"].value
                    )

            date = datetime.datetime.strptime(
                event.getElementsByTagName("date")[0].attributes["value"].value,
                "%Y-%m-%dT%H:%M:%S%z",
            )
            date = date.replace(tzinfo=None)
            event_data[
                event.getElementsByTagName("date")[0].attributes["key"].value
            ] = date
            CASES[case].append(event_data)
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
            try:
                if k in d_g[vk].keys():
                    parallel[(k, vk)] = ""
                else:
                    causal[k].add(vk)
            except:
                causal[k].add(vk)

        if len(causal[k]) == 0:
            del causal[k]

    ############################ Look for causal and parallels ############################

    def check_related(causal, parallel, elem_1, elem_2):
        from itertools import product

        S = set(product(elem_1, elem_2)).union(set(product(elem_1, elem_2)))
        for pair in S:
            if pair in parallel or pair in causal:
                return True
        return False

    def identifiy_places(pairs, p):
        for elem in pairs:
            if p != elem and p[0].issubset(elem[0]) and p[1].issubset(elem[1]):
                return False
        return True

    pairs = []
    for key, element in causal.items():
        for item in element:
            pairs.append(({key}, {item}))

    for i in range(0, len(pairs)):
        p1 = pairs[i]
        for j in range(i, len(pairs)):
            p2 = pairs[j]

            if p1 == p2:
                continue

            # Check whether items in p1 are present in p2
            is_subset = p1[0].issubset(p2[0]) or p1[1].issubset(p2[1])
            if not is_subset:
                continue

            is_related = check_related(causal, parallel, p1[0], p2[0]) or check_related(
                causal, parallel, p1[1], p2[1]
            )

            if is_related:
                continue

            new_pair = (p1[0] | p2[0], p1[1] | p2[1])
            if new_pair not in pairs:
                pairs.append(new_pair)

    # Getting all task name for the transitions
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

    # Filter the pairs to get only the on that correspond to a place
    places_to_add = filter(lambda p: identifiy_places(pairs, p), pairs)

    # Adding all places
    for pair in places_to_add:
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


###############################################################
#########                    TESTING                   ########
###############################################################

mined_model = alpha(read_from_file("extension-log.xes"))
# mined_model = alpha(read_from_file("loan-process.xes"))


def check_enabled(pn, a):
    ts = [
        "record issue",
        "inspection",
        "intervention authorization",
        "action not required",
        "work mandate",
        "no concession",
        "work completion",
        "issue completion",
    ]
    # ts = [
    #     "register application",
    #     "check credit",
    #     "calculate capacity",
    #     "check system",
    #     "accept",
    #     "reject",
    #     "send decision e-mail",
    # ]
    for t in ts:
        print(pn.is_enabled(pn.transition_name_to_id(t)))
        pass
    print("")


trace = [
    "record issue",
    "inspection",
    "intervention authorization",
    "work mandate",
    "work completion",
    "issue completion",
]
# trace = [
#     "register application",
#     "check credit",
#     "check system",
#     "calculate capacity",
#     "accept",
#     "send decision e-mail",
# ]
for a in trace:
    check_enabled(mined_model, a)
    mined_model.fire_transition(mined_model.transition_name_to_id(a))
