import pprint
import datetime

from itertools import combinations
from xml.dom import minidom
from xxlimited import foo

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

    def transition_name_to_id(self, name):
        for transition_obj in self.transitions.values():
            if transition_obj.name == name:
                return transition_obj.id


###############################################################
#########                 READ_FROM_FILE               ########
###############################################################


def read_from_file(filename):
    CASES = {}
    file = minidom.parse(
        f"/Users/thomashebrard/code/dtu/02269_process_mining/assignment3/{filename}"
    )

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
#########                     ALPHA                    ########
###############################################################


def alpha(cases):

    footprint = {}

    #################### NORMAL ORDER ####################

    for case in cases.values():
        for idx in range(len(case) - 1):
            task = case[idx]["concept:name"]
            next_task = case[idx + 1]["concept:name"]

            if task not in footprint:
                footprint[task] = {next_task: "->"}
            else:
                footprint[task][next_task] = "->"

            if (s := case[-1]["concept:name"]) not in footprint:
                footprint[s] = {}
    ############################################################

    #################### REVERSE ORDER ########################

    for case in cases.values():
        for idx in range(1, len(case)):
            idx = -idx
            task = case[idx]["concept:name"]
            prev_task = case[idx - 1]["concept:name"]

            footprint[task][prev_task] = "<-"
    ############################################################

    all_tasks = list(footprint.keys())

    #################### FILL EMPTY SPOTS ####################
    for f in footprint.values():
        for task in all_tasks:
            if task not in f:
                f[task] = "#"

    #################### REMOVE DOUBLES ####################

    for k in all_tasks:
        for v in all_tasks:
            if (
                footprint[k][v] == footprint[v][k]
                and footprint[k][v] != "#"
                and footprint[v][k] != "#"
            ):
                footprint[v][k] = "||"
                footprint[k][v] = "||"

    pprint.pprint(footprint)

    #################### POSSIBLE SETS ####################

    possible_sets = []

    # Simple with simple
    for k in all_tasks:
        for v in all_tasks:
            if footprint[k][v] == "->":
                possible_sets.append([k, v])

    def check_validity(footprint, possibilities):
        for k in possibilities:
            for v in possibilities:
                if footprint[k][v] != "#":
                    return False
        return True

    # Simple with multiples
    for k in all_tasks:
        candidates = []
        for v in all_tasks:
            if footprint[k][v] == "->":
                candidates.append(v)
        all_possibilities = [
            list(com)
            for sub in range(1, len(all_tasks))
            for com in combinations(candidates, sub + 1)
        ]
        for possibilities in all_possibilities:
            if check_validity(footprint, possibilities):
                possible_sets.append([k, possibilities])

    # SAME IN REVERSE
    for k in all_tasks:
        candidates = []
        for v in all_tasks:
            if footprint[k][v] == "<-":
                candidates.append(v)
        all_possibilities = [
            list(com)
            for sub in range(1, len(all_tasks))
            for com in combinations(candidates, sub + 1)
        ]
        for possibilities in all_possibilities:
            if check_validity(footprint, possibilities):
                possible_sets.append([possibilities, k])



###############################################################
#########                    TESTING                   ########
###############################################################

CASES = {
    "case_1": [
        {"concept:name": "a"},
        {"concept:name": "b"},
        {"concept:name": "c"},
        {"concept:name": "d"},
    ],
    "case_2": [
        {"concept:name": "a"},
        {"concept:name": "c"},
        {"concept:name": "b"},
        {"concept:name": "d"},
    ],
    "case_3": [{"concept:name": "a"}, {"concept:name": "e"}, {"concept:name": "d"}],
}
mined_model = alpha(CASES)

# def check_enabled(pn):
#   ts = ["record issue", "inspection", "intervention authorization", "action not required", "work mandate", "no concession", "work completion", "issue completion"]
#   for t in ts:
#     print (pn.is_enabled(pn.transition_name_to_id(t)))
#   print("")


# trace = ["record issue", "inspection", "intervention authorization", "work mandate", "work completion", "issue completion"]
# for a in trace:
#   check_enabled(mined_model)
#   mined_model.fire_transition(mined_model.transition_name_to_id(a))
