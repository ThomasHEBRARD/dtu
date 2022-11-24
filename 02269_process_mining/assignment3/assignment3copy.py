import datetime

from xml.dom import minidom
from itertools import product

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


###############################################################
#########                    TESTING                   ########
###############################################################

# mined_model = alpha(read_from_file("extension-log.xes"))
mined_model = alpha(read_from_file("loan-process.xes"))


def check_enabled(pn, a):
    # ts = [
    #     "record issue",
    #     "inspection",
    #     "intervention authorization",
    #     "action not required",
    #     "work mandate",
    #     "no concession",
    #     "work completion",
    #     "issue completion",
    # ]
    ts = [
        "register application",
        "check credit",
        "calculate capacity",
        "check system",
        "accept",
        "reject",
        "send decision e-mail",
    ]
    for t in ts:
        print(pn.is_enabled(pn.transition_name_to_id(t)))
        pass
    print("")


# trace = [
#     "record issue",
#     "inspection",
#     "intervention authorization",
#     "work mandate",
#     "work completion",
#     "issue completion",
# ]
trace = [
    "register application",
    "check credit",
    "check system",
    "calculate capacity",
    "accept",
    "send decision e-mail",
]
for a in trace:
    check_enabled(mined_model, a)
    mined_model.fire_transition(mined_model.transition_name_to_id(a))
